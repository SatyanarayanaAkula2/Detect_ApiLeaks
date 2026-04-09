# Secret Leak Detection Platform

LeakGuard is a powerful security tool that detects exposed secrets such as API keys, tokens, and credentials from text, files, GitHub repositories, and global GitHub search.

It combines **regex detection, entropy analysis, and contextual risk scoring** to identify and classify sensitive information.

## 🚀 Features

* 🔍 Detect secrets using pattern matching (API keys, tokens, passwords)
* 🧠 Entropy-based analysis to identify randomness
* 📊 Context-based scoring to reduce false positives
* ⚖️ Risk classification (LOW / MEDIUM / HIGH)
* 🌍 Global GitHub scanning
* 📂 Repository scanning
* 📄 File-based scanning
* 📝 Text input scanning
* 📈 Interactive dashboard with charts and filters


## 🧩 Tech Stack

* Python
* Streamlit (Frontend UI)
* FastAPI (Backend API)
* Pandas & Matplotlib (Data visualization)
* GitHub API (Code search)


## 📁 Project Structure

```
.
├── streamlit_app/
│   ├── app.py
├── github/
│   ├── fetcher.py
│   ├── parser.py
├── detector/
│   ├── regex.py
│   ├── entropy.py
│   ├── context.py
├── classification/
│   ├── risk_engine.py
├── utils/
│   ├── helper.py
├── source.py
├── .env
├── .gitignore
```

## ⚙️ Installation

```bash
git clone https://github.com/your-username/secret-leak-scanner.git
cd secret-leak-scanner
pip install -r requirements.txt
```


## 🔑 Environment Setup

Create a `.env` file:

```
GITHUB_TOKEN=your_github_token_here
```

⚠️ Do NOT commit `.env` to GitHub.


## ▶️ Run the Application

### Streamlit UI

```bash
streamlit run app.py
```


### FastAPI Backend (optional)

```bash
uvicorn app:app --reload
```


## 🧪 How It Works

1. Detect secrets using regex patterns
2. Calculate entropy to measure randomness
3. Extract surrounding context
4. Assign risk score using:

   * Secret type
   * Entropy
   * Context
5. Classify severity (LOW / MEDIUM / HIGH)


## 📊 Risk Scoring

Risk is calculated as:

```
Risk = Base Severity + Entropy Factor + Context Score
```


## 🔍 Scan Modes

* 📝 Text Scan → Paste and analyze text
* 📄 File Scan → Upload files
* 🔗 Repo Scan → Scan a GitHub repository
* 🌍 Global Scan → Search across GitHub


## 🔐 Security Note

* Never expose real API keys in public repositories
* Always use `.env` for secrets
* Revoke any leaked tokens immediately


## 🛠 Future Improvements

* 🔄 Async scanning for better performance
* 🤖 ML-based detection
* 📡 Real-time monitoring
* 🔔 Alert system


## 🤝 Contributing

Contributions are welcome!
Feel free to fork and submit pull requests.


## 📜 License

This project is open-source and available under the MIT License.


## 👨‍💻 Author

Developed by **Satyanarayana Akula**

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
