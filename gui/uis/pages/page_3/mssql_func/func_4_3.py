def check_func_4_3(mssql_conn):
    no = "4_3"
    check_result = "양호"  # 기본값 설정
    try:
        cursor = mssql_conn.cursor()
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()
        if row:  # fetchone() 결과가 있는 경우
            version_info = row[0]
        else:  # 결과가 없는 경우 (예상치 못한 상황)
            version_info = "버전 정보를 조회할 수 없습니다."
            check_result = "n/a"  # 버전 정보를 조회하지 못한 경우 조치가 필요하다고 표시

        check_detail = f"설치된 버전 정보: {version_info}. 현재 버전정보와 MS SQL 최신패치를 확인하고, 적용 영향도 평가를 실시하여 적용여부를 판단해야 함."
                
    except Exception as e:
        check_detail = f"버전 정보 조회 중 오류 발생: {str(e)}"
        check_result = "n/a"  # 예외가 발생한 경우 결과를 'n/a'로 설정
    
    return no, check_detail, check_result