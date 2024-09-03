def check_func_3_6(oracle_conn):
    no = "3_6"
    check_result = "n/a"  # 초기 기본값 설정
    check_detail = "RESOURCE_LIMIT 설정값: "

    try:
        # RESOURCE_LIMIT 값 확인을 위한 쿼리
        query = "SELECT value FROM v$parameter WHERE name = 'resource_limit'"

        # 쿼리 실행
        cursor = oracle_conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            resource_limit = result[0]
            check_detail += resource_limit

            if resource_limit.upper() == 'TRUE':
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail += "설정을 확인할 수 없음"

    except Exception as e:
        # 오류 처리
        print(f"Error checking RESOURCE_LIMIT: {e}")
        check_detail += "점검 중 오류 발생"
        check_result = "n/a"

    return no, check_detail, check_result
