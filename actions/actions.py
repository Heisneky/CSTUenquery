import requests
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import mysql.connector

class ActionFetchCourseName(Action):
    def name(self) -> Text:
        return "action_fetch_course_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # ดึง course_code จาก slot ที่ผู้ใช้ระบุ
        course_code = tracker.get_slot('course_code')

        # ใช้ print() เพื่อแสดงค่าของ course_code
        print(f"Received course_code: {course_code}")

        if not course_code:
            dispatcher.utter_message(text="กรุณาระบุรหัสวิชาที่ถูกต้อง")
            return []

        # เชื่อมต่อฐานข้อมูล MySQL
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",  # ชื่อผู้ใช้ของคุณ
                password="",  # รหัสผ่านของคุณ
                database="cstu"
            )
            print("Database connection successful")

            cursor = connection.cursor()

            # Query เพื่อดึงชื่อวิชาจากรหัสวิชา
            cursor.execute("SELECT courseName_TH FROM `courses-61` WHERE courseID_TH=%s", (course_code,))
            course_name = cursor.fetchone()

            # ใช้ print() เพื่อตรวจสอบผลลัพธ์จาก query
            print(f"Database query result: {course_name}")

            if course_name:
                response = f"ชื่อวิชาของ {course_code} คือ {course_name[0]}"
            else:
                response = f"ไม่พบข้อมูลสำหรับรหัสวิชา {course_code}"

            dispatcher.utter_message(text=response)

        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            dispatcher.utter_message(text="เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล")

        finally:
            # ปิดการเชื่อมต่อฐานข้อมูล
            if connection:
                connection.close()
                print("Database connection closed")

        return []

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
