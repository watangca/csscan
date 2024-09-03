def check_func_1_3(mssql_conn):
    no = "1_3"
    check_detail = "패스워드 복잡도 정책 적용 여부 및 로그인 상세 정보:\n"
    check_result = "n/a"

    try:
        cursor = mssql_conn.cursor()
        # LOGINPROPERTY 값을 문자열로 변환
        cursor.execute("""
            SELECT 
                name, 
                CAST(LOGINPROPERTY(name, 'IsPolicyChecked') AS VARCHAR) as PolicyChecked, 
                is_disabled 
            FROM sys.sql_logins
        """)
        logins_info = [(row[0], row[1], row[2]) for row in cursor]

        non_compliant_logins = []
        for login, policy_checked, is_disabled in logins_info:
            policy_status = "적용됨" if policy_checked == '1' else "적용되지 않음"
            check_detail += f"로그인: {login}, 패스워드 정책: {policy_status}, 계정 상태: {'비활성화' if is_disabled else '활성화'}\n"

            if policy_checked != '1':
                non_compliant_logins.append(login)

        if non_compliant_logins:
            check_result = "취약"
            check_detail += f"\n패스워드 정책이 적용되지 않은 로그인: {', '.join(non_compliant_logins)}"
        else:
            check_result = "양호"
            check_detail += "\n모든 로그인에 패스워드 정책이 적용됨"

    except Exception as e:
        check_detail += f"\n점검 중 오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
