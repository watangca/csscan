def check_func_1_15(client):
    no = "1_15"
    policy_name = "네트워크 액세스: 익명 SID/이름 변환 허용"
    policy_setting = ""

    # 'secedit' 명령어를 사용하여 보안 설정을 내보내고, 결과를 분석
    export_command = "secedit /export /cfg secpol.cfg"
    client.run_cmd(export_command)

    # 생성된 'secpol.cfg' 파일을 읽어서 필요한 정보 추출
    get_policy_command = "type secpol.cfg"
    result = client.run_cmd(get_policy_command)

    # 'Network access: Allow anonymous SID/Name translation' 설정 값 찾기
    check_result = "n/a"
    for line in result.std_out.decode().split('\n'):
        if "LSAAnonymousNameLookup" in line:
            policy_value = line.split('=')[1].strip()
            if policy_value == "0":
                policy_setting = "사용 안 함"
                check_result = "양호"
            elif policy_value == "1":
                policy_setting = "사용"
                check_result = "취약"
            break

    check_detail = f"{policy_name}: {policy_setting}"
    return no, check_detail, check_result
