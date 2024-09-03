def check_func_1_4(oracle_conn):
    no = "1_4"
    check_detail = ""
    check_result = "n/a"

    try:
        cursor = oracle_conn.cursor()

        # Step 1: SYSDBA 권한 점검
        cursor.execute("""
            SELECT USERNAME 
            FROM V$PWFILE_USERS 
            WHERE USERNAME NOT IN (SELECT GRANTEE FROM DBA_ROLE_PRIVS WHERE GRANTED_ROLE='DBA') 
            AND USERNAME !='INTERNAL' 
            AND SYSDBA='TRUE'
        """)
        sysdba_users = cursor.fetchall()
        if sysdba_users:
            check_detail += "SYSDBA 권한 계정 발견: {}\n".format(", ".join([user[0] for user in sysdba_users]))
            check_result = "취약"
        else:
            check_detail += "SYSDBA 권한 계정 없음\n"
            check_result = "양호"

        # Step 2: Admin에 부적합 계정 존재 여부 점검
        cursor.execute("""
            SELECT GRANTEE, PRIVILEGE 
            FROM DBA_SYS_PRIVS 
            WHERE GRANTEE NOT IN ('SYS', 'SYSTEM', 'AQ_ADMINISTRATOR_ROLE', 'DBA', 'MDSYS', 'LBACSYS', 'SCHEDULER_ADMIN', 'WMSYS') 
            AND ADMIN_OPTION='YES' 
            AND GRANTEE NOT IN (SELECT GRANTEE FROM DBA_ROLE_PRIVS WHERE GRANTED_ROLE='DBA')
        """)
        admin_users = cursor.fetchall()
        if admin_users:
            check_detail += "Admin 부적합 계정 발견: {}\n".format(", ".join([user[0] for user in admin_users]))
            check_result = "취약"
        else:
            check_detail += "Admin 부적합 계정 없음\n"
            if check_result != "취약":
                check_result = "양호"

    except Exception as e:
        check_detail = "데이터베이스 접속 오류: {}".format(e)
        check_result = "n/a"

    return no, check_detail, check_result
