# 🤖 ThreatIntel Telegram Bot

An automated, secure Threat Intelligence Agent designed for Security Operations Center (SOC) engineers. This bot periodically polls live cybersecurity news feeds, uses local AI to synthesize actionable threat advisories, and delivers them silently to a private Telegram channel.

## 🚀 Key Features

* **Secure Credential Handling**: Uses `.env` files and `.gitignore` to ensure your API keys and tokens never leave your local machine.
* **Context-Injected Intelligence**: Bypasses the limitations of small-language models by handling data parsing via Python and injecting sanitized content into the AI context.
* **Actionable SOC Playbooks**: Instead of generic summaries, the bot generates custom **Remediation Actions** and **Detection Use Cases** tailored for your existing monitoring infrastructure.
* **Deterministic Reasoning**: Uses `temperature=0` to ensure threat reporting remains factual, professional, and free from AI hallucinations.

## ⚙️ Architecture Overview



1. **Ingestion**: Python-native RSS parsing (The Hacker News).
2. **Synthesis**: Local Llama 3.1 LLM (via Ollama/LangGraph) compiles the advisory.
3. **Delivery**: Silent API-driven delivery via the Telegram Bot API.

## 🛠️ Setup & Installation

### 1. Prerequisites
- **Ollama**: Ensure [Ollama](https://ollama.com/) is installed and the `llama3.1` model is pulled.
- **Python 3.x**: Ensure Python is installed.

### 2. Configuration
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
