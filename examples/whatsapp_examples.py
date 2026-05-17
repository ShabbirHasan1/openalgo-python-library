"""
OpenAlgo WhatsApp Notification API Examples

This file demonstrates how to use the WhatsApp notification API to send
text, image, and document alerts via your OpenAlgo paired WhatsApp device.

Prerequisites:
1. WhatsApp device must be paired in OpenAlgo (open /whatsapp in the web UI,
   click Pair, scan the QR with your phone).
2. The bot auto-reconnects on every server boot from the encrypted session
   blob stored in openalgo.db. No further action needed.
3. The OpenAlgo API key must be active.

Notes:
- WhatsApp is single-user per deployment. The paired device IS the operator.
- Pairing is admin-only via the /whatsapp web UI; the REST API exposes only
  the send endpoint (security: a leaked API key cannot re-pair the device).
- A 5-recipient cap applies to broadcast lists — bulk-messaging patterns
  can get the paired device unlinked by Meta.
"""

import openalgo

# Initialize the API client
api = openalgo.api(
    api_key="your_api_key_here",
    host="http://127.0.0.1:5000",
)

# Replace with one of your contacts' E.164 numbers when testing
PHONE = "919876543210"

print("=" * 80)
print("OpenAlgo WhatsApp Notification API Examples")
print("=" * 80)

# ============================================================================
# Example 1: Send to yourself (the simplest case)
# ============================================================================
print("\n1. Self-send (no recipient args -> the paired device's own number)")
print("-" * 80)

result = api.whatsapp("Build #482 deployed. P&L today: +1.2%")
if result.get('status') == 'success':
    print("Delivered.", result.get('data'))
else:
    print("Error:", result.get('message'))

# ============================================================================
# Example 2: Send to a single phone number
# ============================================================================
print("\n2. Send to one number")
print("-" * 80)

result = api.whatsapp(
    "Are you free for a quick call about the BANKNIFTY 48000 CE trade?",
    to=PHONE,
)
print(result)

# ============================================================================
# Example 3: Small broadcast (max 5 recipients)
# ============================================================================
print("\n3. Broadcast to a small list (capped at 5 server-side)")
print("-" * 80)

result = api.whatsapp(
    "Server maintenance window starting in 10 minutes. Strategies will be paused.",
    to=["919876543210", "919812345678", "919900112233"],
)
print(result)

# ============================================================================
# Example 4: Send an image (e.g. an EOD chart)
# ============================================================================
print("\n4. Image with caption")
print("-" * 80)

# Path is read from the OpenAlgo server's filesystem. It must lie under
# WHATSAPP_ATTACHMENT_ROOTS (defaults to <openalgo>/db/attachments/).
result = api.whatsapp(
    to=PHONE,
    image="/srv/charts/nifty_eod.png",
    caption="NIFTY end-of-day chart",
)
print(result)

# ============================================================================
# Example 5: Send a document (e.g. a daily report PDF)
# ============================================================================
print("\n5. Document attachment")
print("-" * 80)

result = api.whatsapp(
    "Daily P&L report attached.",
    to=PHONE,
    document="/srv/reports/2026-05-17.pdf",
    filename="DailyPnL_2026-05-17.pdf",
)
print(result)

# ============================================================================
# Example 6: Trade signal — multi-line message to self
# ============================================================================
print("\n6. Trade signal alert to self")
print("-" * 80)

signal = (
    "BUY Signal: RSI oversold on NIFTY 24000 CE\n"
    "Entry: 145.50\n"
    "Target: 165.00\n"
    "SL: 138.00"
)
result = api.whatsapp(signal)
print(result)

# ============================================================================
# Example 7: Stop-loss hit — fire-and-forget
# ============================================================================
print("\n7. Fire-and-forget (don't wait for delivery)")
print("-" * 80)

# When you don't need the per-recipient delivery report — useful inside hot
# strategy loops where every millisecond matters. Server still queues to its
# alert pool and dispatches via the bot worker thread.
result = api.whatsapp(
    "Stop-loss hit on BANKNIFTY position. Position closed.",
    wait_for_delivery=False,
)
print(result)

# ============================================================================
# Example 8: Daily summary
# ============================================================================
print("\n8. Daily trading summary to self")
print("-" * 80)

summary = (
    "Daily Trading Summary\n"
    "Winning Trades: 8\n"
    "Losing Trades: 2\n"
    "Net P&L: +15,450\n"
    "Win Rate: 80%\n\n"
    "Great day."
)
result = api.whatsapp(summary)
print(result)

# ============================================================================
# Example 9: Send to a linked OpenAlgo username (if you maintain a
#            multi-recipient deployment with linked users)
# ============================================================================
print("\n9. Send to a linked OpenAlgo user (legacy multi-recipient path)")
print("-" * 80)

result = api.whatsapp(
    "Position update: BANKNIFTY 48000 CE now at +21% P&L.",
    username="alice",
)
print(result)

# ============================================================================
# Example 10: Conditional inside a strategy
# ============================================================================
print("\n10. Conditional inside a trading loop")
print("-" * 80)

current_price = 24150
target_price = 24100
symbol = "NIFTY"

if current_price >= target_price:
    result = api.whatsapp(
        f"{symbol} reached target price: {current_price}",
    )
    if result.get('status') == 'success':
        print("Target alert sent.")
    else:
        print("Error:", result.get('message'))
else:
    print(f"Price {current_price} has not crossed target {target_price} yet.")

print("\n" + "=" * 80)
print("Examples complete.")
print("=" * 80)
print()
print("Receiving messages: type slash-commands from your own phone in the")
print('"Message yourself" chat (e.g. /orderbook, /positions, /quote RELIANCE NSE).')
print("The bot only responds to messages where is_from_me=True, so random")
print("contacts who message you cannot drive it.")
