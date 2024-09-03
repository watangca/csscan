def check_func_2_1(mssql_conn):
    no = "2_1"
    check_result = "n/a"  # 초기값 설정
    check_detail = "원격에서 DB 서버로의 접속을 허용하는 계정: "

    # 원격 접속을 허용하는 계정을 확인하는 쿼리
    sql_query = """
    SELECT sp.name
    FROM sys.server_principals sp
    WHERE sp.principal_id > 4 AND sp.type IN ('U', 'S', 'G') 
    AND sp.is_disabled = 0
    AND sp.name NOT LIKE '##%' OR sp.name = 'sa'
    ORDER BY sp.name;
    """
    try:
        cursor = mssql_conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                check_detail += f"{row[0]}, "
            check_detail = check_detail[:-2]  # 마지막에 추가된 쉼표와 공백 제거
            check_result = "취약"  # 접속이 가능한 계정이 있으므로 "취약"
        else:
            check_detail += "원격 접속을 허용하는 계정이 없습니다."
            check_result = "양호"
    except Exception as e:
        check_detail = f"SQL 쿼리 실행 중 예외 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result
