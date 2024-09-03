def check_func_5_8(client):
    no = "5_8"
    registry_path = "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon"
    check_detail = "Autologon 설정 확인: "

    # 원격 시스템에서 Autologon 설정 확인을 위한 PowerShell 명령어
    policy_command = f"""
    $registryPath = '{registry_path}'
    try {{
        $autoAdminLogon = (Get-ItemProperty -Path Registry::$registryPath -Name AutoAdminLogon -ErrorAction Stop).AutoAdminLogon
    }} catch {{
        $autoAdminLogon = 'Not Set'
    }}
    return $autoAdminLogon
    """

    try:
        policy_response = client.run_ps(policy_command)

        if policy_response.status_code == 0:
            auto_admin_logon = policy_response.std_out.decode('utf-8').strip()

            if auto_admin_logon == "":
                auto_admin_logon = "Not Set"

            check_detail += f"AutoAdminLogon: {auto_admin_logon}"

            # AutoAdminLogon 값이 '1'인 경우 '취약', '0'이거나 'Not Set'인 경우 '양호'
            if auto_admin_logon == "1":
                check_result = "취약"
            elif auto_admin_logon in ["0", "Not Set"]:
                check_result = "양호"
            else:
                check_result = "n/a"
        else:
            check_detail += f"명령 실행 오류: {policy_response.std_err.decode('utf-8')}"
            check_result = "n/a"

    except Exception as e:
        check_detail += f"\nException: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
