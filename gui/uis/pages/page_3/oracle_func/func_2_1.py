def check_func_2_1(oracle_conn):
    no = "2_1"
    # 초기 설정값, 줄바꿈을 사용하지 않음
    check_detail = "원격에서 db 서버로의 접속제한 설정값 출력 -"
    check_result = "n/a"  # 초기 상태는 평가 불가능으로 설정

    try:
        # Oracle DB의 REMOTE_OS_AUTHENT 설정 확인
        cursor = oracle_conn.cursor()
        query = "SELECT value FROM v$parameter WHERE name = 'remote_os_authent'"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            value = result[0]
            # 정보 추가 시 줄바꿈 대신 다른 구분자 사용 (예: ", ")
            check_detail += f" REMOTE_OS_AUTHENT 설정값: {value}"
            # REMOTE_OS_AUTHENT가 FALSE로 설정되어 있으면 양호
            if value == 'FALSE':
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            # 설정값을 찾을 수 없는 경우, 정보 추가 시 줄바꿈 대신 다른 구분자 사용
            check_detail += " REMOTE_OS_AUTHENT 설정값을 찾을 수 없습니다."
            check_result = "n/a"

    except Exception as e:
        # 오류 발생 시 정보 추가, 줄바꿈 대신 다른 구분자 사용
        check_detail += f" 오류 발생: {str(e)}"
        check_result = "n/a"

    finally:
        if 'cursor' in locals():
            cursor.close()

    return no, check_detail, check_result
