def check_func_1_4(mssql_conn):
    no = "1_4"
    check_detail = "Default DBA 계정외에 dba 권한이 부여된 계정: "
    check_result = "양호"

    try:
        cursor = mssql_conn.cursor()

        # sysadmin 역할을 가진 계정 조회
        cursor.execute("""
            SELECT sp.name
            FROM sys.server_principals sp
            INNER JOIN sys.server_role_members srm ON sp.principal_id = srm.member_principal_id
            INNER JOIN sys.server_principals spr ON srm.role_principal_id = spr.principal_id
            WHERE spr.name = 'sysadmin'
            AND sp.name != 'sa'
        """)
        admin_users = cursor.fetchall()

        if admin_users:
            check_detail += ", ".join([user[0] for user in admin_users])
            check_result = "취약"
        else:
            check_detail += "없음"

    except Exception as e:
        check_detail = f"오류 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result
