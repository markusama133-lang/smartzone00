import mysql.connector

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            print(f"Error connecting to DB: {err}")

    def ensure_connection(self):
        if not self.conn or not self.conn.is_connected():
            self.connect()

    def get_all_brands(self):
        self.ensure_connection()
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM brands")
        result = cursor.fetchall()
        cursor.close()
        return result

    def find_or_create_brand(self, brand_name):
        self.ensure_connection()
        cursor = self.conn.cursor()
        cursor.execute("SELECT brand_id FROM brands WHERE brand_name = %s", (brand_name,))
        result = cursor.fetchone()
        
        if result:
            cursor.close()
            return result[0]
        else:
            cursor.execute("INSERT INTO brands (brand_name) VALUES (%s)", (brand_name,))
            self.conn.commit()
            new_id = cursor.lastrowid
            cursor.close()
            return new_id

    # --- تم تحديث هذه الدالة لترجع ID بدلاً من True ---
    def add_phone(self, model_name, brand_id, release_date, specs_list, price, image_url):
        self.ensure_connection()
        try:
            cursor = self.conn.cursor()
            
            # 1. إضافة الهاتف
            query_phone = """
                INSERT INTO phones (model_name, brand_id, release_date, image_url, price)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query_phone, (model_name, brand_id, release_date, image_url, price))
            phone_id = cursor.lastrowid

            # 2. إضافة المواصفات
            query_specs = """
                INSERT INTO specs (phone_id, spec_category, spec_name, spec_value)
                VALUES (%s, %s, %s, %s)
            """
            
            for spec in specs_list:
                cursor.execute(query_specs, (
                    phone_id, 
                    spec.get('category', 'General'), 
                    spec.get('name'), 
                    spec.get('value')
                ))

            self.conn.commit()
            cursor.close()
            return phone_id # إرجاع الآي دي لكي يستخدمه التطبيق
        except mysql.connector.Error as err:
            print(f"Error saving phone: {err}")
            return None

    def get_all_phones(self):
        self.ensure_connection()
        cursor = self.conn.cursor(dictionary=True)
        query = """
            SELECT p.phone_id, p.model_name, b.brand_name, p.price, p.image_url 
            FROM phones p 
            JOIN brands b ON p.brand_id = b.brand_id
            ORDER BY p.phone_id DESC
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_phone_details(self, phone_id):
        self.ensure_connection()
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            # 1. البيانات الأساسية
            query_phone = """
                SELECT p.*, b.brand_name 
                FROM phones p 
                JOIN brands b ON p.brand_id = b.brand_id 
                WHERE p.phone_id = %s
            """
            cursor.execute(query_phone, (phone_id,))
            phone = cursor.fetchone()
            
            if not phone:
                return None

            # 2. المواصفات
            query_specs = "SELECT spec_name, spec_value FROM specs WHERE phone_id = %s"
            cursor.execute(query_specs, (phone_id,))
            specs = cursor.fetchall()
            
            phone['specs'] = {s['spec_name']: s['spec_value'] for s in specs}
            
            cursor.close()
            return phone
            
        except mysql.connector.Error as err:
            print(f"Error getting details: {err}")
            return None

    # --- هذه الدالة كانت ناقصة وتمت إضافتها ---
    def find_phone_by_name(self, search_term):
        self.ensure_connection()
        try:
            cursor = self.conn.cursor(dictionary=True)
            # يبحث في اسم الموديل أو اسم الشركة + الموديل
            query = """
                SELECT p.phone_id 
                FROM phones p
                JOIN brands b ON p.brand_id = b.brand_id
                WHERE p.model_name LIKE %s OR CONCAT(b.brand_name, ' ', p.model_name) LIKE %s
                LIMIT 1
            """
            term = f"%{search_term}%"
            cursor.execute(query, (term, term))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return result['phone_id']
            return None
        except mysql.connector.Error as err:
            print(f"Error finding phone: {err}")
            return None

    def delete_phone(self, phone_id):
        self.ensure_connection()
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM phones WHERE phone_id = %s", (phone_id,))
            self.conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error deleting: {err}")
            return False