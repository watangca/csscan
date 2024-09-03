def check_func_3_1(mssql_conn):
    no = "3_1"
    check_detail = ""
    
    try:
        cursor = mssql_conn.cursor()
        # 데이터베이스의 모든 사용자에 대해 Role을 체크합니다.
        cursor.execute("""
            SELECT dp.name, dp.type_desc, STRING_AGG(rp.name, ', ') WITHIN GROUP (ORDER BY rp.name) AS roles
            FROM sys.database_principals AS dp
            JOIN sys.database_role_members AS drm ON dp.principal_id = drm.member_principal_id
            JOIN sys.database_principals AS rp ON drm.role_principal_id = rp.principal_id
            WHERE dp.type_desc IN ('SQL_USER', 'WINDOWS_USER', 'WINDOWS_GROUP')
            GROUP BY dp.name, dp.type_desc
            HAVING STRING_AGG(rp.name, ', ') LIKE '%public%'
        """)
        
        rows = cursor.fetchall()
        if rows:
            check_detail = "DBA 계정의 Role이 Public으로 설정되어 있는 계정 목록:"
            for row in rows:
                check_detail += f"- 계정 이름: {row[0]}, 타입: {row[1]}, Role: {row[2]}"
            check_result = "취약"
        else:
            check_detail = "DBA 계정의 Role이 Public으로 설정되어 있지 않음"
            check_result = "양호"
    except Exception as e:
        check_detail = f"점검 중 오류 발생: {str(e)}"
        check_result = "n/a"
    
    return no, check_detail, check_result
