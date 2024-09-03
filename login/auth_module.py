import sqlite3
import os
import hashlib
import binascii
import datetime
from login import sessionmanager
from login.database.UserDatabaseManager import get_user_db_connection


# 데이터베이스 테이블 생성 및 수정
def create_tables():
    conn = get_user_db_connection()
    cursor = conn.cursor()
    # users 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            account_locked BOOLEAN NOT NULL DEFAULT 0       
        )
    ''')
    # login_attempts 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            username TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            success BOOLEAN NOT NULL,
            ip_address TEXT NOT NULL  
        )
    ''')
    conn.commit()
    conn.close()

# 사용자 인증 및 어드민 권한 확인
def authenticate_user(username, password, ip_address, db_connection):
    session_manager = sessionmanager.SessionManager(db_connection)
    cursor = db_connection.cursor()

    # COLLATE BINARY를 사용하여 대소문자를 구분
    cursor.execute('SELECT password, role FROM users WHERE username = ? COLLATE BINARY', (username,))
    user = cursor.fetchone()

    if user is not None:
        stored_password, role = user
        success = verify_password(stored_password, password)

        # 세션 생성 및 로그인 시도 기록
        session_id = session_manager.create_session(username, ip_address, login_success=success)
        log_login_attempt(session_id, username, success, ip_address)

        return role if success else False
    else:
        # 사용자가 존재하지 않는 경우에도 로그인 시도 기록
        session_id = session_manager.create_session(username, ip_address, login_success=False)
        log_login_attempt(session_id, username, False, ip_address)

        return False


# 비밀번호 해싱
def hash_password(password):
    """새 비밀번호를 해시하는 함수입니다."""
    # os.urandom은 암호학적으로 안전한 랜덤 바이트를 생성합니다.
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    # 해시와 솔트를 저장합니다.
    return (salt + pwdhash).decode('ascii')

# 비밀번호 검증
def verify_password(stored_password, provided_password):
    """저장된 해시 비밀번호와 사용자가 제공한 비밀번호를 검증하는 함수입니다."""
    # 저장된 값에서 솔트를 추출합니다.
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    # 데이터베이스에 저장된 해시와 사용자가 입력한 비밀번호의 해시를 비교
    return pwdhash == stored_password

# 로그인 시도 로깅 
def log_login_attempt(session_id, username, success, ip_address):
    conn = get_user_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO login_attempts (session_id, username, timestamp, success, ip_address) 
        VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?)
    ''', (session_id, username, success, ip_address))
    conn.commit()
    conn.close()

# 이상 행위 감지 및 잠금 메커니즘 
def detect_abnormal_behavior_and_lock_account(username):
    conn = get_user_db_connection()
    cursor = conn.cursor()
    
    # 설정: 10분 내에 5회 이상의 실패한 로그인 시도를 이상 행위로 간주
    MAX_ATTEMPTS = 5
    TIME_PERIOD = datetime.timedelta(minutes=10)
    
    now = datetime.datetime.now()
    
    # 지정된 시간 간격 내에 있는 로그인 시도 기록 조회
    cursor.execute(
        'SELECT * FROM login_attempts WHERE username = ? AND timestamp > ? AND success = 0',
        (username, now - TIME_PERIOD)
    )
    attempts = cursor.fetchall()
    
    # 실패한 로그인 시도 횟수 카운트
    failed_attempts = len(attempts)    
    # 계정 잠금 여부
    account_locked = False    
    # 이상 행위 감지 및 계정 잠금
    if failed_attempts >= MAX_ATTEMPTS:
        account_locked = True
        # 계정을 잠그는 로직 구현
        cursor.execute('UPDATE users SET account_locked = 1 WHERE username = ?', (username,))  
    conn.commit()
    conn.close()
    
    return account_locked

# 사용자 등록 
def register_user(username, email, password, role='user'):
    conn = get_user_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)  
    try:
        cursor.execute('INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)', (username, email, hashed_password, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# 마스터 사용자 및 일반 사용자 생성
# def create_master_and_regular_user():
#     # 마스터 사용자 정보
#     master_username = 'master'
#     master_password = 'masterpassword'
#     master_email = 'master@example.com'  

#     # 일반 사용자 정보
#     regular_username = 'test'
#     regular_password = 'test1234'
#     regular_email = 'test@example.com' 

#     # 데이터베이스 연결
#     conn = get_user_db_connection()
#     cursor = conn.cursor()

#     # 마스터 사용자 생성
#     cursor.execute('SELECT * FROM users WHERE username = ?', (master_username,))
#     if cursor.fetchone() is None:
#         # 마스터 계정이 어드민 권한을 가지도록 설정합니다.
#         hashed_master_password = hash_password(master_password)
#         cursor.execute('INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
#                        (master_username, master_email, hashed_master_password, 'admin'))

#     # 일반 사용자 생성
#     cursor.execute('SELECT * FROM users WHERE username = ?', (regular_username,))
#     if cursor.fetchone() is None:
#         # 일반 계정 생성
#         hashed_regular_password = hash_password(regular_password)
#         cursor.execute('INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
#                        (regular_username, regular_email, hashed_regular_password, 'user'))

#     # 변경 사항 커밋
#     conn.commit()
#     conn.close()


# 로그인 시도 기록 확인
def print_login_attempts():
    conn = get_user_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM login_attempts')
    attempts = cursor.fetchall()
    for attempt in attempts:
        print(attempt)
    conn.close()

# 모듈이 임포트될 때 초기 설정 실행
create_tables()
# create_master_and_regular_user()
