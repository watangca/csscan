def check_func_2_2(mssql_conn):
    no = "2_2"
    check_detail = "시스템 테이블에 접근권한이 있는 계정명: "
    check_result = "n/a"  # 초기 상태 설정

    try:
        cursor = mssql_conn.cursor()
        # 시스템 뷰 및 테이블에 대한 접근 권한을 가진 사용자 및 역할 확인
        query = """
        SELECT dp.name AS principal_name, dp.type_desc AS principal_type, 
               perm.permission_name, perm.state_desc, 
               obj.name AS object_name, sch.name AS schema_name
        FROM sys.database_permissions AS perm
        JOIN sys.objects AS obj ON perm.major_id = obj.object_id
        JOIN sys.schemas AS sch ON obj.schema_id = sch.schema_id
        JOIN sys.database_principals AS dp ON perm.grantee_principal_id = dp.principal_id
        WHERE obj.is_ms_shipped = 1 AND perm.type = 'SL' -- Looking for SELECT permissions on system objects
        AND dp.name IN ('public', 'guest') OR dp.type IN ('S', 'U') -- System, SQL user, and Windows user
        ORDER BY dp.name;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            # 접근 권한이 있는 계정명 출력
            for row in results:
                check_detail += f"\nPrincipal Name: {row[0]}, Type: {row[1]}, Permission: {row[2]}, State: {row[3]}, Object: {row[4]}, Schema: {row[5]}"
            check_result = "취약"
        else:
            check_detail = "DBA 외 시스템 테이블에 접근권한이 있는 계정 없음."
            check_result = "양호"

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    finally:
        if cursor:
            cursor.close()

    return no, check_detail, check_result
