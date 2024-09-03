def check_func_1_3(client):
    no = "1_3"
    check_detail = ""
    check_result = "N/A"

    config_files = ["/etc/pam.d/common-auth", "/etc/pam.d/system-auth", "/etc/pam.d/password-auth"]
    lock_threshold = None
    file_exist = False
    setting_found = False  # 설정이 발견되었는지 여부를 추적합니다.

    for file_path in config_files:
        try:
            stdin, stdout, stderr = client.exec_command(f'cat {file_path}')
            config_content = stdout.read().decode('utf-8')
            if config_content:
                file_exist = True
                for line in config_content.split('\n'):
                    if ("pam_tally2" in line or "pam_faillock" in line) and not line.strip().startswith("#"):
                        setting_found = True  # 설정이 한 줄이라도 발견되었다면 True로 설정
                        if "deny=" in line:
                            lock_threshold = int(line.split("deny=")[1].split()[0])
                            break  # 첫 번째 유효한 설정을 찾으면 반복을 중단합니다.

                if lock_threshold is not None:
                    break
            else:
                check_detail += f"{file_path}: 설정이 발견되지 않음\n"
        except:
            check_detail += f"{file_path} 파일이 존재하지 않음.\n"

    if not file_exist:
        check_result = "N/A"
    elif lock_threshold is None:
        if setting_found:
            check_detail += "계정 잠금 임계값 설정이 주석 처리됨 또는 deny= 값이 설정되지 않음"
        else:
            check_detail += "계정 잠금 설정이 발견되지 않음"
        check_result = "취약"
    elif lock_threshold > 10:
        check_detail = f"계정 잠금 임계값: {lock_threshold}회 (10회 이상으로 설정되어 취약)"
        check_result = "취약"
    else:
        check_detail = f"계정 잠금 임계값: {lock_threshold}회"
        check_result = "양호"

    return no, check_detail, check_result
