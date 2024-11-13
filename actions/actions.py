from rasa_sdk import Action
import requests
import json

class ActionQueryTyphoon(Action):
    def name(self):
        return "action_query_typhoon"

    def run(self, dispatcher, tracker, domain):
        # รับข้อความจากผู้ใช้
        user_message = tracker.latest_message.get("text")

        # กำหนด API endpoint และ API key
        api_url = "https://api.opentyphoon.ai/v1/chat/completions"
        api_key = "sk-EmdY1GfsArekFLaLqWZlPcTiGsKnAub0PAqkjiRZhXhykLOZ"

        # ข้อมูลที่ส่งไปยัง Typhoon API
        payload = {
            "model": "typhoon-v1.5x-70b-instruct",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. You must answer only in Thai."},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 512,
            "temperature": 0.6,
            "top_p": 0.95,
            "repetition_penalty": 1.05,
            "stream": False
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        try:
            # ส่งคำถามไปยัง Typhoon API
            response = requests.post(api_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # ตรวจสอบข้อผิดพลาด HTTP

            # ตรวจสอบการตอบกลับ
            if response.status_code == 200:
                response_data = response.json()
                answer = response_data['choices'][0]['message']['content']
                dispatcher.utter_message(text=answer)
            else:
                dispatcher.utter_message(text=f"เกิดข้อผิดพลาด: รหัสสถานะ {response.status_code} - {response.text}")
        except requests.exceptions.HTTPError as http_err:
            dispatcher.utter_message(text=f"HTTP Error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            dispatcher.utter_message(text=f"ข้อผิดพลาดในการเชื่อมต่อ: {req_err}")
        except Exception as err:
            dispatcher.utter_message(text=f"เกิดข้อผิดพลาดบางประการ: {err}")

        return []
