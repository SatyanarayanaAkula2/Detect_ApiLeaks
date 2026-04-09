from github.fetcher import (
    parse_github_url,
    get_repo_files,
    search_public_code,
    get_file_content
)
from github.parser import normalize_text
from detector.regex import detect_secrets
from detector.entropy import shannon_entropy
from detector.context import extract_context
from classification.risk_engine import calculate_risk
from utils.helper import mask, timestamp
from utils.alert import send_alert

import requests


# 🔹 Process text
def process_text(text, source="manual"):
    results = []

    findings = detect_secrets(text)

    for f in findings:
        secret = f["secret"]
        secret_type = f["type"]

        entropy = shannon_entropy(secret)
        context_text = extract_context(text, secret)

        risk = calculate_risk(secret_type, entropy, context_text)

        alert_msg=None
        if(risk["risk"]=="HIGH"):
            alert_msg=send_alert({
                "source":source,
                "type":secret_type,
                "risk":risk["risk"],
                "reason":risk["reason"]
            })

        results.append({
            "secret": mask(secret),
            "type": f["type"],
            "entropy": entropy,
            "risk": risk["risk"],
            "risk_score": risk["score"],
            "confidence": risk["confidence"],
            "reason": risk["reason"],
            "source": source,
            "timestamp": timestamp(),
            "alert":risk["risk"]=="HIGH",
            "alert_message": alert_msg
        })

    return results

#text scan
def scan_text_input(text:str):
    try:
        if not text.strip():
            return [],"Empty input text"
        results=process_text(text,source="text-input")
        return results,None
    except Exception as e:
        print("Text scan error:",str(e))
        return [],str(e)

#file scan
def scan_file_content(content:str,filename="uploaded_file"):
    try:
        if not content.strip():
            return[],"Empty File"
        text=normalize_text(content)
        results=process_text(text,source=filename)
        return results,None
    except Exception as e:
        print("File scan error:",str(e))
        return [],str(e)

# 🔗 Repo scan (WORKING)
def scan_specific_repo(repo_url):
    try:
        owner, repo = parse_github_url(repo_url)
    except:
        return [], "Invalid GitHub URL"

    file_urls, err = get_repo_files(owner, repo)

    if err:
        return [], err

    if not file_urls:
        return [], "No files found"

    results = []

    for file_url in file_urls[:20]:  # 🔥 LIMIT FILES
        content = get_file_content(file_url)

        if not content:
            continue

        text = normalize_text(content)
        findings = process_text(text, repo_url)

        results.extend(findings)

    if not results:
        return [], "No secrets detected"

    print("✅ Repo scan results:", len(results))
    return results, None


# 🌍 Global scan (FIXED)
def run_global_scan(target_results=5):
    results = []

    print("🔥 Starting global scan...")

    items, err = search_public_code(per_page=target_results*2)

    if err:
        print("❌ GitHub error:", err)
        return [], err

    if not items:
        print("❌ No items from GitHub")
        return [], "No results from GitHub"

    print(f"🔍 Found {len(items)} items")

    for item in items:  # 🔥 LIMIT API CALLS
        try:
            html_url = item.get("html_url")

            if not html_url:
                continue

            print("📂 Processing:", html_url)

            # 🔥 Convert to RAW URL
            raw_url = html_url.replace("github.com", "raw.githubusercontent.com")
            raw_url = raw_url.replace("/blob/", "/")

            print("➡️ RAW URL:", raw_url)

            response = requests.get(raw_url, timeout=5)

            if response.status_code != 200:
                print("❌ Failed to fetch raw content")
                continue

            content = response.text

            print("✅ Content length:", len(content))

            text = normalize_text(content)
            findings = process_text(text, html_url)

            print("🔎 Findings:", len(findings))

            results.extend(findings)

            if len(results) >= target_results:
                break

        except Exception as e:
            print("⚠️ Error processing file:", e)
            continue

    # 🔥 Fallback if no results
    if not results:
        print("⚠️ No real results found → returning demo data")

        return [],"No data found from global scan"

    print("✅ Global scan results:", len(results))
    return results[:target_results], None