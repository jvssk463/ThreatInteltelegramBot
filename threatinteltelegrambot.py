import os
import json
import requests
import feedparser
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HISTORY_FILE = "sent_items.json"

# 1. Initialize the AI (Deterministic)
llm = ChatOllama(model="llama3.1", temperature=0)

# 2. History Management
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-100:], f)  # Keep last 100 to avoid file bloat

# 3. Data Ingestion: Scans multiple feeds and multiple entries per feed
def fetch_new_threat(sent_items):
    # List of RSS feeds to monitor
    feed_urls = [
        "https://feeds.feedburner.com/TheHackersNews",
        "https://www.bleepingcomputer.com/feed/"
    ]
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for url in feed_urls:
        try:
            print(f"[SYSTEM] Scanning feed: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                # Check top 5 entries of each feed
                for entry in feed.entries[:5]: 
                    entry_id = entry.get('link')
                    if entry_id not in sent_items:
                        return entry, None # Found a new one!
        except Exception as e:
            print(f"[SYSTEM] Error scanning {url}: {e}")
            continue
            
    return None, "No new alerts found across all feeds."

# 4. AI Tool
@tool
def send_background_telegram(message_content: str) -> str:
    """Sends the finalized threat briefing to the user via Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return "FAILED: Missing environment configuration."
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message_content}
    response = requests.post(url, json=payload, timeout=10)
    
    return "SUCCESS" if response.status_code == 200 else f"FAILED: {response.text}"

# Setup Agent
tools = [send_background_telegram]
agent_executor = create_react_agent(llm, tools)

# 5. EXECUTION LOGIC
print("--- Activating Background Cybersecurity Agent ---")

sent_items = load_history()
top_alert, error = fetch_new_threat(sent_items)

if error:
    print(f"[SYSTEM] {error}")
else:
    print(f"[SYSTEM] New threat found: {top_alert.get('title')}. Processing...")
    
    task = f"""
    You are an expert SOC Engineer and Threat Intelligence Analyst. 
    Analyze the following threat data and compile a highly professional, actionable advisory:
    
    Title: {top_alert.get('title')}
    Summary: {top_alert.get('summary')}
    Link: {top_alert.get('link')}
    
    Response format:
    
    🚨 THREAT INTEL ADVISORY 🚨
    Title: [Insert exact Title here]
    -------------------------------------------
    
    📋 BRIEF SUMMARY
    [Provide a concise 2-3 sentence technical overview of the attack vector or vulnerability based on the summary provided.]
    
    🛡️ REMEDIATION ACTIONS
    - [Provide a direct patching, upgrading, or configuration hardening action]
    - [Provide a user awareness or policy-based remediation step relevant to this specific attack]
    
    🔍 SOC DETECTION USE CASES
    - Use Case 1 (Log Source): [Provide a specific detection logic description. Identify the target log source (e.g., Firewall logs, EDR telemetry, Web Application Proxy, Active Directory logs) and what specific anomaly or pattern to alert on.]
    - Use Case 2 (Log Source): [Provide a second, different detection logic targeting a different stage of the attack chain.]
    
    -------------------------------------------
    🔗 Source: [Insert Link here]
    
    """
    
    agent_executor.invoke({"messages": [("user", task)]})
    
    # Update and save history
    sent_items.append(top_alert.get('link'))
    save_history(sent_items)
    print("[SYSTEM] Alert processed and history updated.")

print("\n--- AI Agent Run Sequence Terminated ---")