def check_func_1_2(client):
    no = "1_2"
    check_detail = ""
    check_result = "취약"

    # /etc/security/pwquality.conf 파일 확인
    pwquality_conf_path = "/etc/security/pwquality.conf"
    try:
        stdin, stdout, stderr = client.exec_command(f'grep "minlen=" {pwquality_conf_path}')
        pwquality_config = stdout.read().decode('utf-8').strip()
        if pwquality_config:
            check_detail += f"{pwquality_conf_path}: {pwquality_config}\n"
            minlen = int(pwquality_config.split("=")[1])
            if minlen >= 8:
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail += f"{pwquality_conf_path}: minlen 설정값 없음\n"
            check_result = "취약"
    except:
        check_detail += f"{pwquality_conf_path} 파일이 존재하지 않습니다.\n"

    # PAM 관련 파일 확인
    pam_files = ["/etc/pam.d/common-password", "/etc/pam.d/system-auth", "/etc/pam.d/password-auth"]
    for pam_file in pam_files:
        try:
            stdin, stdout, stderr = client.exec_command(f'grep "pam_pwquality.so" {pam_file}')
            pam_config = stdout.read().decode('utf-8').strip()
            if pam_config:
                check_detail += f"{pam_file}: {pam_config}\n"
                if check_result != "취약":
                    check_result = "양호"
            else:
                check_detail += f"{pam_file}: pam_pwquality.so 설정값 없음\n"
                if check_result != "양호":
                    check_result = "취약"
        except:
            check_detail += f"{pam_file} 파일이 존재하지 않음\n"
            if check_result != "양호":
                check_result = "N/A"

    # 결과 반환
    return no, check_detail, check_result
