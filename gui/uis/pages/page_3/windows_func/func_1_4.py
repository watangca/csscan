def check_func_1_4(client):
    no = "1_4"
    check_detail = "원도우 서버의 모든 계정의 잠금 임계값: "
    check_result = "n/a"

    # 계정 잠금 임계값을 확인하는 PowerShell 명령
    ps_command_threshold = "net accounts | Select-String 'Lockout threshold'"
    ps_command_users = "Get-LocalUser | Select-Object -ExpandProperty 'Name'"

    try:
        # 원격 서버에서 계정 잠금 임계값을 가져옴
        result_threshold = client.run_ps(ps_command_threshold)
        result_users = client.run_ps(ps_command_users)

        if result_threshold.status_code == 0 and result_users.status_code == 0:
            # 잠금 임계값 추출
            lockout_threshold_line = result_threshold.std_out.decode().strip()
            lockout_threshold_value = lockout_threshold_line.split(':')[1].strip()
            if not lockout_threshold_value.isdigit():
                lockout_threshold_value = "설정안됨"  # 임계값이 설정되지 않았을 때

            # 모든 사용자 계정 추출
            user_list = result_users.std_out.decode().strip().split('\n')

            # 각 계정별로 잠금 임계값 할당
            for user in user_list:
                user = user.strip()
                check_detail += f"{user}: 임계값 {lockout_threshold_value}, "

            # 마지막 콤마 제거
            check_detail = check_detail.rstrip(', ')

            # 임계값 판단
            if lockout_threshold_value == "설정안됨" or int(lockout_threshold_value) > 5:
                check_result = "취약"
            elif int(lockout_threshold_value) <= 5:
                check_result = "양호"
        else:
            check_detail += "계정 잠금 임계값을 확인하는 데 실패했습니다."
            check_result = "취약"

    except Exception as e:
        check_detail += f"계정 잠금 임계값 확인 중 오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result

