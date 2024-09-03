def check_func_3_14(client):
    no = "3_14"
    check_detail = ""
    check_result = "n/a"

    # Sendmail 서비스 실행 여부 확인
    stdin, stdout, stderr = client.exec_command("ps -ef | grep sendmail | grep -v grep")
    output = stdout.read().decode()
    error = stderr.read().decode()

    if error:
        check_detail += "Sendmail 서비스 확인 중 오류 발생: " + error
    elif "sendmail" in output:
        check_detail += "Sendmail 서비스 실행 중\n"
        sendmail_running = True
    else:
        check_detail += "Sendmail 서비스 비활성화 됨\n"
        sendmail_running = False

    # /etc/sendmail.cf 파일에서 restrictqrun 옵션 확인
    if sendmail_running:
        stdin, stdout, stderr = client.exec_command("cat /etc/mail/sendmail.cf | grep 'O PrivacyOptions'")
        output = stdout.read().decode()
        error = stderr.read().decode()

        if "No such file or directory" in error:
            check_detail += "/etc/sendmail.cf 파일이 존재하지 않음\n"
            check_result = "양호"
        elif error:
            check_detail += "Sendmail 설정 파일 읽기 오류: " + error
        elif "restrictqrun" in output:
            check_detail += "Sendmail이 restrictqrun 옵션으로 설정되어 있음\n"
            check_result = "양호"
        else:
            check_detail += "Sendmail이 restrictqrun 옵션으로 설정되지 않음\n"
            check_result = "취약"
    else:
        check_result = "양호"

    return no, check_detail, check_result

