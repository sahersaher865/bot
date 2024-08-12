import os
import time
import psutil

def is_running(script_name):
    # التحقق مما إذا كان الملف قيد التشغيل من خلال البحث عن الاسم
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if script_name in process.info['cmdline']:
            return True
    return False

def check_and_restart():
    while True:
        if not is_running("App.py"):
            print("App.py توقف. يتم إعادة تشغيله الآن...")
            os.system("python3 App.py")
        
        time.sleep(10)  # تحقق كل 10 ثوانٍ

if __name__ == "__main__":
    check_and_restart()
