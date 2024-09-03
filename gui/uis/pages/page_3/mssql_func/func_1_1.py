import datetime

def check_func_1_1(mssql_conn):
    no = "1_1"
    check_detail = "mssql dba 계정 중 패스워드 변경 이력 출력"
    check_result = "n/a"

    try:
        # cursor 객체 생성
        cursor = mssql_conn.cursor()

        # MSSQL 쿼리 실행
        query = "SELECT name, modify_date FROM sys.sql_logins WHERE type_desc = 'SQL_LOGIN' AND is_disabled = 0"
        cursor.execute(query)

        changed_accounts = []
        current_time = datetime.datetime.now()

        # 결과 처리
        for row in cursor:
            account, modify_date = row
            modify_time = modify_date

            # 패스워드 변경 기준 설정 (예: 최근 90일)
            if (current_time - modify_time).days <= 90:
                changed_accounts.append(account)

        if changed_accounts:
            check_result = "양호"
            check_detail += f"\n패스워드 변경된 계정: {', '.join(changed_accounts)}"
        else:
            check_result = "취약"
    except Exception as e:
        check_detail += f"\n쿼리 실행 오류: {str(e)}"

    return no, check_detail, check_result