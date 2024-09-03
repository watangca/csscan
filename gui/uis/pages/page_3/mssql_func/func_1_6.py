def check_func_1_6(mssql_conn):
    no = "1_6"
    check_detail = "DBA 계정 외 계정: 출력된 계정에 대한 공용계정으로 사용 여부 인터뷰 필요."
    check_result = "양호"  # 무조건 양호로 판단

    # SQL 쿼리. sys.database_principals 뷰에서 DBA 계정을 제외한 모든 계정을 조회
    query = """
    SELECT name
    FROM sys.database_principals
    WHERE type_desc IN ('SQL_USER', 'WINDOWS_USER', 'WINDOWS_GROUP')
    AND name NOT IN ('dbo', 'guest', 'sys', 'INFORMATION_SCHEMA')
    """
    try:
        cursor = mssql_conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                check_detail += row[0] + ", "
            check_detail = check_detail[:-2]  # 마지막에 추가된 쉼표와 공백 제거
    except Exception as e:
        check_detail = f"오류 발생: {e}"

    return no, check_detail, check_result
