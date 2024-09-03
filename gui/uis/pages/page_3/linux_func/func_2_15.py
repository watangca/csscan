def check_func_2_15(client):
    no = "2_15"
    check_detail = ""
    check_result = "N/A"

    try:
        # /etc/hosts.lpd 파일의 속성을 검사합니다.
        stdin, stdout, stderr = client.exec_command('ls -l /etc/hosts.lpd')
        result = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()

        if result:
            # 파일이 존재하면, 파일 정보를 check_detail에 추가합니다.
            check_detail = result
            # 소유자가 root이고, 권한이 600인지 확인합니다.
            permissions, owner = result.split()[0], result.split()[2]
            if owner == 'root' and permissions == '-rw-------':
                check_result = "양호"
            else:
                check_result = "취약"
        elif 'No such file or directory' in error:
            # 파일이 존재하지 않으면 '양호'로 설정합니다.
            check_detail = "/etc/hosts.lpd 파일이 발견되지 않음"
            check_result = "양호"
        else:
            # 다른 오류가 발생하면 'N/A'로 설정합니다.
            check_detail = f"Error: {error}"
            check_result = "N/A"

    except Exception as e:
        check_detail = f"오류 발생: {str(e)}"
        check_result = "N/A"

    return no, check_detail, check_result