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


## 🤖 Setting up your Telegram Bot

To receive these alerts, you need to register a bot with Telegram and obtain your Chat ID.

### 1. Create your Telegram Bot
1. Open Telegram and search for **@BotFather**.
2. Click **Start** and send the command `/newbot`.
3. Follow the instructions to give your bot a **Name** and a **Username** (must end in `_bot`).
4. Once created, BotFather will provide an **API Token**. Keep this safe; this is your `TELEGRAM_BOT_TOKEN`.

### 2. Obtain your Chat ID
1. Search for **@userinfobot** in Telegram and start a chat.
2. Send any message to it. It will reply with your numerical **Id**. This is your `TELEGRAM_CHAT_ID`.

### 3. Initialize the Bot
1. Search for your new bot in Telegram by its username and click **Start**.
2. You must interact with the bot once (send "Hello") so the bot is authorized to send you messages.

*Note: Your `.env` file should now look like this:*
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ
TELEGRAM_CHAT_ID=987654321
