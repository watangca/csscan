def check_func_5_12(client):
    no = "5_12"
    registry_path = "HKLM\\Software\\Policies\\Microsoft\\Windows NT\\Printers"
    policy_name = "DisablePrinterDriverInstallation"
    check_detail = "사용자가 프린터 드라이버를 설치할 수 없게 함 설정 확인: "

    # 원격 시스템에서 해당 정책 확인을 위한 PowerShell 명령어
    policy_command = f"""
    try {{
        $policyValue = (Get-ItemProperty -Path Registry::{registry_path} -Name {policy_name} -ErrorAction Stop).{policy_name}
    }} catch {{
        $policyValue = 'Not Set'
    }}
    return $policyValue
    """

    try:
        policy_response = client.run_ps(policy_command)

        if policy_response.status_code == 0:
            policy_value = policy_response.std_out.decode('utf-8').strip()

            if policy_value == "":
                policy_value = "Not Set"

            check_detail += f"{policy_value}"

            # 정책 값에 따라 결과 설정
            if policy_value == "1":
                check_result = "양호"
            elif policy_value == "0" or policy_value == "Not Set":
                check_result = "취약"
            else:
                check_result = "n/a"
        else:
            check_detail += f"명령 실행 오류: {policy_response.std_err.decode('utf-8')}"
            check_result = "취약"

    except Exception as e:
        check_detail += f"\nException: {str(e)}"
        check_result = "취약"

    return no, check_detail, check_result
