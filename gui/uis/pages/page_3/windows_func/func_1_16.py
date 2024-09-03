def check_func_1_16(client):
    no = "1_16"
    policy_name = "최근 암호 기억"

    # 'secedit' 명령어를 사용하여 보안 설정을 내보내고, 결과를 분석
    export_command = "secedit /export /cfg secpol.cfg"
    client.run_cmd(export_command)

    # 생성된 'secpol.cfg' 파일을 읽어서 필요한 정보 추출
    get_policy_command = "type secpol.cfg"
    result = client.run_cmd(get_policy_command)

    # 'PasswordHistorySize' 설정 값 찾기
    check_result = "n/a"
    policy_setting = ""
    for line in result.std_out.decode().split('\n'):
        if "PasswordHistorySize" in line:
            password_history_size = int(line.split('=')[1].strip())
            policy_setting = f"{password_history_size} 개"
            if password_history_size >= 4:
                check_result = "양호"
            else:
                check_result = "취약"
            break

    check_detail = f"{policy_name}: {policy_setting}"
    return no, check_detail, check_result
