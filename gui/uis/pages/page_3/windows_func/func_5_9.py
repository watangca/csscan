def check_func_5_9(client):
    no = "5_9"
    registry_path = "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\RemovableStorageDevices"
    policy_name = "Deny_All"
    check_detail = "이동식 미디어 포맷 및 꺼내기 허용 정책 설정 확인: "

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

            check_detail += policy_value

            # 정책 값에 따라 결과 설정
            if policy_value == "Administrator":
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail += f"명령 실행 오류: {policy_response.std_err.decode('utf-8')}"
            check_result = "취약"

    except Exception as e:
        check_detail += f"\nException: {str(e)}"
        check_result = "취약"

    return no, check_detail, check_result
