def check_func_3_25(client):
    no = "3_25"
    check_detail = ""
    check_result = "양호"

    try:
        ftp_services = ["ftp", "vsftpd", "proftpd"]
        active_services = []

        for service in ftp_services:
            # 각 FTP 서비스의 활성 여부 확인
            stdin, stdout, stderr = client.exec_command(f'ps -ef | grep {service} | grep -v grep')
            service_output = stdout.read().decode('utf-8').strip()

            if service_output:
                active_services.append(service)
                check_detail += f"{service} 서비스가 활성화되어 있음: {service_output}\n"

        if active_services:
            check_result = "취약"
        else:
            check_detail += "FTP 서비스가 비활성화되어 있음"

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
