def check_func_3_3(oracle_conn):
    no = "3_3"
    # 초기 기본값 설정
    check_detail = "PASSWORD_VERIFY_FUNCTION 설정값: 설정을 확인할 수 없음"
    check_result = "n/a"

    try:
        # 패스워드 검증 함수 설정값 확인 쿼리
        query = """
        SELECT profile, resource_name, limit
        FROM dba_profiles
        WHERE resource_name = 'PASSWORD_VERIFY_FUNCTION'
        """

        # 쿼리 실행
        cursor = oracle_conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        # 설정값 분석
        if results:
            for profile, resource_name, limit in results:
                # NULL이 아니고, 'DEFAULT' 이상의 구체적인 설정이 있는 경우를 찾음
                if limit not in (None, 'NULL', 'DEFAULT'):
                    check_detail = f"{profile} 프로파일에서 {resource_name}이(가) {limit}로 설정됨"
                    check_result = "양호"
                    break
            else:  # 양호한 설정을 찾지 못한 경우
                check_detail = "모든 프로파일에서 PASSWORD_VERIFY_FUNCTION 설정값이 적절히 설정되지 않음"
                check_result = "취약"
        else:
            # 쿼리 결과가 없는 경우
            check_result = "취약"
    except Exception as e:
        # 오류 처리
        print(f"Error checking PASSWORD_VERIFY_FUNCTION: {e}")
        check_result = "n/a"

    return no, check_detail, check_result
