def check_func_2_5(oracle_conn):
    no = "2_5"
    check_detail = "로그인 시도 횟수 제한값"
    check_result = "n/a"  # 초기값 설정

    try:
        # Oracle 데이터베이스에 쿼리 실행
        cursor = oracle_conn.cursor()
        query = """
                SELECT RESOURCE_NAME, LIMIT
                FROM DBA_PROFILES
                WHERE PROFILE='DEFAULT'
                AND RESOURCE_NAME='FAILED_LOGIN_ATTEMPTS'
                """
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            limit_value = result[1]
            check_detail += ": " + str(limit_value)
            
            # 로그인 시도 횟수 제한 설정을 확인
            if limit_value.isdigit():  # 숫자인 경우
                limit_value = int(limit_value)
                if limit_value > 0:
                    check_result = "양호"
                else:
                    check_result = "취약"
            else:
                if limit_value == 'UNLIMITED':
                    check_result = "취약"
                else:
                    check_result = "n/a"  # 예상치 못한 값인 경우
        else:
            check_detail += ": 설정값 없음"
            check_result = "취약"

    except Exception as e:
        check_detail += ": 에러 발생 - " + str(e)
        check_result = "n/a"

    finally:
        if cursor:
            cursor.close()

    return no, check_detail, check_result