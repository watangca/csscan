import json  # JSON 데이터를 처리하기 위해 필요

def check_func_2_5(mysql_conn):
    no = "2_5"
    
    # MySQL 버전 확인
    cursor = mysql_conn.cursor()
    cursor.execute("SELECT VERSION();")
    version = cursor.fetchone()
    
    if version and version[0] >= '8.0':  # MySQL 8.0 이상인지 확인
        # User_attributes 열에서 설정 확인
        cursor.execute("SELECT user, host, account_locked, User_attributes FROM mysql.user;")
        users = cursor.fetchall()
        
        # 설정 확인 로직 개선
        check_detail_list = []
        for user in users:
            user_attrs = json.loads(user[3]) if user[3] else {}  # User_attributes 열을 JSON으로 파싱
            fa = user_attrs.get("Password_locking", {}).get("failed_login_attempts")
            plt = user_attrs.get("Password_locking", {}).get("password_lock_time_days")
            detail = f"User: {user[0]}, Host: {user[1]}, Account Locked: {user[2]}, Failed Login Attempts: {fa}, Password Lock Time (days): {plt}"
            check_detail_list.append(detail)
        
        check_detail = "로그인 시도횟수 제한 및 계정 잠금 시간 설정:\n" + "\n".join(check_detail_list)
        # 설정이 적용된 사용자가 하나라도 있는지 확인
        if any(user[3] and '"failed_login_attempts":' in user[3] and '"password_lock_time_days":' in user[3] for user in users):
            check_result = "양호"
        else:
            check_result = "취약"
    else:
        check_detail = "MySQL 버전 8.0 이상에서만 로그인 시도횟수 제한 및 계정 잠금 시간 설정을 지원함"
        check_result = "n/a"
    
    cursor.close()
    return no, check_detail, check_result
