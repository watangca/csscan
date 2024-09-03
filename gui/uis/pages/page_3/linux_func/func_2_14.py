def check_func_2_14(client):
    no = "2_14"
    check_detail = ""
    check_result = "양호"  # 기본적으로 양호로 설정

    files_to_check = [
        "/etc/hosts.deny",
        "/etc/hosts.allow",
        "/etc/sysconfig/iptables",
        "/etc/iptables/rules.v4"
    ]

    try:
        for file in files_to_check:
            stdin, stdout, stderr = client.exec_command(f'cat {file}')
            content = stdout.read().decode('utf-8').strip()

            # 파일 내용에서 'ALL: ALL' 또는 '-j ACCEPT'가 포함된 줄을 찾습니다.
            if 'ALL: ALL' in content or '-j ACCEPT' in content:
                check_result = "취약"
                check_detail += f"{file}: 'ALL: ALL' or '-j ACCEPT' 설정 발견\n"
            else:
                # 취약한 설정이 없을 경우에는 해당 파일에서의 취약한 설정이 없음을 기록합니다.
                check_detail += f"{file}: 'ALL: ALL' or '-j ACCEPT' 등의 취약한 설정이 발견되지 않음\n"

    except Exception as e:
        check_detail = f"오류 발생: {str(e)}"
        check_result = "N/A"

    return no, check_detail, check_result