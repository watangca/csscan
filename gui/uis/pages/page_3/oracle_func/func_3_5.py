def check_func_3_5(oracle_conn):
    no = "3_5"
    # 초기 설정
    check_detail = "Grant Option Role이 부여된 계정: "
    check_result = "n/a"  # 기본값 설정

    try:
        # Grant Option이 일반 사용자에게 부여되었는지 점검하기 위한 쿼리
        query = """
        SELECT grantee || ':' || owner || '.' || table_name AS grant_info
        FROM dba_tab_privs
        WHERE grantable = 'YES'
        AND owner NOT IN ('SYS','MDSYS','ORDPLUGINS','ORDSYS','SYSTEM', 'WMSYS','DBSNMP', 'LBACSYS')
        AND grantee NOT IN (SELECT grantee FROM dba_role_privs WHERE granted_role = 'DBA')
        ORDER BY grantee
        """

        # 쿼리 실행
        cursor = oracle_conn.cursor()
        cursor.execute(query)
        grants = cursor.fetchall()

        if grants:
            # 취약: Grant Option이 일반 사용자에게 부여된 경우
            check_result = "취약"
            granted_accounts = ', '.join([grant[0] for grant in grants])
            check_detail += granted_accounts
        else:
            # 양호: Grant Option이 일반 사용자에게 부여되지 않은 경우
            check_result = "양호"
            check_detail += "부여되지 않음"

    except Exception as e:
        print(f"Error checking Grant Option Roles: {e}")
        check_detail += "점검 중 오류 발생"
        check_result = "n/a"

    return no, check_detail, check_result
