def check_func_3_10(client):
    no = "3_10"
    check_result = "n/a"

    # NIS 서비스 상태 확인
    commands = ["systemctl is-active ypserv", "service nis status"]
    service_status = None

    for command in commands:
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode().strip()

        # 서비스 상태 확인
        if "active" in output or "running" in output:
            service_status = "active"
            break
        elif "inactive" in output or "failed" in output:
            service_status = output  
            break

    # 서비스 상태에 따른 결과 설정
    if service_status == "active":
        check_result = "취약"
    elif service_status in ["inactive", "failed"]:
        check_result = "양호"

    check_detail = f"NIS 서비스 상태: {service_status if service_status else '확인할 수 없음'}"

    return no, check_detail, check_result
