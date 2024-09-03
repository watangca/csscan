def check_func_1_14(client):
    no = "1_14"
    check_detail = ""
    check_result = "N/A"

    # 로그인이 불필요한 계정 리스트
    system_accounts = ['daemon', 'bin', 'sys', 'adm', 'listen', 'nobody', 'nobody4', 'noaccess', 'diag', 'operator', 'games', 'gopher']
    
    try:
        # /etc/passwd에서 계정과 쉘 정보 가져오기
        command = 'grep -E "^(' + '|'.join(system_accounts) + '):" /etc/passwd'
        stdin, stdout, stderr = client.exec_command(command)
        account_lines = stdout.read().decode().strip().split('\n')

        # 각 계정에 대해 쉘 설정 확인
        non_conforming_accounts = []
        for line in account_lines:
            parts = line.split(":")
            account, shell = parts[0], parts[-1]
            if shell not in ['/bin/false', '/usr/sbin/nologin']:
                non_conforming_accounts.append(account)

        # 결과 결정
        if non_conforming_accounts:
            check_detail += f"로그인 쉘이 /bin/false 또는 /usr/sbin/nologin으로 설정되지 않은 계정: {', '.join(non_conforming_accounts)}\n"
            check_detail += "해당 계정에 대해 /bin/false 또는 /usr/sbin/nologin 설정 필요"
            check_result = "취약"
        else:
            check_detail = "모든 시스템 계정에 로그인 쉘이 적절히 설정되어 있음 (/bin/false 또는 /usr/sbin/nologin)"
            check_result = "양호"

    except Exception as e:
        check_detail = f"계정 쉘 설정 확인 중 오류 발생: {e}"
        check_result = "N/A"

    return no, check_detail, check_result
