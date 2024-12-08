import sqlite3

class dbContextManger():
    def __init__(self, db_name: str) -> None:
        self.db_name: str = db_name
        self.conn = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()


def conn_to_sqldb() -> str:
    """
    إنشاء اتصال بقاعدة البيانات وإنشاء الجداول إذا لم تكن موجودة
    
    Args:
        db_path (str): مسار ملف قاعدة البيانات
        
    Returns:
        str: "done" إذا تمت العملية بنجاح، False في حالة حدوث خطأ
    """
    try:
        db_path="server.db"
        # استخدام context manager للتعامل مع الاتصال تلقائياً
        with dbContextManger(db_path) as conn:
            # تفعيل دعم المفاتيح الأجنبية
            conn.execute("PRAGMA foreign_keys = ON")
            
            cursor = conn.cursor()
            
            # إنشاء جدول معلومات المستخدمين
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id BIGINT NOT NULL,
                    name VARCHAR(70),
                    age INTEGER,
                    UNIQUE(user_id),
                    CHECK(age > 0 AND age < 120)
                )
            """)
            
            # إنشاء جدول التحذيرات
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS warns (
                    warn_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    warn_reason VARCHAR(100) NOT NULL,
                    warned_id INTEGER NOT NULL,
                    warn_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(warned_id) REFERENCES users_info(id) ON DELETE CASCADE,
                    CHECK(LENGTH(warn_reason) > 0)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS friendship(
                    id1 INTEGER NOT NULL,
                    id2 INTEGER NOT NULL,
                    FOREIGN KEY(id1) REFERENCES users_info(id) ON DELETE CASCADE,
                    FOREIGN KEY(id2) REFERENCES users_info(id) ON DELETE CASCADE
                )
            """)

            cursor.close()
            
            return "done"
        
    except sqlite3.Error as e:
        print(f"خطأ في قاعدة البيانات: {e}")
        return f"Error With DataBase {e}"
    except Exception as e:
        print(f"خطأ غير متوقع: {e}")
        return f"Error {e}"


    

if __name__== "__main__":
    print(conn_to_sqldb())