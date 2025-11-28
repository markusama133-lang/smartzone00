import customtkinter as ctk
from tkinter import messagebox
from database_manager import DatabaseManager

# إعدادات المظهر
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AdminDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # إعدادات النافذة
        self.title("SmartZone Admin Panel")
        self.geometry("900x700") # قمت بزيادة الطول لاستيعاب الحقل الجديد
        self.resizable(False, False)

        # الاتصال بقاعدة البيانات
        self.db_config = {
            'user': 'root',
            'password': '',  # تأكد من كلمة المرور الخاصة بك
            'host': '127.0.0.1',
            'database': 'smartzone_db'
        }
        self.db = DatabaseManager(self.db_config)

        # تقسيم الواجهة
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- القائمة الجانبية ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="SmartZone\nAdmin", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_add = ctk.CTkButton(self.sidebar, text="إضافة موبايل", command=self.show_add_frame)
        self.btn_add.grid(row=1, column=0, padx=20, pady=10)

        self.btn_manage = ctk.CTkButton(self.sidebar, text="إدارة الموبايلات", command=self.show_manage_frame)
        self.btn_manage.grid(row=2, column=0, padx=20, pady=10)

        # --- الإطارات الرئيسية ---
        self.add_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.manage_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent", label_text="قائمة الهواتف")

        # بناء محتويات الإطارات
        self.setup_add_interface()
        
        # تشغيل الافتراضي
        self.show_add_frame()

    def show_add_frame(self):
        self.manage_frame.grid_forget()
        self.add_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_manage_frame(self):
        self.add_frame.grid_forget()
        self.manage_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.load_phones_list()

    def setup_add_interface(self):
        # عنوان
        title = ctk.CTkLabel(self.add_frame, text="إضافة هاتف جديد", font=("Arial", 20))
        title.pack(pady=15)

        # حاوية تمرير (Scrollable Frame)
        self.input_scroll = ctk.CTkScrollableFrame(self.add_frame, fg_color="transparent", width=600)
        self.input_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # حقول الإدخال الأساسية
        self.entry_model = ctk.CTkEntry(self.input_scroll, placeholder_text="اسم الموديل (مثال: Galaxy S24)")
        self.entry_model.pack(pady=8, fill="x", padx=20)

        # قائمة الشركات
        brands = self.db.get_all_brands()
        brand_names = [b['brand_name'] for b in brands] if brands else ["Other"]
        self.combo_brand = ctk.CTkComboBox(self.input_scroll, values=brand_names)
        self.combo_brand.pack(pady=8, fill="x", padx=20)
        self.combo_brand.set("اختر الشركة")

        self.entry_price = ctk.CTkEntry(self.input_scroll, placeholder_text="السعر (EGP)")
        self.entry_price.pack(pady=8, fill="x", padx=20)

        self.entry_img = ctk.CTkEntry(self.input_scroll, placeholder_text="رابط الصورة (URL)")
        self.entry_img.pack(pady=8, fill="x", padx=20)

        # --- قسم المواصفات ---
        ctk.CTkLabel(self.input_scroll, text="المواصفات الفنية", font=("Arial", 14, "bold")).pack(pady=(15, 5), anchor="w", padx=20)

        # === 1. إضافة حقل الشاشة الجديد ===
        self.entry_screen = ctk.CTkEntry(self.input_scroll, placeholder_text="حجم الشاشة (مثال: 6.8 inches)")
        self.entry_screen.pack(pady=5, fill="x", padx=20)
        # ================================

        self.entry_ram = ctk.CTkEntry(self.input_scroll, placeholder_text="الرام (مثال: 12 GB)")
        self.entry_ram.pack(pady=5, fill="x", padx=20)

        self.entry_storage = ctk.CTkEntry(self.input_scroll, placeholder_text="المساحة (مثال: 256 GB)")
        self.entry_storage.pack(pady=5, fill="x", padx=20)
        
        self.entry_battery = ctk.CTkEntry(self.input_scroll, placeholder_text="البطارية (مثال: 5000 mAh)")
        self.entry_battery.pack(pady=5, fill="x", padx=20)

        self.entry_camera = ctk.CTkEntry(self.input_scroll, placeholder_text="الكاميرا الأساسية (مثال: 200 MP)")
        self.entry_camera.pack(pady=5, fill="x", padx=20)

        self.entry_chipset = ctk.CTkEntry(self.input_scroll, placeholder_text="المعالج (مثال: Snapdragon 8 Gen 3)")
        self.entry_chipset.pack(pady=5, fill="x", padx=20)

        # زر الحفظ
        btn_save = ctk.CTkButton(self.input_scroll, text="حفظ البيانات", command=self.save_phone, fg_color="green", height=40)
        btn_save.pack(pady=20)

    def save_phone(self):
        model = self.entry_model.get()
        brand_name = self.combo_brand.get()
        price = self.entry_price.get()
        img = self.entry_img.get()
        
        if not model or brand_name == "اختر الشركة":
            messagebox.showerror("خطأ", "يرجى ملء اسم الموديل واختيار الشركة")
            return

        # 1. البحث عن ID الشركة
        brand_id = self.db.find_or_create_brand(brand_name)

        # 2. تجهيز المواصفات (تمت إضافة الشاشة هنا)
        specs = [
            # === ربط الشاشة بقاعدة البيانات ===
            {"category": "Display", "name": "Screen Size", "value": self.entry_screen.get()},
            # =================================
            {"category": "Performance", "name": "RAM", "value": self.entry_ram.get()},
            {"category": "Storage", "name": "Internal", "value": self.entry_storage.get()},
            {"category": "Battery", "name": "Capacity", "value": self.entry_battery.get()},
            {"category": "Camera", "name": "Main Camera", "value": self.entry_camera.get()},
            {"category": "Platform", "name": "Chipset", "value": self.entry_chipset.get()}
        ]

        # 3. الحفظ في قاعدة البيانات
        result = self.db.add_phone(
            model_name=model,
            brand_id=brand_id,
            release_date="2024-01-01", 
            specs_list=specs,
            price=float(price) if price else 0.0,
            image_url=img
        )

        if result:
            messagebox.showinfo("نجاح", f"تم إضافة {model} بنجاح!")
            self.clear_inputs()
        else:
            messagebox.showerror("فشل", "حدث خطأ أثناء الحفظ بقاعدة البيانات")

    def clear_inputs(self):
        self.entry_model.delete(0, 'end')
        self.entry_price.delete(0, 'end')
        self.entry_img.delete(0, 'end')
        
        # تنظيف حقل الشاشة
        self.entry_screen.delete(0, 'end')
        
        self.entry_ram.delete(0, 'end')
        self.entry_storage.delete(0, 'end')
        self.entry_battery.delete(0, 'end')
        self.entry_camera.delete(0, 'end')
        self.entry_chipset.delete(0, 'end')

    def load_phones_list(self):
        # تنظيف القائمة القديمة
        for widget in self.manage_frame.winfo_children():
            widget.destroy()

        phones = self.db.get_all_phones()
        if not phones:
            ctk.CTkLabel(self.manage_frame, text="لا توجد هواتف مسجلة").pack(pady=20)
            return

        for p in phones:
            row = ctk.CTkFrame(self.manage_frame)
            row.pack(fill="x", pady=5, padx=10)

            name_lbl = ctk.CTkLabel(row, text=f"{p['brand_name']} {p['model_name']}", anchor="w")
            name_lbl.pack(side="left", padx=10)

            del_btn = ctk.CTkButton(row, text="حذف", width=60, fg_color="red", 
                                  command=lambda pid=p['phone_id']: self.delete_phone(pid))
            del_btn.pack(side="right", padx=10, pady=5)

    def delete_phone(self, phone_id):
        if messagebox.askyesno("تأكيد", "هل أنت متأكد من حذف هذا الهاتف؟"):
            self.db.delete_phone(phone_id)
            self.load_phones_list() 

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()