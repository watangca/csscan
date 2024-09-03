def check_func_2_7(client):
    no = "2_7"
    check_detail = ""
    check_result = "N/A"

    files_to_check = ['/etc/syslog.conf', '/etc/rsyslog.conf', '/etc/syslog-ng.conf']

    try:
        for file in files_to_check:
            stdin, stdout, stderr = client.exec_command(f'ls -l {file}')
            file_info = stdout.read().decode('utf-8').strip()

            if file_info and not file_info.startswith("ls:"):
                check_detail += f"{file} 정보: {file_info}\n"
                parts = file_info.split()

                # 권한 및 소유자 추출
                permissions = parts[0]
                owner = parts[2]

                # 권한이 640 이하인지 확인
                permission_valid = permissions[1] in ['r', '-'] and permissions[2] in ['w', '-'] and \
                                   all(char in ['-', 'r'] for char in permissions[3:6]) and \
                                   all(char == '-' for char in permissions[6:])

                # 소유자 확인 (root, bin, sys 중 하나인지)
                if owner in ['root', 'bin', 'sys'] and permission_valid:
                    check_result = "양호"
                else:
                    check_result = "취약"

    except Exception as e:
        check_detail = f"오류 발생: {str(e)}"
        check_result = "N/A"

    return no, check_detail.strip(), check_result
