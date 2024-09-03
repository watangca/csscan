def check_func_4_4(client):
    no = "4_4"
    check_detail = ""
    check_result = "양호"

    # 로그 디렉토리 경로
    system_log_dir = "%systemroot%\\system32\\config"
    iis_log_dir = "%systemroot%\\system32\\LogFiles"

    # Everyone 권한 확인을 위한 PowerShell 명령어
    system_log_command = f"Get-Acl -Path '{system_log_dir}' | Select-Object -ExpandProperty Access | Where-Object {{ $_.IdentityReference -eq 'Everyone' }}"
    iis_log_command = f"Get-Acl -Path '{iis_log_dir}' | Select-Object -ExpandProperty Access | Where-Object {{ $_.IdentityReference -eq 'Everyone' }}"

    try:
        # 시스템 로그 디렉토리 권한 확인
        system_log_response = client.run_ps(system_log_command)
        # IIS 로그 디렉토리 권한 확인
        iis_log_response = client.run_ps(iis_log_command)

        # Everyone 권한 존재 여부 확인 및 상세 정보 기록
        if system_log_response.std_out:
            check_detail += f"System Log Directory '{system_log_dir}' has Everyone permission.\n"
            check_result = "취약"
        if iis_log_response.std_out:
            check_detail += f"IIS Log Directory '{iis_log_dir}' has Everyone permission.\n"
            check_result = "취약"

        if check_detail == "":
            check_detail = "로그 디렉토리에 'everyone' 권한 발견되지 않음"

    except Exception as e:
        check_detail = f"Error: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
