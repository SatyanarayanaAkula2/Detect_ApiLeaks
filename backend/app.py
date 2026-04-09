import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from source import run_local_test, scan_specific_repo, run_global_scan, process_text

# 🔹 Page Config
st.set_page_config(page_title="Secret Leak Scanner", layout="wide")

# 🎨 SAME CSS (unchanged)
st.markdown("""
<style>
h1 {
    text-align: center;
    font-size: 36px;
    font-weight: 700;
}
.subtitle {
    text-align: center;
    color: #6c757d;
    margin-bottom: 25px;
}
div.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 600;
    border: none;
    color: white;
    transition: all 0.25s ease;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
}
</style>
""", unsafe_allow_html=True)

# 🔹 HEADER
st.markdown("<h1>Secret Leak Detection Platform</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Detect exposed credentials across public sources with risk analysis</p>", unsafe_allow_html=True)

# 🔹 NAVIGATION
page = st.sidebar.radio(
    "Navigate",
    ["📝 Text Scan", "📄 File Scan", "🔗 Repo Scan", "🌍 Global Scan"]
)

# 🔹 SESSION STATE
if "results" not in st.session_state:
    st.session_state.results = []

# 🔹 COMMON RESULT UI (UNCHANGED + FILTER ADDED)
def show_results():
    if "results" not in st.session_state:
        st.session_state.results = []
    results = st.session_state.results

    if not results:
        st.warning("No secrets detected")
        return
    st.markdown("## scan results")

    df = pd.DataFrame(results)
    filtered_df=df.copy()
    st.markdown("## Alerts")
    alert_found=False
    for _, row in df.iterrows():
        if(row.get("risk")=="HIGH"):
            alert_found=True
            st.error(f"{row['type']} detected | Risk:{row['risk']}\n\n reason:{row['reason']}")
    if not alert_found:
        st.success("No Critical alerts")

    st.markdown("---")
    st.markdown("## Results")

    # 🔥 FILTER (NOW PERSISTENT)
    filter_option = st.selectbox(
        "Filter by Risk Level",
        ["ALL", "HIGH", "MEDIUM", "LOW"],
        key="filter"
    )

    if filter_option != "ALL":
        filtered_df = df[df["risk"] == filter_option]
    if df.empty:
        st.warning("No secrets detected for selected filter")
        return

    # 🔹 METRICS
    high = len(df[df["risk"] == "HIGH"])
    medium = len(df[df["risk"] == "MEDIUM"])
    low = len(df[df["risk"] == "LOW"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Findings", len(df))
    col2.metric("High Risk", high)
    col3.metric("Medium Risk", medium)
    col4.metric("Low Risk", low)

    # 🔹 CHART (same)
    st.markdown("### Risk Severity Distribution")

    labels = ["High", "Medium", "Low"]
    sizes = [high, medium, low]
    colors = ["#ff6b6b", "#f7b731", "#2ecc71"]

    fig, ax = plt.subplots(figsize=(2.2, 2.2))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    if high == 0 and medium == 0 and low == 0:
        st.warning("No data to display chart for selected filter")
        return
    ax.pie(sizes, colors=colors, startangle=90, wedgeprops=dict(width=0.35))
    centre_circle = plt.Circle((0, 0), 0.72, fc='white')
    fig.gca().add_artist(centre_circle)

    ax.text(0, 0, str(len(df)), ha='center', va='center',
            fontsize=12, fontweight='bold')

    ax.axis('equal')
    plt.tight_layout()

    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.pyplot(fig, transparent=True)

    # 🔹 TABLE
    st.markdown("### Detailed Findings")
    st.dataframe(df, use_container_width=True)


    st.markdown("# Export Results")
    col11,col22=st.columns(2)
    with col11:
        if not df.empty:
            full_csv=df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Full report CSV",
                data=full_csv,
                file_name="scan_results.csv",
                mime="text/csv"
            )
        else:
            st.info("No available data to download")
    with col22:
        if not filtered_df.empty:
            filtered_csv=df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download filtered report CSV",
                data=filtered_csv,
                file_name="filtered_scan_results.csv",
                mime="text/csv"
            )
        else:
            st.info("No available data to download")
# =========================================================
# 📝 TEXT SCAN
# =========================================================
if page == "📝 Text Scan":
    st.markdown("### Paste Text to Scan")

    text_input = st.text_area("Enter text", height=200)

    if st.button("Scan Text"):
        if text_input.strip():
            with st.spinner("Scanning text..."):
                results=process_text(text_input,"text_input")
            st.session_state.results = results
            st.toast("Text scan completed")

        else:
            st.warning("Enter text")

# =========================================================
# 📄 FILE SCAN
# =========================================================
elif page == "📄 File Scan":
    st.markdown("### Upload File")

    uploaded_file = st.file_uploader("Choose file", type=["txt", "py", "env", "json"])

    if st.button("Scan File"):
        if uploaded_file:
           
            with st.spinner("Scanning File..."):
                content = uploaded_file.read().decode("utf-8", errors="ignore")
                results=process_text(content,uploaded_file.name)
            st.session_state.results = results
            st.toast("File scan completed")


        else:
            st.warning("Upload file first")

# =========================================================
# 🔗 REPO SCAN
# =========================================================
elif page == "🔗 Repo Scan":
    st.markdown("### Scan GitHub Repository")

    repo_url = st.text_input("GitHub Repo URL")

    if st.button("Scan Repo"):
        if repo_url:
            with st.spinner("Scanning repository..."):
                results, error = scan_specific_repo(repo_url)

            if error:
                st.error(error)
            else:
                st.session_state.results = results
                st.toast("Repository scan completed")
    
        else:
            st.warning("Enter repository URL")

# =========================================================
# 🌍 GLOBAL SCAN
# =========================================================
elif page == "🌍 Global Scan":
    st.markdown("### Scan GitHub Globally")

    limit = st.slider("Number of leaks to detect", 1, 50, 10)

    if st.button("Run Global Scan"):
       with st.spinner("Running global scan..."):
            results, error = run_global_scan(target_results=limit)  
            if error:
                st.error(error)
            else:
                st.session_state.results = results
                st.toast("Global scan completed")
# 🔥 ALWAYS SHOW RESULTS (fix)
if st.session_state.results:
    show_results()