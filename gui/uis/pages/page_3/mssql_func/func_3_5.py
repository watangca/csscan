def check_func_3_5(mssql_conn):
    no = "3_5"
    # 초기 상세 설명 설정
    check_detail = "grant option 권한이 부여되지 않은 경우를 확인"
    check_result = "n/a"  # 초기 결과는 n/a로 설정

    try:
        cursor = mssql_conn.cursor()
        # WITH GRANT OPTION이 설정된 일반 사용자를 찾는 쿼리
        cursor.execute("""
            SELECT dp.name, dp.type_desc, prm.permission_name, prm.state_desc
            FROM sys.database_permissions prm
            JOIN sys.database_principals dp ON prm.grantee_principal_id = dp.principal_id
            WHERE prm.state_desc = 'WITH GRANT OPTION'
            AND dp.type IN ('S', 'U')  -- S: SQL user, U: Windows user
        """)
        rows = cursor.fetchall()
        
        if rows:
            # WITH GRANT OPTION 권한이 부여된 사용자가 있을 경우
            check_result = "취약"
            users_with_grant_option = ", ".join([row[0] for row in rows])
            check_detail = f"grant option 권한이 부여되어 있는 일반 사용자: {users_with_grant_option}"
        else:
            # WITH GRANT OPTION 권한이 부여되지 않았으므로 양호
            check_result = "양호"
            check_detail = "grant option 권한이 부여되어 있는 일반 사용자가 없음"
    except Exception as e:
        check_detail = f"점검 중 오류 발생 - {str(e)}"
    
    return no, check_detail, check_result
