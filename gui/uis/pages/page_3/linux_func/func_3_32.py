def check_func_3_32(client):
    no = "3_32"
    check_detail = ""
    check_result = "양호"  # 처음에는 양호로 설정

    # 점검할 파일 및 관련 설정 확인 커맨드 목록
    files_and_commands = [
        ("/etc/motd", 'cat /etc/motd'),
        ("/etc/issue.net", 'cat /etc/issue.net'),
        ("/etc/vsftpd/vsftpd.conf", 'grep "ftpd_banner" /etc/vsftpd/vsftpd.conf'),
        ("/etc/mail/sendmail.cf", 'grep "^O SmtpGreetingMessage" /etc/mail/sendmail.cf'),
        ("/etc/named.conf", 'grep "options {.*};" /etc/named.conf')  # 예시, 실제 배너 메시지 설정 커맨드는 환경에 따라 다를 수 있음
    ]

    try:
        for file_path, command in files_and_commands:
            stdin, stdout, stderr = client.exec_command(command)
            content = stdout.read().decode('utf-8').strip()
            error = stderr.read().decode('utf-8').strip()

            if error:
                check_detail += f"{file_path} 파일 확인 중 오류 발생: {error}\n"
                # 파일이 없거나 읽을 수 없는 경우에도 취약으로 판단
                check_result = "취약"
            elif content:
                check_detail += f"{file_path} 경고메시지 설정 내용: \n{content}\n"
            else:
                check_detail += f"{file_path} 파일에 경고메시지 설정이 없음\n"
                check_result = "취약"
                break  # 하나라도 설정이 없으면 즉시 취약 판정 후 반복 중단

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
