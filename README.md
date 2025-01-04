# CSTU enquery Chatbot

# บทคัดย่อ

# bot cut yor

# ขั้นตอนการติดตั้ง และเปิดใช้งาน

## 1. ฝึกโมเดลเพื่อเตรียมนำไปใช้
หลังจากได้ดาวโหลดโปรแกรมมาบนคอมพิวเตอร์แล้ว ให้เข้าไปที่โฟลเดอร์ CSTUenquery

```
cd CSTUenquery
```
ให้ทำการฝึกโมเดลก่อนโดยพิมคำสั่ง
```
 rasa train
```
ขั้นตอนนี้อาจใช้เวลาสักพัก

## 2. นำเข้าฐานข้อมูล
นำเข้าไฟล์ CSTU.sql ไปที่โปรแกรมจัดการฐานข้อมูลตามที่ถนัด


## 3. เริ่มต้นใช้งาน
ให้เปิด command prompt ขึ้นมา 4 ตัวเพื่อเปิดใช้งานฟีเจอร์ต่างๆของโปรแกรมนี้

### command prompt 1 
เริ่มต้นการทำงานของโปรแกรมด้วยคำสั่ง
```
rasa run --enable-api
```


### command prompt 2
รันคำสั่ง เพื่อเริ่มต้นใช้งาน webhook
```
python .\line_connector.py
```


### command prompt 3
รันคำสั่ง เพื่อใช้งานความสามารถในการตอบคำถาม
```
rasa run actions
```
แก้ไขส่วนต่อไปนี้หากมีการเปลี่ยนแปลงรายละเอียดฐานข้อมูล ใน ```CSTUenquery\actions\actions.py```
```
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",  # ชื่อผู้ใช้ของคุณ
                password="",  # รหัสผ่านของคุณ
                database="cstu"
            )
            print("Database connection successful")
```

### command prompt 4
รันคำสั่ง เพื่อให้คอมพิวเตอร์เป็นโฮสต์
```
ngrok http 5000
```
หลังจากรันคำสั่งนี้แล้วให้หาบรรทัดนี้
```
Forwarding                    https://e150-49-228-125-24.ngrok-free.app -> http://localhost:5000
```
คำลอกส่วน https มานำไปใช้เป็น webhook ในรูปแบบนี้

ตัวอย่าง
> https://e150-49-228-125-24.ngrok-free.app/webhook

และแก้ webhook URL บน line developer ทุกครั้งที่มีการเปิดใช้งานใหม่

