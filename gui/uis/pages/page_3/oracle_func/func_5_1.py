def check_func_5_1(oracle_conn):
    no = "5_1"
    check_result = "n/a"  # 기본값 설정
    check_detail = "Audit Table 접근 계정: "

    try:
        # 감사 테이블 소유자 조회 쿼리
        query = "SELECT owner FROM dba_tables WHERE table_name='AUD$'"

        # 쿼리 실행
        cursor = oracle_conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            owner = result[0]
            check_detail += owner

            # 관리자 계정이 소유자인지 확인
            if owner.upper() in ('SYS', 'SYSTEM'):  # 일반적인 관리자 계정
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail += "정보를 찾을 수 없음."

    except Exception as e:
        print(f"Error checking Audit Table access: {e}")
        check_result = "n/a"

    return no, check_detail, check_result
