def check_func_1_9(client):
    no = "1_9"
    check_detail = ""
    check_result = "N/A"

    try:
        # 원격 시스템의 /etc/login.defs 파일에서 PASS_MIN_DAYS 설정 확인
        stdin, stdout, stderr = client.exec_command('grep "^PASS_MIN_DAYS" /etc/login.defs')
        login_defs_config = stdout.read().decode('utf-8').strip()
        if login_defs_config:
            # 설정값을 파싱하여 숫자만 추출
            min_days = int(login_defs_config.split()[1])
            check_detail = f"패스워드 최소 사용기간 설정값: {min_days}일"
            if min_days >= 1:
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail = "패스워드 최소 사용기간 설정값 없음"
            check_result = "취약"
    except Exception as e:
        check_detail += f"/etc/login.defs 파일을 확인하는 중 오류가 발생했습니다: {e}"
        check_result = "N/A"

    return no, check_detail, check_result