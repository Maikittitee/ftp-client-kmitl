จงเขียนโปรแกรมด้วยภาษา Pythonเพื่อพัฒนาโปรแกรมที่เลียนแบบค าสั่ง ftp ในระบบปฏิบัติการ Windowsโดยใช้ socketlibrary ในภาษา Python (ห้ามใช้ library ส าหรับ FTP ส าเร็จรูปอื่นใดนอกจากการใช้ socket library)โปรแกรมดังกล่าวจะต้องสามารถเลียบแบบลักษณะการท างานและค าสั่งของโปแกรม ftp ในระบบปฏิบัติการ Windows ต่อไปนี้•โครงสร้างหลักของโปรแกรมสามารถท างานแบบ Read-Evaluate-Print-Loop (REPL) และรับค าสั่งได้ (4คะแนน)

•ascii(2 คะแนน)
•binary(2 คะแนน)
•bye(1 คะแนน)
•cd(2 คะแนน)
•close(1 คะแนน)
•delete(2 คะแนน)
•disconnect(1 คะแนน)
•get(2 คะแนน)
•ls(2 คะแนน)
•open(2 คะแนน)
•put(2 คะแนน)
•pwd(2 คะแนน)
•quit(1 คะแนน)
•rename(2 คะแนน)
•user(2 คะแนน)

addictional

- file ที่ get มาจะอยู่ใน root directory ของ project นี้นะครับ (directory เดียวกับ main.py) แทนที่จะอยู่ใน usr/home
- บาง output จะเป็น format ของ macOS นะครับ เนื่องจากหา resource ของ window ได้จำกัด แล้วแก้ได้แค่นี้
- ไม่ได้ protect พวก case wrong input หลายๆเคส เนื่องจากเชื่อว่าจุดมุ่งหมายของงานนี้คือการเรียนรู้วิธีการเขียน socket programming จึงไม่ได้ดักบางเคส
- ใช้ Python 3.11.7 ในการทำนะครับ 


