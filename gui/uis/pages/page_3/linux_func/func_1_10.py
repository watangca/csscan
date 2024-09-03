import datetime

def check_func_1_10(client):
    no = "1_10"
    check_detail = ""
    check_result = "N/A"
    # 기본계정 목록
    default_accounts = ['lp', 'uucp', 'nuucp']
    # 현재 날짜에서 6개월(180일)을 빼서 기준 날짜를 계산
    cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=180)).strftime('%Y-%m-%d')

    try:
        # 원격 시스템에서 사용자 목록 확인
        stdin, stdout, stderr = client.exec_command('cat /etc/passwd')
        passwd_output = stdout.read().decode('utf-8').strip()

        # 원격 시스템에서 lastlog 명령을 실행하여 마지막 로그인 정보 확인
        stdin, stdout, stderr = client.exec_command('lastlog -b 180')
        lastlog_output = stdout.read().decode('utf-8').strip()

        # 기본 계정 존재 여부 확인
        existing_default_accounts = []
        for account in default_accounts:
            if account in passwd_output:
                existing_default_accounts.append(account)

        # 6개월 동안 로그인하지 않은 계정 확인
        inactive_accounts = []
        for line in lastlog_output.split('\n')[1:]:  # 첫 번째 줄은 헤더이므로 제외
            parts = line.split()
            if parts and len(parts) > 0:
                last_login = parts[-1]
                if last_login != 'Never' and last_login < cutoff_date:
                    inactive_accounts.append(parts[0])

        # 결과 상세 내용 작성
        if existing_default_accounts:
            check_detail += f"발견된 OS 기본 계정: {', '.join(existing_default_accounts)}\n"
            check_result = "취약"
        elif inactive_accounts:
            check_detail += f"6개월 동안 사용되지 않은 계정: {', '.join(inactive_accounts)}\n"
            check_result = "취약"
        else:
            check_detail += "기본 계정이나 사용되지 않은 계정이 없습니다.\n"
            check_result = "양호"

    except Exception as e:
        check_detail += f"계정을 확인하는 중 오류가 발생했습니다: {e}\n"
        check_result = "N/A"

    return no, check_detail, check_result

