def check_func_3_11(client):
    no = "3_11"
    check_detail = ""
    check_result = "N/A"

    services = ["tftp", "talk", "ntalk"]
    services_status = {} 

    # 각 서비스의 상태 확인
    for service in services:
        command = f"systemctl is-active {service}"
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode().strip()

        # 서비스 상태 저장
        services_status[service] = output
        check_detail += f"{service} 서비스 상태: {output}\n"

    # 최종 결과 판단
    if any(status == "active" for status in services_status.values()):
        check_result = "취약"
    else:
        check_result = "양호"

    return no, check_detail.strip(), check_result
