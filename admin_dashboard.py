import customtkinter as ctk
from tkinter import messagebox, filedialog
from database_manager import DatabaseManager
import pandas as pd  # <-- مكتبة التعامل مع الإكسيل
import os

# إعدادات المظهر
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AdminDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # إعدادات النافذة
        self.title("SmartZone Admin Panel")
        self.geometry("1000x750")
        self.resizable(False, False)

        self.current_edit_id = None 

        # الاتصال بقاعدة البيانات
        self.db_config = {
            'user': 'root',
            'password': '',  
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

        self.btn_add = ctk.CTkButton(self.sidebar, text="إضافة موبايل", command=self.reset_and_show_add)
        self.btn_add.grid(row=1, column=0, padx=20, pady=10)

        self.btn_manage = ctk.CTkButton(self.sidebar, text="إدارة الموبايلات", command=self.show_manage_frame)
        self.btn_manage.grid(row=2, column=0, padx=20, pady=10)
        
        # زر استيراد Excel (تم التعديل)
        self.btn_excel = ctk.CTkButton(self.sidebar, text="استيراد Excel", command=self.import_excel_file, fg_color="#107c10", hover_color="#0b550b")
        self.btn_excel.grid(row=3, column=0, padx=20, pady=10)

        self.btn_refresh = ctk.CTkButton(self.sidebar, text="تحديث البيانات", fg_color="gray", command=self.refresh_data)
        self.btn_refresh.grid(row=4, column=0, padx=20, pady=10)

        # --- الإطارات الرئيسية ---
        self.add_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.manage_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent", label_text="قائمة الهواتف")

        self.setup_add_interface()
        self.reset_and_show_add()

    def refresh_data(self):
        brands = self.db.get_all_brands()
        brand_names = [b['brand_name'] for b in brands] if brands else ["Other"]
        self.combo_brand.configure(values=brand_names)
        
        if self.manage_frame.winfo_ismapped():
            self.load_phones_list()
        
        messagebox.showinfo("تم", "تم تحديث البيانات بنجاح")

    def reset_and_show_add(self):
        self.current_edit_id = None
        self.save_btn.configure(text="حفظ البيانات", fg_color="green")
        self.title_lbl.configure(text="إضافة هاتف جديد")
        self.clear_inputs()
        self.show_add_frame()

    def show_add_frame(self):
        self.manage_frame.grid_forget()
        self.add_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_manage_frame(self):
        self.add_frame.grid_forget()
        self.manage_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.load_phones_list()

    def setup_add_interface(self):
        self.title_lbl = ctk.CTkLabel(self.add_frame, text="إضافة هاتف جديد", font=("Arial", 20))
        self.title_lbl.pack(pady=15)

        self.input_scroll = ctk.CTkScrollableFrame(self.add_frame, fg_color="transparent", width=600)
        self.input_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_label_entry("اسم الموديل:", "Galaxy S24", "entry_model")
        
        ctk.CTkLabel(self.input_scroll, text="الشركة المصنعة:", anchor="w").pack(pady=2, fill="x", padx=20)
        brands = self.db.get_all_brands()
        brand_names = [b['brand_name'] for b in brands] if brands else ["Other"]
        self.combo_brand = ctk.CTkComboBox(self.input_scroll, values=brand_names)
        self.combo_brand.pack(pady=5, fill="x", padx=20)
        self.combo_brand.set("اختر الشركة")

        self.create_label_entry("السعر (EGP):", "40000", "entry_price")
        self.create_label_entry("رابط الصورة (URL):", "https://...", "entry_img")

        ctk.CTkLabel(self.input_scroll, text="المواصفات الفنية", font=("Arial", 16, "bold"), text_color="#3b82f6").pack(pady=(20, 10), anchor="w", padx=20)

        self.create_label_entry("حجم الشاشة (Screen Size):", "6.8 inches", "entry_screen")
        self.create_label_entry("الرام (RAM):", "12 GB", "entry_ram")
        self.create_label_entry("المساحة (Storage):", "256 GB", "entry_storage")
        self.create_label_entry("البطارية (Battery):", "5000 mAh", "entry_battery")
        self.create_label_entry("الكاميرا (Main Camera):", "200 MP", "entry_camera")
        self.create_label_entry("المعالج (Chipset):", "Snapdragon 8 Gen 3", "entry_chipset")

        self.save_btn = ctk.CTkButton(self.input_scroll, text="حفظ البيانات", command=self.save_phone, fg_color="green", height=40)
        self.save_btn.pack(pady=30)

    def create_label_entry(self, label_text, placeholder, attr_name):
        lbl = ctk.CTkLabel(self.input_scroll, text=label_text, anchor="w")
        lbl.pack(pady=(5, 0), fill="x", padx=20)
        entry = ctk.CTkEntry(self.input_scroll, placeholder_text=placeholder)
        entry.pack(pady=(0, 10), fill="x", padx=20)
        setattr(self, attr_name, entry)

    def save_phone(self):
        model = self.entry_model.get()
        brand_name = self.combo_brand.get()
        price = self.entry_price.get()
        img = self.entry_img.get()
        
        if not model or brand_name == "اختر الشركة":
            messagebox.showerror("خطأ", "يرجى ملء اسم الموديل واختيار الشركة")
            return

        brand_id = self.db.find_or_create_brand(brand_name)

        specs = [
            {"category": "Display", "name": "Screen Size", "value": self.entry_screen.get()},
            {"category": "Performance", "name": "RAM", "value": self.entry_ram.get()},
            {"category": "Storage", "name": "Internal", "value": self.entry_storage.get()},
            {"category": "Battery", "name": "Capacity", "value": self.entry_battery.get()},
            {"category": "Camera", "name": "Main Camera", "value": self.entry_camera.get()},
            {"category": "Platform", "name": "Chipset", "value": self.entry_chipset.get()}
        ]

        if self.current_edit_id:
            success = self.db.update_phone(self.current_edit_id, model, brand_id, specs, float(price) if price else 0.0, img)
            msg = "تم تحديث البيانات بنجاح!"
        else:
            success = self.db.add_phone(model, brand_id, "2024-01-01", specs, float(price) if price else 0.0, img)
            msg = "تم إضافة الهاتف بنجاح!"

        if success:
            messagebox.showinfo("نجاح", msg)
            if self.current_edit_id: self.show_manage_frame()
            else: self.clear_inputs()
        else:
            messagebox.showerror("فشل", "حدث خطأ أثناء الاتصال بقاعدة البيانات")

    def edit_phone(self, phone_id):
        details = self.db.get_phone_details(phone_id)
        if not details: return

        self.current_edit_id = phone_id
        self.show_add_frame()
        self.title_lbl.configure(text=f"تعديل: {details['model_name']}")
        self.save_btn.configure(text="حفظ التعديلات", fg_color="#d97706")

        self.entry_model.delete(0, 'end'); self.entry_model.insert(0, details['model_name'])
        self.combo_brand.set(details['brand_name'])
        self.entry_price.delete(0, 'end'); self.entry_price.insert(0, str(details['price']))
        if details['image_url']: self.entry_img.delete(0, 'end'); self.entry_img.insert(0, details['image_url'])

        specs = details.get('specs', {})
        self.entry_screen.delete(0, 'end'); self.entry_screen.insert(0, specs.get('Screen Size', ''))
        self.entry_ram.delete(0, 'end'); self.entry_ram.insert(0, specs.get('RAM', ''))
        self.entry_storage.delete(0, 'end'); self.entry_storage.insert(0, specs.get('Internal', ''))
        self.entry_battery.delete(0, 'end'); self.entry_battery.insert(0, specs.get('Capacity', ''))
        self.entry_camera.delete(0, 'end'); self.entry_camera.insert(0, specs.get('Main Camera', ''))
        self.entry_chipset.delete(0, 'end'); self.entry_chipset.insert(0, specs.get('Chipset', ''))

    def clear_inputs(self):
        for attr in dir(self):
            if attr.startswith("entry_"): getattr(self, attr).delete(0, 'end')
        self.combo_brand.set("اختر الشركة")

    def load_phones_list(self):
        for widget in self.manage_frame.winfo_children(): widget.destroy()
        phones = self.db.get_all_phones()
        if not phones:
            ctk.CTkLabel(self.manage_frame, text="لا توجد هواتف مسجلة").pack(pady=20)
            return
        for p in phones:
            row = ctk.CTkFrame(self.manage_frame)
            row.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(row, text=f"{p['brand_name']} {p['model_name']}", anchor="w", font=("Arial", 14)).pack(side="left", padx=10)
            ctk.CTkButton(row, text="حذف", width=60, fg_color="#ef4444", hover_color="#dc2626", command=lambda pid=p['phone_id']: self.delete_phone(pid)).pack(side="right", padx=5, pady=5)
            ctk.CTkButton(row, text="تعديل", width=60, fg_color="#3b82f6", hover_color="#2563eb", command=lambda pid=p['phone_id']: self.edit_phone(pid)).pack(side="right", padx=5, pady=5)

    def delete_phone(self, phone_id):
        if messagebox.askyesno("تأكيد", "هل أنت متأكد من حذف هذا الهاتف؟"):
            self.db.delete_phone(phone_id)
            self.load_phones_list()

    # --- دالة استيراد Excel الجديدة ---
    def import_excel_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if not file_path: return

        try:
            # قراءة ملف الإكسيل
            df = pd.read_excel(file_path)
            
            # تنظيف البيانات (ملء الخلايا الفارغة)
            df = df.fillna('')
            
            count = 0
            for index, row in df.iterrows():
                # التأكد من وجود البيانات الأساسية
                if str(row.get('Model', '')).strip() == '' or str(row.get('Brand', '')).strip() == '':
                    continue
                
                brand_id = self.db.find_or_create_brand(str(row['Brand']).strip())
                
                # تحويل السعر لرقم
                try:
                    price_val = float(str(row.get('Price', 0)).replace(',', '').replace('EGP', '').strip())
                except:
                    price_val = 0.0

                specs = [
                    {"category": "Display", "name": "Screen Size", "value": str(row.get('Screen', ''))},
                    {"category": "Performance", "name": "RAM", "value": str(row.get('RAM', ''))},
                    {"category": "Storage", "name": "Internal", "value": str(row.get('Storage', ''))},
                    {"category": "Battery", "name": "Capacity", "value": str(row.get('Battery', ''))},
                    {"category": "Camera", "name": "Main Camera", "value": str(row.get('Camera', ''))},
                    {"category": "Platform", "name": "Chipset", "value": str(row.get('Chipset', ''))}
                ]

                self.db.add_phone(
                    model_name=str(row['Model']),
                    brand_id=brand_id,
                    release_date="2024-01-01",
                    specs_list=specs,
                    price=price_val,
                    image_url=str(row.get('Image', ''))
                )
                count += 1
            
            messagebox.showinfo("نجاح", f"تم استيراد {count} هاتف بنجاح من Excel!")
            self.refresh_data()

        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء قراءة الملف:\n{e}")

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()