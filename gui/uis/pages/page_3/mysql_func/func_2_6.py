def check_func_2_6(client):
    no = "2_6"
    check_detail = "umask 값 확인 불가."
    check_result = "n/a"

    # client는 이미 설정된 paramiko SSHClient 객체입니다.
    try:
        # umask 값을 가져오기 위한 명령어 실행
        stdin, stdout, stderr = client.exec_command('umask')
        umask_value = stdout.read().decode().strip()

        # umask 값 출력
        check_detail = f"설정된 umask 값: {umask_value}"

        # umask 값이 022 이상인지 확인
        if int(umask_value, 8) >= 0o022:
            check_result = "양호"
        else:
            check_result = "취약"

    except Exception as e:
        # SSH 명령 실행 중 에러 발생 시
        check_detail = f"umask 값을 가져오는 중 에러 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
