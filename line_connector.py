from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# LINE Messaging API Configuration
CHANNEL_ACCESS_TOKEN = "6dAOE20/9L71J4Nmy9IMGm79OB2fbd3esw7ZWMR7yDe2y5uKEa+oliq/JUk0lhHPUZfKtkq2xzcPadoZsGXP+o5stqyJyE6pvBQNFGYT0QsU0pYH8C6mY8r0zMua3LmzwQ1oPgPA9ILSvgJ/azASSgdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "3217c9cdfc78a6f1a9b9cbf15a5088b9"
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        body = request.json
        for event in body.get("events", []):
            if event["type"] == "message" and event["message"]["type"] == "text":
                user_message = event["message"]["text"]
                reply_token = event["replyToken"]

                # ส่งข้อความไปยัง Rasa REST API
                response = requests.post(
                    RASA_URL,
                    json={"sender": event["source"]["userId"], "message": user_message},
                )
                
                # Debug response จาก Rasa
                print(f"Rasa response: {response.json()}")

                if response.status_code == 200:
                    rasa_response = response.json()
                    if rasa_response and isinstance(rasa_response, list) and "text" in rasa_response[0]:
                        rasa_reply = rasa_response[0].get("text", "ไม่สามารถตอบกลับได้")
                    else:
                        rasa_reply = "ไม่มีการตอบกลับจาก Rasa"
                    reply_to_line(reply_token, rasa_reply)
                else:
                    reply_to_line(reply_token, "เกิดข้อผิดพลาดในการประมวลผล")
        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

def reply_to_line(reply_token, message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
    }
    body = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": message}],
    }
    response = requests.post(
        "https://api.line.me/v2/bot/message/reply", headers=headers, json=body
    )
    print(f"LINE API response: {response.status_code}, {response.text}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
