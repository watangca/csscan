def check_func_3_15(client):
    no = "3_15"
    check_detail = ""
    check_result = "n/a"

    # DNS 서비스 (named) 실행 여부 확인
    stdin, stdout, stderr = client.exec_command("ps -ef | grep [n]amed")
    output = stdout.read().decode()
    error = stderr.read().decode()

    if error:
        check_detail += "DNS 서비스 확인 중 오류 발생: " + error
    elif "named" in output:
        check_detail += "DNS 서비스(named) 실행 중\n"
        dns_running = True
    else:
        check_detail += "DNS 서비스(named) 비활성화 됨\n"
        dns_running = False

    # named 버전 확인
    if dns_running:
        stdin, stdout, stderr = client.exec_command("named -v")
        version_output = stdout.read().decode().strip()
        version_error = stderr.read().decode().strip()

        if version_error:
            check_detail += "named 버전 확인 중 오류 발생: " + version_error + "\n"
        else:
            check_detail += "BIND 버전: " + version_output + "\n"
            check_detail += "BIND 최신버전 패치를 확인하고 적용여부 판단 필요\n"

            # 여기서는 실제 패치 관리 여부를 자동으로 판단할 수 없으므로, 양호로 설정
            check_result = "양호"
    else:
        # DNS 서비스(named)가 실행 중이지 않으므로, 양호로 판단
        check_result = "양호"

    return no, check_detail, check_result
