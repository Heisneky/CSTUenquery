import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import mysql.connector

class ActionGetCourseInfo(Action):
    def name(self) -> Text:
        return "action_get_course_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # ดึง entity courseID จาก slot ที่ผู้ใช้ระบุ
        courseID = tracker.get_slot('courseID')


        # เชื่อมต่อฐานข้อมูล MySQL บน XAMPP
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cstu"
        )

        cursor = connection.cursor()

        # Query ข้อมูลวิชาจากฐานข้อมูล
        cursor.execute("SELECT courseName_TH FROM `courses-61` WHERE courseID_TH=%s", (courseID,))
        course_info = cursor.fetchone()

        # ตรวจสอบว่ามีข้อมูลหรือไม่
        if course_info:
            course_name = course_info[0]
            response = f"รหัสวิชา {courseID} คือวิชา {course_name}."
        else:
            response = f"ไม่พบข้อมูลสำหรับรหัสวิชา {courseID}"

        # ส่งคำตอบกลับให้ผู้ใช้
        dispatcher.utter_message(text=response)

        # ปิดการเชื่อมต่อฐานข้อมูล
        connection.close()

        return []