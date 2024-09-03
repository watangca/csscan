def check_func_3_2(oracle_conn):
    no = "3_2"
    # 설정값을 확인하기 위한 딕셔너리 초기화
    check_detail = {'os_roles': None, 'remote_os_authentication': None, 'remote_os_roles': None}

    try:
        # 설정값 조회를 위한 SQL 쿼리
        query = """
        SELECT name, value
        FROM v$parameter
        WHERE name IN ('os_roles', 'remote_os_authentication', 'remote_os_roles')
        """
        
        # oracle_conn을 사용하여 쿼리 실행
        cursor = oracle_conn.cursor()
        cursor.execute(query)
        
        # 조회된 결과 처리
        for name, value in cursor:
            if name in check_detail:
                check_detail[name] = value  # 해당 설정의 값을 딕셔너리에 저장

        # 모든 설정값이 'FALSE'인지 확인
        if all(value.upper() == 'FALSE' for value in check_detail.values() if value is not None):
            # 모든 필요한 설정값이 'FALSE'로 확인된 경우
            if None not in check_detail.values():
                check_result = "양호"
            else:
                # 어떤 설정값을 확인하지 못한 경우
                check_result = "n/a"
        else:
            # 하나라도 'TRUE'이거나 확인하지 못한 설정이 있는 경우
            check_result = "취약"

    except Exception as e:
        # 오류 처리
        print(f"Error checking database settings: {e}")
        check_result = "n/a"
    
    return no, check_detail, check_result
