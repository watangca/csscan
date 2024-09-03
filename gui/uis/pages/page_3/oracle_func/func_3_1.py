def check_func_3_1(oracle_conn):
    no = "3_1"
    check_detail = []
    check_result = "양호"  # 기본값 양호로 설정

    try:
        # Oracle 데이터베이스에 대한 쿼리 실행
        cursor = oracle_conn.cursor()
        query = "SELECT granted_role FROM dba_role_privs WHERE grantee = 'PUBLIC'"
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            granted_roles = ', '.join([row[0] for row in results])
            check_detail.append(f"DBA Role 설정: 발견된 role: {granted_roles}")
            if 'DBA' in granted_roles:
                check_result = "취약"
            else:
                check_result = "양호"
        else:
            check_detail.append("DBA Role 설정: no rows selected")
            check_result = "양호"

    except Exception as e:
        check_result = "n/a"
        check_detail.append(f"점검 중 오류 발생: {str(e)}")

    return no, check_detail, check_result
