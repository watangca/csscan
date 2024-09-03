def check_func_4_2(oracle_conn):
    no = "4_2"
    check_result = "n/a"  # 기본값 설정
    check_detail = "감사기록 설정값: "

    try:
        # 감사 정책 설정값 확인을 위한 쿼리
        query = "SELECT value FROM v$parameter WHERE name = 'audit_trail'"

        # 쿼리 실행
        cursor = oracle_conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            audit_trail_value = result[0]
            check_detail += audit_trail_value

            # 감사 로그 저장 정책이 활성화된 경우
            if audit_trail_value.upper() in ('DB', 'DB_EXTENDED', 'XML', 'XML_EXTENDED'):
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail += "설정을 확인할 수 없음"

    except Exception as e:
        print(f"Error checking audit policy: {e}")
        check_detail += "점검 중 오류 발생"
        check_result = "n/a"

    return no, check_detail, check_result
