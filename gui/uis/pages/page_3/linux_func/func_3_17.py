def check_func_3_17(client):
    no = "3_17"
    check_detail = ""
    check_result = "n/a"

    # Apache 서비스 실행 여부 확인
    cmd = "ps -ef | grep apache2 | grep -v grep"
    stdin, stdout, stderr = client.exec_command(cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()

    if error:
        check_detail += f"Apache 서비스 확인 중 오류 발생: {error}\n"
    elif output:
        check_detail += "Apache 웹 서비스 실행중\n"
        webserver_running = True
    else:
        check_detail += "실행 중인 Apache 웹 서버가 없음\n"
        webserver_running = False

    if webserver_running:
        # Apache의 디렉토리 검색 기능 설정 확인
        config_files = ["/etc/apache2/apache2.conf", "/etc/httpd/conf/httpd.conf"]
        found = False
        for config_file in config_files:
            check_cmd = f"cat {config_file} | grep -E 'Options.*Indexes'"
            stdin, stdout, stderr = client.exec_command(check_cmd)
            config_output = stdout.read().decode()
            config_error = stderr.read().decode()

            if config_output:
                check_detail += f"Apache 디렉토리 검색 설정 ({config_file}): \n{config_output}\n"
                check_result = "취약"
                found = True
                break
            elif config_error:
                check_detail += f"Apache 디렉토리 검색 설정 확인 중 오류 발생: {config_error}\n"

        if not found:
            check_detail += "Apache 디렉토리 검색 기능을 사용하지 않음\n"
            check_result = "양호"

    return no, check_detail, check_result
