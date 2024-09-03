def check_func_2_6(client):
    no = "2_6"
    check_detail = "시스템 umask 설정값"
    check_result = "n/a"  # 기본값 설정

    try:
        # SSH를 통해 원격 서버에 umask 값을 확인하는 명령어 실행
        stdin, stdout, stderr = client.exec_command('umask')
        umask_value = stdout.read().decode('utf-8').strip()

        # umask 값을 출력 형식에 맞추어 조정
        check_detail = f"시스템 umask 설정값: {umask_value}"

        # umask 값이 022 이상인지 확인
        if int(umask_value, 8) >= 0o022:
            check_result = "양호"
        else:
            check_result = "취약"

    except Exception as e:
        # SSH 연결 실패 또는 명령어 실행 오류 처리
        check_detail = f"umask 값 확인 중 오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result