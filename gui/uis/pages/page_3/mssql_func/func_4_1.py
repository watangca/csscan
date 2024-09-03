def check_func_4_1(mssql_conn):
    no = "4_1"
    check_result = "양호"  # 기본값 설정
    try:
        cursor = mssql_conn.cursor()
        # 현재 적용된 보안 패치 정보 조회
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()
        if row:  # fetchone() 결과가 있는 경우
            version_info = row[0]
            security_patch_info = version_info.split('-')[-1].strip()
        else:  # 결과가 없는 경우 (예상치 못한 상황)
            security_patch_info = "보안 패치 정보를 조회할 수 없습니다."
            check_result = "n/a"  

        check_detail = f"현재 적용된 보안 패치 정보: {security_patch_info}. MS SQL 최신 보안패치를 확인하고, 적용 영향도 평가를 실시하여 적용여부를 판단해야 함."
                
    except Exception as e:
        check_detail = f"보안 패치 정보 조회 중 오류 발생: {str(e)}"
        check_result = "n/a"  # 예외가 발생한 경우 결과를 'n/a'로 설정
    
    return no, check_detail, check_result
