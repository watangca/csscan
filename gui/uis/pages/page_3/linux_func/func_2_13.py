def check_func_2_13(client):
    no = "2_13"
    check_detail = ""
    check_result = "N/A"

    try:
        # login, shell, exec 서비스 사용 확인
        services = ["login", "shell", "exec"]
        services_status = {service: False for service in services}
        for service in services:
            stdin, stdout, stderr = client.exec_command(f'chkconfig --list | grep {service}')
            output = stdout.read().decode('utf-8').strip()
            if output:
                services_status[service] = True

        check_detail += f"서비스 상태: {services_status}\n"

        # 파일 소유자 및 권한 확인
        files = ["/etc/hosts.equiv", "$HOME/.rhosts"]
        for file in files:
            stdin, stdout, stderr = client.exec_command(f'ls -l {file}')
            file_info = stdout.read().decode('utf-8').strip()
            if file_info:
                parts = file_info.split()
                permissions = parts[0]
                owner = parts[2]
                check_detail += f"{file} - 권한: {permissions}, 소유자: {owner}\n"
                if '+' in permissions or owner not in ['root', client.get_username()]:
                    check_result = "취약"
                    break
            else:
                check_detail += f"{file} 파일이 발견되지 않음\n"

        # 모든 점검 완료 후 결과 결정
        if check_result != "취약":
            if all(not status for status in services_status.values()):
                check_result = "양호"
            else:
                check_result = "취약"

    except Exception as e:
        check_detail = f"오류 발생: {str(e)}"
        check_result = "N/A"

    return no, check_detail, check_result