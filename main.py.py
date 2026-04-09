import flet as ft
import json
import os

# --- إعداد ملف الخزن الدائم (الطلب 5) ---
# هذا الملف راح ينحفظ بجانب الكود، ويخزن كل المهام للأبد بدون ما تنحذف
DB_FILE = "tasks_db.json"

def get_all_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_all_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- بداية التطبيق ---
def main(page: ft.Page):
    # الطلب 2: اسم التطبيق الرسمي
    page.title = "مهماتي"
    page.rtl = True
    page.theme_mode = "light"
    page.padding = 0
    page.spacing = 0

    # دالة لجلب المهام من الملف للغرفة المحددة
    def load_tasks(room_name):
        data = get_all_data()
        return data.get(room_name, [])

    # دالة لحفظ المهام في الملف للغرفة المحددة
    def save_tasks(room_name, tasks):
        data = get_all_data()
        data[room_name] = tasks
        save_all_data(data)

    # منطقة المحتوى (الجهة اليسرى)
    content_area = ft.Container(
        expand=True,
        padding=40,
        bgcolor="#ffffff",
        content=ft.Column([
            # الطلب 1: العبارة الترحيبية الجديدة
            ft.Text("أهلاً و سهلاً في مهماتي", size=30, weight="bold"),
            ft.Text("اختر قسماً من القائمة الجانبية للبدء.", size=16, color="grey"),
        ], alignment="center", horizontal_alignment="center")
    )

    # دالة تغيير محتوى الصفحة (الغرف)
    def change_view(name, color):
        # تحميل مهام الغرفة
        current_tasks = load_tasks(name)

        # الطلب 7: خاصية تحديد الوقت + حقل المهمة
        task_input = ft.TextField(label="اكتب المهمة هنا...", expand=True, border_radius=10)
        time_input = ft.TextField(label="الوقت (مثال: 10:30 ص)", width=170, border_radius=10)
        
        tasks_list_view = ft.Column(scroll="auto", expand=True)

        # دالة تحديث الشاشة
        def update_ui():
            tasks_list_view.controls.clear()
            for index, task in enumerate(current_tasks):
                # الطلب 4: إضافة زر لحذف المهمة
                def create_delete_btn(i):
                    return ft.ElevatedButton("حذف", bgcolor="#e74c3c", color="white", on_click=lambda e: delete_task(i))
                
                row = ft.Row([
                    ft.Checkbox(label=f"{task['title']} - (الوقت: {task['time']})", value=task.get('done', False)),
                    create_delete_btn(index)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                tasks_list_view.controls.append(row)
            page.update()

        # الطلب 3: تصليح إضافة المهمة
        def add_task(e):
            if task_input.value != "":
                new_task = {
                    "title": task_input.value,
                    "time": time_input.value if time_input.value != "" else "غير محدد",
                    "done": False
                }
                current_tasks.append(new_task)
                save_tasks(name, current_tasks) # الخزن الدائم
                task_input.value = "" # تفريغ الحقل
                time_input.value = ""
                update_ui()

        # دالة الحذف
        def delete_task(index):
            current_tasks.pop(index)
            save_tasks(name, current_tasks)
            update_ui()

        update_ui()

        # الطلب 9: داخل غرفة الطالب ضيف غرف فرعية
        if name == "غرفة الطلاب":
            content_area.content = ft.Column([
                ft.Text("غرفة الطلاب", size=28, weight="bold", color=color),
                ft.Text("اختر إحدى الغرف الفرعية:", size=16, color="grey"),
                ft.Divider(height=20),
                ft.Row([
                    ft.ElevatedButton("غرفة الامتحانات", bgcolor="red", color="white", on_click=lambda _: change_view("الامتحانات", "red")),
                    ft.ElevatedButton("غرفة المحاضرات", bgcolor="green", color="white", on_click=lambda _: change_view("المحاضرات", "green")),
                    ft.ElevatedButton("غرفة الواجبات اليومية", bgcolor="blue", color="white", on_click=lambda _: change_view("الواجبات", "blue")),
                ], spacing=20)
            ])
        else:
            # شكل الغرف الاعتيادية
            content_area.content = ft.Column([
                ft.Text(f"قسم: {name}", size=28, weight="bold", color=color),
                ft.Divider(height=20),
                ft.Row([
                    task_input, 
                    time_input, 
                    ft.ElevatedButton("إضافة المهمة", bgcolor=color, color="white", on_click=add_task)
                ]),
                ft.Container(height=20),
                ft.Text("المهام الحالية:", weight="bold", size=18),
                tasks_list_view
            ])
        page.update()

    # زر القائمة
    def menu_button(text, color):
        return ft.Container(
            content=ft.Text(text, color="white", weight="bold", size=16),
            padding=15,
            on_click=lambda _: change_view(text, color),
            ink=True,
        )

    # القائمة الجانبية
    sidebar = ft.Container(
        width=250,
        bgcolor="#2c3e50",
        padding=20,
        content=ft.Column([
            ft.Text("لوحة التحكم", color="white", size=22, weight="bold"),
            ft.Divider(color="white24"),
            # الطلب 6: ترتيب القائمة اليمنى (الطالب أول وحدة)
            menu_button("غرفة الطلاب", "teal"),
            menu_button("غرفة العميد", "blue"),
            menu_button("غرفة الموظفين", "bluegrey"),
            menu_button("الغرفة العائلية", "purple"),
        ], spacing=10)
    )

    page.add(ft.Row([sidebar, content_area], expand=True, spacing=0))

ft.app(target=main)