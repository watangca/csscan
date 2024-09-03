def check_func_5_1(mssql_conn):
    no = "5_1"
    check_result = "n/a"
    check_detail = ""

    try:
        cursor = mssql_conn.cursor()

        # 일반 사용자로 접근 가능한 감사 테이블 목록 조회
        cursor.execute("""
        SELECT name 
        FROM sys.objects 
        WHERE type_desc = 'USER_TABLE' 
        AND name LIKE 'sys%audit%'
        """)
        audit_tables = cursor.fetchall()

        if audit_tables:
            check_detail = "감사 테이블에 접근 가능한 일반 사용자 계정: "
            check_detail += ", ".join([table[0] for table in audit_tables])
            check_result = "취약"
        else:
            check_detail = "감사 테이블에 접근 가능한 일반 사용자 계정이 발견되지 않음"
            check_result = "양호"
    except Exception as e:
        check_detail = f"감사 테이블 접근 권한 확인 중 오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
