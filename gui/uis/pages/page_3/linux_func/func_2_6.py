def check_func_2_6(client):
    no = "2_6"
    check_detail = ""
    check_result = "N/A"

    try:
        # /etc/xinetd.conf 파일의 소유자 및 권한 확인
        stdin, stdout, stderr = client.exec_command('ls -l /etc/xinetd.conf')
        xinetd_conf_info = stdout.read().decode('utf-8').strip()

        if xinetd_conf_info:
            check_detail = xinetd_conf_info
            parts = xinetd_conf_info.split()

            # 권한 및 소유자 추출
            permissions = parts[0]
            owner = parts[2]

            # 권한이 600인지 확인
            permission_valid = permissions[1] == 'r' and permissions[2] == 'w' and \
                               all(char == '-' for char in permissions[3:])

            # 소유자 확인 (root인지)
            if owner == 'root' and permission_valid:
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail = "/etc/xinetd.conf 파일 정보를 가져오지 못함"

    except Exception as e:
        check_detail = f"오류 발생: {str(e)}"
        check_result = "N/A"

    return no, check_detail, check_result
