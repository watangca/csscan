import sys
import platform
import os

# 애플리케이션 루트 경로를 운영 체제에 맞게 설정
if platform.system() == 'Darwin':  # macOS
    app_root = '/Applications/csscan.app/Contents/Resources/login'
elif platform.system() == 'Windows':  # Windows
    app_root = 'C:\\Program Files (x86)\\csscan\\_internal'
else:
    raise Exception("Unsupported operating system.")

sys.path.append(app_root)

# settings.json 파일의 경로 설정
settings_path = os.path.join(app_root, 'settings.json')

# 환경 변수 설정 (필요 시)
os.environ['SETTINGS_PATH'] = settings_path


from login.auth_module import create_tables, register_user
from login.database.UserDatabaseManager import get_user_db_connection

def create_admin_account(username, password):
    email = f'{username}@example.com'
    if register_user(username, email, password, 'admin'):
        print(f"Admin account created for username: {username}")
    else:
        print(f"Failed to create admin account for username: {username}. Username may already exist.")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: create_admin_account.py <username> <password>")
        sys.exit(1)
    username = sys.argv[1]
    password = sys.argv[2]

    # 데이터베이스 연결 테스트
    conn = get_user_db_connection()
    conn.close()

    create_tables()  
    create_admin_account(username, password)