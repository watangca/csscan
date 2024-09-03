def check_func_4_1(oracle_conn):
    no = "4_1"
    # 버전 정보를 확인하기 위한 쿼리
    query_version = "SELECT * FROM v$version WHERE banner LIKE 'Oracle%'"

    try:
        # 쿼리 실행
        cursor = oracle_conn.cursor()
        cursor.execute(query_version)
        version_info = cursor.fetchone()
        if version_info:
            oracle_version = version_info[0]
            check_detail = f"현재 Oracle 버전: {oracle_version}, 영향도 평가를 실시하여 최신 패치 적용여부 결정 필요"
            check_result = "양호"  # 이 점검 항목은 버전 정보 확인에 초점을 맞추며, 결과는 '양호'로 설정
        else:
            check_detail = "Oracle 버전 정보를 조회할 수 없습니다."
            check_result = "n/a"

    except Exception as e:
        # 오류 처리
        check_detail = f"Oracle 버전 정보 조회 중 오류 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result
