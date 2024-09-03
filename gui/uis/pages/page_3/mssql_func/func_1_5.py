def check_func_1_5(win_conn):
    no = "1_5"
    check_detail = "패스워드 재사용 정책 설정: "
    check_result = "n/a"

    # secedit을 사용하여 보안 정책을 내보내고, 필요한 정보를 추출합니다.
    ps_script = "$pol = secedit /export /cfg $env:temp\\secpol.cfg; Get-Content -Path $env:temp\\secpol.cfg | Select-String 'PasswordHistorySize', 'MinimumPasswordAge'"
    result = win_conn.run_ps(ps_script)

    try:
        if result.status_code == 0:
            policies = result.std_out.decode().split('\n')
            passwordHistorySize = None
            minimumPasswordAge = None
            for policy in policies:
                if 'PasswordHistorySize' in policy:
                    passwordHistorySize = int(policy.split('=')[1].strip())
                    check_detail += f"PasswordHistorySize = {passwordHistorySize}, "
                elif 'MinimumPasswordAge' in policy:
                    minimumPasswordAge = int(policy.split('=')[1].strip())
                    check_detail += f"MinimumPasswordAge = {minimumPasswordAge}, "

            # 마지막 쉼표 제거
            check_detail = check_detail[:-2]

            # 설정값을 기반으로 결과 판단
            if passwordHistorySize is not None and minimumPasswordAge is not None:
                if passwordHistorySize > 0 and minimumPasswordAge > 0:
                    check_result = "양호"
                else:
                    check_result = "취약"
            else:
                check_result = "취약"
        else:
            check_detail += "패스워드 정책 확인 실패"
            check_result = "n/a"

    except Exception as e:
        check_detail = f"오류 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result
