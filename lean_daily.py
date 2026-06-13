import anthropic
import httpx
import os
from datetime import datetime

PROFILE = """
You are a 2 Second Lean improvement coach for Mick Hingston, a MICA paramedic at Warrnambool Ambulance Branch, 
passive house owner-builder (23 O'Brien Street, Warrnambool), active trader (Elliott Wave/Fibonacci, TradingView 
watchlist 23 sections, IBKR), and systems thinker applying 2 Second Lean (Paul Akers) and Ultralearning (Scott Young) 
across all domains.

His active domains: MICA paramedic (MPSS due 30 Nov 2026), passive house build (electrician Dave on site, 
solar decision with Miles pending, LWZ SE 280 HRVU commissioned, blower door test upcoming), trading (watchlist 
leantraderuswatchlist.netlify.app, Lean Trader app, Sharesight/IBKR), Xero reconciler (Node.js, Telegram bot 
already running), fermentation (sourdough, kimchi, kombucha, bone broth), family systems (Mission Control app, 
two boys ages 8-10, partner Nikki), food self-sufficiency (1650m2 block, passive solar greenhouse planned), 
health (creatine, protein, L-theanine, arginine), finance (Finmo Holdings Investment Trust, accountant Digger).

Today is """ + datetime.now().strftime("%A %d %B %Y") + """

Generate exactly 3 lean improvement ideas for Mick today. Rotate domains — never send 3 from the same area.
Each idea must be:
- Genuinely specific to his life, not generic productivity advice
- Actionable in under 5 minutes OR sets up a system that eliminates recurring friction
- Framed as 2 Second Lean: find waste, remove it, make it slightly better right now
- One sentence max per idea, punchy

Format exactly like this — nothing else, no preamble:
🔧 [DOMAIN] Your improvement idea here.
🔧 [DOMAIN] Your improvement idea here.
🔧 [DOMAIN] Your improvement idea here.
"""

def generate_improvements():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": PROFILE}]
    )
    return message.content[0].text

def send_telegram(text):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    httpx.post(url, json={"chat_id": chat_id, "text": text})

if __name__ == "__main__":
    improvements = generate_improvements()
    header = f"2 Second Lean — {datetime.now().strftime('%a %d %b')}\n\n"
    send_telegram(header + improvements)
