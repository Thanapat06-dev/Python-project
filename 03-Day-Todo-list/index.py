import os # ใช้สำหรับตรวจสอบว่ามีไฟล์อยู่จริงไหม

FILE_NAME = "tasks.txt"

def load_tasks():
    """" ฟังก์ชันสำหรับการอ่านไฟล์ตอนเริ่มโปรแกรม """
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readline()]
    return [] # ส่งค่า List ป่าว ถ้าไม่มีไฟล์

def save_tasks(tasks):
    """ ฟังก์ชันสำหรับ save ไฟล์ """
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for task in tasks:
            f.write(task + "\n")

# --- เริ่มต้นโปรแกรม ---
tasks = load_tasks()

while True:
    print("\n --- To-Do List (Auto-Save) ---")
    print(f"Current tasks: {len(tasks)}")
    print("Menu: 1. Add 2. Remove 3. Show 4. Exit")

    choice = input("Select: ")

    if choice == "1":
        new_task = input("Enter yout task: ")
        tasks.append(new_task)
        save_tasks(tasks)
        print("Saved!")

    elif choice == "2":
        try:
            idx = int(input("Number to remove: ")) - 1
            tasks.pop(idx)
            save_tasks(tasks)
            print("Removed and Updated!")
        except:
            print("Error!")

    elif choice == "3":
        for i, t in enumerate(tasks, start= 1):
            print(f"{i}. {t}")

    elif choice == "4":
        break

    else:
        print("Invalid select menu!")