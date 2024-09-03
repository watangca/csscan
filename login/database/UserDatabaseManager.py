import os
import shutil
import sqlite3
import sys

def get_user_db_connection():
    app_name = "CSSCAN"
    db_filename = "cs_scanner_users.db"

    # PyInstaller 또는 개발 환경에 따라 데이터베이스 경로 설정
    if getattr(sys, 'frozen', False):
        # PyInstaller 환경: 실행 파일이 있는 곳의 환경 데이터 사용
        if os.name == 'nt':  # Windows 환경
            dest_folder = os.path.join(os.environ.get('APPDATA', ''), app_name)
        else:  # macOS 및 Unix 계열
            dest_folder = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', app_name)
    else:
        # 개발 환경: 프로젝트 기반 경로 사용
        dest_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database')

    database_path = os.path.join(dest_folder, db_filename)

    # 데이터베이스 경로가 존재하지 않을 경우 생성
    os.makedirs(dest_folder, exist_ok=True)
    if not os.path.exists(database_path):
        # 데이터베이스 파일 복사
        src_db_path = os.path.join(sys._MEIPASS, 'login/database', db_filename) if getattr(sys, 'frozen', False) else os.path.join(dest_folder, db_filename)
        shutil.copy(src_db_path, database_path)

    # 데이터베이스 파일에 대한 연결 시도
    try:
        conn = sqlite3.connect(database_path)
        return conn
    except sqlite3.OperationalError as e:
        raise Exception(f"Unable to open database file at {database_path}: {e}")

