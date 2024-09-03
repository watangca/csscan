def check_func_3_13(client):
    no = "3_13"
    check_detail = "SMTP 서비스 사용 여부 및 릴레이 제한 옵션 확인:\n"
    check_result = "n/a"

    # SMTP 서비스 (sendmail) 실행 여부 점검
    service_command = "ps -ef | grep [s]endmail"
    stdin, stdout, stderr = client.exec_command(service_command)
    service_output = stdout.read().decode().strip()

    if service_output:
        check_detail += "Sendmail 서비스 실행 중.\n"
        service_running = True
    else:
        check_detail += "Sendmail 서비스가 실행중이 아님.\n"
        service_running = False

    if service_running:
        # /etc/mail/sendmail.cf 파일에서 릴레이 제한 설정 확인
        config_command = "grep 'R$\\*' /etc/mail/sendmail.cf | grep 'Relaying denied'"
        stdin, stdout, stderr = client.exec_command(config_command)
        config_output = stdout.read().decode().strip()

        if config_output:
            check_detail += f"릴레이 제한 설정 발견: {config_output}\n"
            check_result = "양호"
        else:
            check_detail += "릴레이 제한 설정이 발견되지 않음.\n"
            check_result = "취약"
    else:
        # Sendmail 서비스가 실행되지 않으면 양호로 간주
        check_result = "양호"

    return no, check_detail, check_result
