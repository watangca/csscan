from login.database.UserDatabaseManager import get_user_db_connection

class ProfileManager:
    def __init__(self):
        self.create_profile_table()

    def create_profile_table(self):
        """사용자 프로필 테이블을 생성합니다."""
        with get_user_db_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_profiles (
                        username TEXT PRIMARY KEY,
                        email TEXT,  
                        first_name TEXT,
                        last_name TEXT,
                        company_name TEXT,
                        company_website TEXT,
                        phone TEXT,
                        country TEXT
                    )
                ''')
            except Exception as e:
                print(f"테이블 생성 중 오류 발생: {e}")

    def save_profile(self, username, first_name, last_name, company_name, company_website, phone, country):
        """사용자 프로필을 저장하거나 업데이트합니다."""
        with get_user_db_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO user_profiles (username, first_name, last_name, company_name, company_website, phone, country)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(username) 
                    DO UPDATE SET 
                        first_name=excluded.first_name,
                        last_name=excluded.last_name,
                        company_name=excluded.company_name,
                        company_website=excluded.company_website,
                        phone=excluded.phone,
                        country=excluded.country;
                ''', (username, first_name, last_name, company_name, company_website, phone, country))
            except Exception as e:
                print(f"프로필 저장 중 오류 발생: {e}")

    def get_profile(self, username):
        with get_user_db_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT first_name, last_name, company_name, company_website, phone, country FROM user_profiles WHERE username = ?", (username,))
                return cursor.fetchone()
            except Exception as e:
                print(f"프로필 불러오기 중 오류 발생: {e}")
                return None
        
    def get_user_info(self, username):
        """주어진 사용자 이름에 해당하는 사용자 정보를 users 테이블에서 불러옵니다."""
        with get_user_db_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT username, email FROM users WHERE username = ?", (username,))
                return cursor.fetchone()
            except Exception as e:
                print(f"사용자 정보 불러오기 중 오류 발생: {e}")
                return None
