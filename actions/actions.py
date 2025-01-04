import requests
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
import mysql.connector
import re

class ActionFetchCoursePrerequisites(Action):
    def name(self) -> Text:
        return "action_fetch_course_Prerequisites"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # ดึง course_code จาก slot ที่ผู้ใช้ระบุ
        course_code = tracker.get_slot('course_code')

        # ใช้ print() เพื่อแสดงค่าของ course_code
        print(f"Received P course_code: {course_code}")

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
            cursor.execute("SELECT mustTaken FROM `courses-61` WHERE courseID_TH=%s", (course_code,))

            course_Prerequisites = cursor.fetchone()

            # ใช้ print() เพื่อตรวจสอบผลลัพธ์จาก query
            print(f"Database query result: {course_Prerequisites}")

            if course_Prerequisites:
                response = (
                    f"ถ้าคุณจะลงเรียนวิชา {course_code} ได้คุณต้องเคยศึกษาวิชา"
                    f"\n {course_Prerequisites[0]}\n"
                )

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

        # ล้างค่า slot หลังจากตอบคำถามเสร็จ
        # return [SlotSet("course_code", None)]
        return []
class ActionFetchCourseName(Action):
    def name(self) -> Text:
        return "action_fetch_course_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # ดึง course_code จาก slot ที่ผู้ใช้ระบุ
        course_code = tracker.get_slot('course_code')

        # ใช้ print() เพื่อแสดงค่าของ course_code ก่อน normalize
        print(f"Received course_code: {course_code}")

        if not course_code:
            dispatcher.utter_message(text="กรุณาระบุรหัสวิชาที่ถูกต้อง")
            return []

        # ขั้นตอนการ normalize course_code
        # 1. ลบช่องว่างที่ไม่จำเป็น
        # 2. แปลงรหัส เช่น กก111 -> กก.111 (ใส่ '.' หลังอักขระไทย 2 ตัวแรก ถ้ายังไม่มี)
        normalized_course_code = re.sub(r'\s+', '', course_code)  # ลบช่องว่าง
        if re.match(r'^[ก-ฮ]{2}\d+$', normalized_course_code):  # ตรวจสอบรูปแบบที่ยังไม่มีจุด
            normalized_course_code = f"{normalized_course_code[:2]}.{normalized_course_code[2:]}"

        # ใช้ print() เพื่อตรวจสอบค่า normalized_course_code
        print(f"Normalized course_code: {normalized_course_code}")

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
            cursor.execute("SELECT courseName_TH, courseDescrip_TH FROM `courses-61` WHERE courseID_TH=%s", (normalized_course_code,))

            course_name_and_description = cursor.fetchone()

            # ใช้ print() เพื่อตรวจสอบผลลัพธ์จาก query
            print(f"Database query result: {course_name_and_description}")

            if course_name_and_description:
                # course_name_and_description[0] คือ courseName_TH
                # course_name_and_description[1] คือ courseDescrip_TH
                response = (
                    f"ชื่อวิชาของ {normalized_course_code} คือ {course_name_and_description[0]} "
                    f"\nโดยจะมีเนื้อหาประมาณนี้ครับ:\n{course_name_and_description[1]}"
                )

            else:
                response = f"ไม่พบข้อมูลสำหรับรหัสวิชา {normalized_course_code}"

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

class ActionFetchCourseCredit(Action):
    def name(self) -> Text:
        return "action_fetch_course_credit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # ดึง course_code จาก slot ที่ผู้ใช้ระบุ
        course_code = tracker.get_slot('course_code')

        # ใช้ print() เพื่อแสดงค่าของ course_code
        print(f"Received C course_code: {course_code}")

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
            cursor.execute("SELECT courseUnit, courseHour FROM `courses-61` WHERE courseID_TH=%s", (course_code,))

            course_credit = cursor.fetchone()

            # ใช้ print() เพื่อตรวจสอบผลลัพธ์จาก query
            print(f"Database query result: {course_credit}")

            if course_credit:
                response = (
                    f"วิชา {course_code} มีหน่วยกิต {course_credit[0]} "
                )

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

class ActionFetchCoursePrerequisitesEN(Action):
    def name(self) -> Text:
        return "action_fetch_course_Prerequisites_en"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # ดึง course_code จาก slot ที่ผู้ใช้ระบุ
        course_code = tracker.get_slot('course_code_en')

        # ใช้ print() เพื่อแสดงค่าของ course_code
        print(f"Received EP course_code: {course_code}")

        if not course_code:
            dispatcher.utter_message(text="not correct course code")
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
            cursor.execute("SELECT mustTaken_EN FROM `courses-61` WHERE courseID_EN=%s", (course_code,))

            course_Prerequisites = cursor.fetchone()

            # ใช้ print() เพื่อตรวจสอบผลลัพธ์จาก query
            print(f"Database query result: {course_Prerequisites}")

            if course_Prerequisites:
                # course_name_and_description[0] คือ courseName_TH
                # course_name_and_description[1] คือ courseDescrip_TH
                response = (
                    f"If you going to enroll {course_code} you must completed"
                    f"\n {course_Prerequisites[0]}\n"
                )

            else:
                response = f"No data found for the course {course_code}"

            dispatcher.utter_message(text=response)

        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            dispatcher.utter_message(text="เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล")

        finally:
            # ปิดการเชื่อมต่อฐานข้อมูล
            if connection:
                connection.close()
                print("Database connection closed")

        # ล้างค่า slot หลังจากตอบคำถามเสร็จ
        # return [SlotSet("course_code", None)]
        return []
class ActionFetchCourseNameEN(Action):
    def name(self) -> Text:
        return "action_fetch_course_name_en"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # ดึง course_code จาก slot ที่ผู้ใช้ระบุ
        course_code = tracker.get_slot('course_code_en')

        # ใช้ print() เพื่อแสดงค่าของ course_code
        print(f"Received EN course_code: {course_code}")

        if not course_code:
            dispatcher.utter_message(text="not correct course code")
            return []

        course_code = course_code.upper()
        print(f"Normalized course_code: {course_code}")
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
            cursor.execute("SELECT courseName_EN, courseDescrip_EN FROM `courses-61` WHERE courseID_EN=%s", (course_code,))

            course_name_and_description = cursor.fetchone()

            # ใช้ print() เพื่อตรวจสอบผลลัพธ์จาก query
            print(f"Database query result: {course_name_and_description}")

            if course_name_and_description:
                # course_name_and_description[0] คือ courseName_EN
                # course_name_and_description[1] คือ courseDescrip_EN
                response = (
                    f"The course {course_code} is named {course_name_and_description[0]} "
                    f"\nIt covers the following content:\n{course_name_and_description[1]}"
                )

            else:
                response = f"No data found for the course {course_code}"

            dispatcher.utter_message(text=response)

        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            dispatcher.utter_message(text="เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล")

        finally:
            # ปิดการเชื่อมต่อฐานข้อมูล
            if connection:
                connection.close()
                print("Database connection closed")

        # ล้างค่า slot หลังจากตอบคำถามเสร็จ
        # return [SlotSet("course_code", None)]
        return []

class ActionFetchCourseCreditEN(Action):
    def name(self) -> Text:
        return "action_fetch_course_credit_en"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # ดึง course_code จาก slot ที่ผู้ใช้ระบุ
        course_code = tracker.get_slot('course_code_en')

        # ใช้ print() เพื่อแสดงค่าของ course_code
        print(f"Received C course_code: {course_code}")

        if not course_code:
            dispatcher.utter_message(text="not correct course code")
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
            cursor.execute("SELECT courseUnit, courseHour FROM `courses-61` WHERE courseID_EN=%s", (course_code,))

            course_Credit = cursor.fetchone()

            # ใช้ print() เพื่อตรวจสอบผลลัพธ์จาก query
            print(f"Database query result: {course_Credit}")

            if course_Credit:
                # course_Credit[0] คือ courseUnit
                # course_Credit[1] คือ courseHour
                response = (
                    f"The course {course_code} has Credit {course_Credit[0]} {course_Credit[1]}"
                )

            else:
                response = f"No data found for the course  {course_code}"

            dispatcher.utter_message(text=response)

        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            dispatcher.utter_message(text="เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล")

        finally:
            # ปิดการเชื่อมต่อฐานข้อมูล
            if connection:
                connection.close()
                print("Database connection closed")

        # ล้างค่า slot หลังจากตอบคำถามเสร็จ
        # return [SlotSet("course_code", None)]
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

# class ActionQueryTyphoon(Action):
#     def name(self):
#         return "action_query_typhoon"

#     def run(self, dispatcher, tracker, domain):
#         # รับข้อความจากผู้ใช้
#         user_message = tracker.latest_message.get("text")

#         # ระบุ path ของไฟล์ .gguf ที่ดาวน์โหลดมา
#         model_path = os.path.join(os.getcwd(), "./unsloth.Q4_K_M.gguf")  # ตรวจสอบ path ที่ถูกต้อง
#         print(f"Model path: {model_path}")  # ตรวจสอบ path

#         try:
#             # สร้างอินสแตนซ์ของ Llama และโหลดโมเดลจากไฟล์ .gguf
#             llm = Llama(model_path=model_path)  # ใช้ model_path ตรงๆ
            
#             # ใช้งานโมเดลเพื่อให้คำตอบ
#             response = llm(user_message)
#             print(f"Response: {response}")  # ตรวจสอบผลลัพธ์จากโมเดล
            
#             # ส่งข้อความตอบกลับ
#             dispatcher.utter_message(text=response['text'] if isinstance(response, dict) else str(response))
#         except Exception as e:
#             dispatcher.utter_message(text="Sorry, I couldn't process your request.")
#             print(f"Error during model inference: {e}")

#         return []