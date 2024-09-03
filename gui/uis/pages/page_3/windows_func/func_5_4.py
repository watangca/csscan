def check_func_5_4(client):
    no = "5_4"
    check_detail = ""
    check_result = "n/a"

    # 비로그온 사용자의 시스템 종료 허용 여부 확인을 위한 PowerShell 명령어
    shutdown_without_logon_command = "Get-ItemProperty -Path 'HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name ShutdownWithoutLogon | Select-Object -ExpandProperty ShutdownWithoutLogon"

    try:
        response = client.run_ps(shutdown_without_logon_command)
        if response.status_code == 0 and response.std_out:
            # PowerShell 명령어의 결과 추출 및 파싱
            shutdown_without_logon_value = response.std_out.decode('utf-8').strip()

            check_detail = f"ShutdownWithoutLogon 설정값: {shutdown_without_logon_value}"
            # 'ShutdownWithoutLogon' 값이 0이면 양호, 그 외의 경우 취약
            if shutdown_without_logon_value == "0":
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail = "ShutdownWithoutLogon 설정을 확인할 수 없음"

    except Exception as e:
        check_detail = f"Error: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result