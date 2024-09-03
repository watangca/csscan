def check_func_3_5(client):
    no = "3_5"
    check_detail = ""
    services_check_result = []

    # 리눅스 배포판 확인
    stdin, stdout, stderr = client.exec_command('cat /etc/*release')
    distro_info = stdout.read().decode('utf-8').lower()

    # xinetd 서비스의 설치 여부를 확인합니다.
    check_cmd = 'dpkg -l | grep xinetd || rpm -q xinetd'
    stdin, stdout, stderr = client.exec_command(check_cmd)
    output = stdout.read().decode('utf-8').strip()

    # xinetd가 설치되어 있지 않으면, 검사를 진행하지 않습니다.
    if 'xinetd' not in output:
        return no, "xinetd 서비스가 설치되지 않음", "n/a"

    services = ['echo', 'discard', 'daytime', 'chargen']
    for service in services:
        # 서비스 파일에서 'disable = yes' 설정을 확인합니다.
        command_yes = f'grep -E "^\\s*disable\\s*=\\s*yes" /etc/xinetd.d/{service} 2>/dev/null'
        stdin, stdout, stderr = client.exec_command(command_yes)
        service_config_yes = stdout.read().decode('utf-8').strip()

        # 서비스 파일에서 'disable = no' 설정을 확인합니다.
        command_no = f'grep -E "^\\s*disable\\s*=\\s*no" /etc/xinetd.d/{service} 2>/dev/null'
        stdin, stdout, stderr = client.exec_command(command_no)
        service_config_no = stdout.read().decode('utf-8').strip()

        if service_config_no:
            services_check_result.append(f"{service} 서비스 활성화됨")
        elif service_config_yes:
            services_check_result.append(f"{service} 서비스 비활성화됨")
        else:
            services_check_result.append(f"{service} 서비스의 disable 설정을 확인할 수 없음")

    # 검사 결과 결정
    if any("활성화됨" in result for result in services_check_result):
        check_result = "취약"
    else:
        check_result = "양호"

    check_detail = "\n".join(services_check_result)
    return no, check_detail.strip(), check_result
