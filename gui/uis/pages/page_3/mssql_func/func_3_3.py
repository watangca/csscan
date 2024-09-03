def check_func_3_3(mssql_conn):
    no = "3_3"
    check_detail = ""
    check_result = "양호"  

    # 패스워드 복잡도 정책을 점검하는 쿼리
    query = """
    SELECT name, is_policy_checked
    FROM sys.sql_logins
    WHERE type_desc = 'SQL_LOGIN' AND is_disabled = 0;
    """

    try:
        cursor = mssql_conn.cursor()
        cursor.execute(query)
        logins = cursor.fetchall()

        if not logins:
            check_detail = "SQL Server 인스턴스에 활성화된 SQL 로그인이 없음"
            check_result = "n/a"
        else:
            for login in logins:
                if not login[1]:  # is_policy_checked가 False라면
                    check_result = "취약"
                    check_detail += f"로그인 {login[0]}에 패스워드 복잡도 정책이 적용되지 않음"

            if check_result == "양호":
                check_detail = "모든 활성화된 SQL 로그인에 대해 패스워드 복잡도 정책이 적용됨"
    except Exception as e:
        check_detail = f"점검 중 오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
