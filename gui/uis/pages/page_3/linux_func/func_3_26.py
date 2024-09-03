def check_func_3_26(client):
    no = "3_26"
    check_detail = ""
    check_result = "양호"

    try:
        # FTP 서비스 계정 확인 (일반적으로 'ftp')
        stdin, stdout, stderr = client.exec_command("grep '^ftp:' /etc/passwd")
        ftp_info = stdout.read().decode('utf-8').strip()

        if ftp_info:
            # ftp 계정의 쉘 정보 추출
            shell = ftp_info.split(":")[-1]
            check_detail += f"FTP 계정 정보: {ftp_info}\n"

            if shell != "/bin/false":
                check_result = "취약"
        else:
            check_detail += "FTP 계정이 존재하지 않음"
    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
