def check_func_3_34(client):
    no = "3_34"
    check_detail = ""
    check_result = "n/a"

    try:
        # /etc/mail/sendmail.cf 파일에서 PrivacyOptions 확인
        config_file_path = "/etc/mail/sendmail.cf"
        stdin, stdout, stderr = client.exec_command(f'grep "PrivacyOptions" {config_file_path}')
        privacy_options = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()

        if error:
            check_detail += f"{config_file_path} 파일 확인 중 오류 발생: {error}"
            check_result = "n/a"
        elif privacy_options:
            check_detail += f"PrivacyOptions 설정: {privacy_options}\n"
            if 'noexpn' in privacy_options and 'novrfy' in privacy_options:
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail += f"{config_file_path} 파일에서 PrivacyOptions 설정을 찾을 수 없습니다."
            check_result = "취약"

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
