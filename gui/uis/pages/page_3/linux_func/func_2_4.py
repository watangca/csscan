def check_func_2_4(client):
    no = "2_4"
    check_detail = ""
    check_result = "N/A"

    try:
        # /etc/shadow 파일의 소유자 및 권한 확인
        stdin, stdout, stderr = client.exec_command('ls -l /etc/shadow')
        shadow_info = stdout.read().decode('utf-8').strip()

        if shadow_info:
            check_detail = shadow_info
            parts = shadow_info.split()

            # 권한 및 소유자 추출
            permissions = parts[0]
            owner = parts[2]

            # 권한이 400 이하인지 확인
            permission_valid = permissions[1] == 'r' and all(char == '-' for char in permissions[2:])

            # 소유자 확인 (root인지)
            if owner == 'root' and permission_valid:
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail = "/etc/shadow 파일 정보를 가져오지 못함"

    except Exception as e:
        check_detail = f"오류 발생: {str(e)}"
        check_result = "N/A"

    return no, check_detail, check_result
