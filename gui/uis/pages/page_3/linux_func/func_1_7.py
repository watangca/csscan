def check_func_1_7(client):
    no = "1_7"
    check_detail = ""
    check_result = "N/A"
    found_file = False  

    # 확인할 파일 리스트에 /etc/login.defs 추가
    files_to_check = [
        "/etc/login.defs",
        "/etc/security/pwquality.conf",
        "/etc/libuser.conf",
        "/etc/pam.d/system-auth",
        "/etc/pam.d/password-auth",
        "/etc/pam.d/common-password"
    ]

    # 패스워드 최소 길이 설정을 찾는 패턴을 확인할 수 있도록 변경
    patterns_to_check = {
        "/etc/login.defs": "PASS_MIN_LEN",
        "default": "minlen"
    }

    for file_path in files_to_check:
        try:
            # 파일의 존재 여부를 확인
            stdin, stdout, stderr = client.exec_command(f"test -f {file_path} && echo 'Exists'")
            if stdout.read().decode().strip() == 'Exists':
                found_file = True
                pattern = patterns_to_check.get(file_path, patterns_to_check["default"])

                # 파일에서 minlen 또는 PASS_MIN_LEN 값을 읽어옴
                stdin, stdout, stderr = client.exec_command(f"grep -E '^{pattern}' {file_path}")
                value_line = stdout.read().decode().strip()

                if value_line:
                    check_detail += f"{file_path}: {value_line}\n"
                    min_value = int(value_line.split()[-1].strip())

                    if min_value >= 8:
                        check_result = "양호"
                        break  # 적절한 값을 찾았으므로 루프 종료
                    else:
                        check_result = "취약"
                        break  # 최소 길이 요구사항을 충족하지 않으므로 루프 종료
                else:
                    # 설정 값을 명시적으로 찾지 못한 경우
                    check_detail += f"{file_path}에 {pattern} 설정되지 않음 (기본값: 6)\n"
                    check_result = "취약"
                    break  # 다음 파일로 넘어가지 않고 루프 종료
        except Exception as e:
            check_detail += f"{file_path} 파일을 확인하는 중 오류 발생: {str(e)}\n"
            continue  # 해당 파일에서 값을 찾지 못하면 다음 파일로 넘어감

    if not found_file:  # 설정 파일을 찾지 못한 경우
        check_detail = "설정 파일이 존재하지 않음"

    return no, check_detail.strip(), check_result
