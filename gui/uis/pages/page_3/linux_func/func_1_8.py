def check_func_1_8(client):
    no = "1_8"
    check_detail = ""
    check_result = "N/A"

    # /etc/login.defs 파일에서 PASS_MAX_DAYS 설정 확인
    try:
        stdin, stdout, stderr = client.exec_command('grep "^PASS_MAX_DAYS" /etc/login.defs')
        login_defs_config = stdout.read().decode('utf-8').strip()
        if login_defs_config:
            # 설정값을 파싱하여 숫자만 추출
            max_days = int(login_defs_config.split()[1])
            check_detail += f"/etc/login.defs: PASS_MAX_DAYS {max_days}\n"
            if max_days <= 90:
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail += "/etc/login.defs: PASS_MAX_DAYS 설정값 없음\n"
            check_result = "취약"
    except Exception as e:
        check_detail += f"/etc/login.defs 파일을 확인하는 중 오류가 발생했습니다: {e}\n"
        check_result = "N/A"

    # /etc/shadow 파일에서 사용자별 패스워드 최대 사용기간 확인 (선택적)
    try:
        stdin, stdout, stderr = client.exec_command('grep -E "^[^:]+:[^!*]:" /etc/shadow')
        shadow_entries = stdout.read().decode('utf-8').strip().split('\n')
        for entry in shadow_entries:
            fields = entry.split(':')
            if len(fields) > 4:
                username = fields[0]
                max_days = int(fields[4])
                if max_days > 90:
                    check_detail += f"/etc/shadow: {username} 패스워드 최대 사용기간 {max_days}일\n"
                    check_result = "취약"
    except Exception as e:
        check_detail += f"/etc/shadow 파일을 확인하는 중 오류가 발생했습니다: {e}\n"
        # /etc/shadow 파일 확인 오류는 check_result를 변경하지 않습니다.

    return no, check_detail, check_result
