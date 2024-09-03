def check_func_3_2(client):
    no = "3_2"
    check_detail = ""
    check_result = "양호"  # 기본값을 "양호"로 설정하고, 익명 접속이 허용된 경우에만 "취약"으로 변경

    # OS 확인
    stdin, stdout, stderr = client.exec_command("cat /etc/*release")
    os_info = stdout.read().decode('utf-8').lower()

    # 패키지 관리자 명령어 결정
    if "ubuntu" in os_info or "debian" in os_info:
        pkg_check_command = "dpkg -l"
    elif "centos" in os_info or "red hat" in os_info or "fedora" in os_info or "amazon linux" in os_info:
        pkg_check_command = "rpm -q"
    else:
        return no, "지원하지 않는 OS", "n/a"

    # FTP 서비스 목록
    ftp_services = ["vsftpd", "proftpd"]

    for service in ftp_services:
        # 패키지 설치 여부 확인
        stdin, stdout, stderr = client.exec_command(f"{pkg_check_command} {service}")
        pkg_output = stdout.read().decode('utf-8')

        if service in pkg_output:
            # 익명 FTP 접속 설정 확인
            config_check_command = f"grep -i 'anonymous_enable' /etc/{service}/{service}.conf"
            stdin, stdout, stderr = client.exec_command(config_check_command)
            config_output = stdout.read().decode('utf-8')

            if "anonymous_enable=YES" in config_output:
                check_result = "취약"
                check_detail += f"{service} 설치됨, 익명 FTP 접속 허용\n"
            else:
                check_detail += f"{service} 설치됨, 익명 FTP 접속 차단\n"
        else:
            check_detail += f"{service} 미설치\n"

    if check_detail == "":
        check_detail = "FTP 서비스 패키지가 설치되지 않음"
        check_result = "양호"

    return no, check_detail.strip(), check_result
