def check_func_4_2(mssql_conn):
    no = "4_2"
    check_result = "n/a"  # 기본값 설정
    check_detail = "감사기록 설정값 조회 중 문제 발생"

    try:
        cursor = mssql_conn.cursor()
        # 서버 수준 감사 설정 확인
        cursor.execute("""
        SELECT
            name
        FROM
            sys.server_audits
        WHERE
            is_state_enabled = 1;
        """)
        audits = cursor.fetchall()

        if audits:  # 감사기록 설정이 활성화되어 있는 경우
            audit_names = [audit[0] for audit in audits]
            audit_details = ", ".join(audit_names)
            check_detail = f"활성화된 감사기록: {audit_details}"
            check_result = "양호"
        else:  # 활성화된 감사기록이 없는 경우
            check_detail = "활성화된 감사기록이 발견되지 않음"
            check_result = "취약"
    except Exception as e:
        check_detail = f"감사기록 설정값 조회 중 예외 발생: {str(e)}"
        # 예외 발생 시 결과를 'n/a'로 설정

    return no, check_detail, check_result
