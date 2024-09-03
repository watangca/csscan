def check_func_3_16(client):
    no = "3_16"
    check_detail = ""
    check_result = "n/a"

    # DNS 서비스 (named) 실행 여부 확인
    stdin, stdout, stderr = client.exec_command("ps -ef | grep [n]amed")
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()

    if error:
        check_detail += "DNS 서비스 확인 중 오류 발생: " + error + "\n"
    elif output:
        check_detail += "DNS 서비스(named) 실행 중\n"
        dns_running = True
    else:
        check_detail += "DNS 서비스(named) 비활성화\n"
        dns_running = False

    # DNS 서비스가 실행 중인 경우, allow-transfer 설정 확인
    if dns_running:
        named_conf_paths = ["/etc/named.conf", "/etc/bind/named.conf"]
        for conf_path in named_conf_paths:
            stdin, stdout, stderr = client.exec_command(f"cat {conf_path} 2>/dev/null")
            conf_content = stdout.read().decode().strip()

            if conf_content:
                if 'allow-transfer' in conf_content:
                    # allow-transfer 설정이 있는 경우, 구체적 내용 출력
                    check_detail += f"{conf_path}에서 'allow-transfer' 설정 발견:\n"
                    stdin, stdout, stderr = client.exec_command(f"grep 'allow-transfer' {conf_path}")
                    allow_transfer_config = stdout.read().decode().strip()
                    check_detail += allow_transfer_config + "\n"
                    check_result = "양호"  # 기본적으로 양호로 설정, 세부 내용에 따라 달라질 수 있음
                else:
                    check_detail += f"{conf_path}에서 'allow-transfer' 설정을 찾을 수 없음\n"
                break  # 첫 번째로 발견된 named.conf 파일에서 설정을 찾으면 검색 중단
            else:
                check_detail += f"{conf_path} 파일을 찾을 수 없음\n"

        if check_result == "n/a":
            check_detail += "적절한 'allow-transfer' 설정을 찾을 수 없음\n"
    else:
        check_result = "양호"  # DNS 서비스(named)가 비활성화되었으므로, 양호로 판단

    return no, check_detail, check_result
