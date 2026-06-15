import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
import requests
import feedparser

# Load environment variables from the local .env file
load_dotenv()

# Retrieve credentials safely
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 1. Initialize the AI (Set temperature to 0 for deterministic, reliable output)
llm = ChatOllama(model="llama3.1", temperature=0)

# 2. STANDARD FUNCTION: Fetch data reliably via Python
def fetch_rss_threat_intel() -> str:
    """Standard Python function to fetch the latest threat data reliably."""
    try:
        print("[SYSTEM] Fetching live XML data from The Hacker News...")
        feed_url = "https://feeds.feedburner.com/TheHackersNews"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        response = requests.get(feed_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return "ERROR: Feed down."
            
        feed = feedparser.parse(response.content)
        if not feed.entries:
            return "ERROR: No news."
            
        top_alert = feed.entries[0]
        title = top_alert.get('title', 'No title')
        summary = top_alert.get('summary', top_alert.get('description', 'No summary'))
        link = top_alert.get('link', 'No link')
        
        return f"Title: {title}\nSummary: {summary}\nLink: {link}"
    except Exception as e:
        return f"ERROR: {str(e)}"

# 3. AI TOOL: Telegram Delivery via safe environment variables
@tool
def send_background_telegram(message_content: str) -> str:
    """Sends the finalized threat briefing to the user via Telegram."""
    
    # Validation step to ensure credentials loaded correctly
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[TELEGRAM] CRITICAL ERROR: Environment variables are missing or unreadable!")
        return "FAILED: Missing environment configuration."
    
    try:
        print(f"\n[AUTOMATION] Firing summary to Telegram...")
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message_content}
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("[TELEGRAM] Success! Message pushed to device.")
            return "SUCCESS: Message delivered."
        else:
            print(f"[TELEGRAM] Error Details: {response.text}")
            return f"FAILED. API said: {response.text}"
    except Exception as e:
        return f"FAILED to execute Telegram API: {str(e)}"

# Bind only the communication tool to the agent
tools = [send_background_telegram]
agent_executor = create_react_agent(llm, tools)

print("--- Activating Background Cybersecurity Agent ---")

# 4. EXECUTION: Fetch, context-inject, and run
latest_news = fetch_rss_threat_intel()

if "ERROR" in latest_news:
    print(f"Stopping execution due to fetch error: {latest_news}")
else:
    task = f"""
    You are an expert SOC Engineer and Threat Intelligence Analyst. 
    Analyze the following live threat data and compile a highly professional, beautiful, and actionable advisory:
    
    {latest_news}
    
    Your response MUST follow this exact layout, using clear emojis, bolding, and simple structural lines. Do not include any introductory filler text. Start directly with the alert.

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
    
    response = agent_executor.invoke({"messages": [("user", task)]})

print("\n--- AI Agent Run Sequence Terminated ---")