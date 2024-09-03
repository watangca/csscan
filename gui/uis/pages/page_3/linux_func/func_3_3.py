def check_func_3_3(client):
    no = "3_3"
    check_detail = ""
    check_result = "양호"
    service_installed = False

    try:
        # rsh, rlogin, rexec 서비스 확인
        services = ['rsh', 'rlogin', 'rexec']

        for service in services:
            # 서비스 설치 및 활성화 확인
            service_cmd = f"dpkg -l | grep -i {service} || rpm -q {service} || yum list installed | grep -i {service}"
            stdin, stdout, stderr = client.exec_command(service_cmd)
            output = stdout.read().decode('utf-8').strip()

            if "not installed" not in output.lower() and "no packages found" not in output.lower():
                service_installed = True

                # 서비스 활성화 확인
                service_cmd = f"systemctl is-active {service} || service {service} status"
                stdin, stdout, stderr = client.exec_command(service_cmd)
                output = stdout.read().decode('utf-8').strip()

                if "active" in output or "running" in output:
                    check_detail += f"{service} 서비스 활성화됨\n"
                    check_result = "취약"

        # 설치된 서비스가 없으면 n/a와 관련된 메시지 추가
        if not service_installed:
            check_result = "n/a"
            check_detail = "rsh, rlogin, rexec 서비스가 설치되지 않음"

    except Exception as e:
        check_detail = f"오류 발생: {str(e)}"
        check_result = "N/A"

    return no, check_detail, check_result
