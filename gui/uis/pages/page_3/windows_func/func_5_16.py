def check_func_5_16(client):
    no = "5_16"
    registry_path = "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Lsa"
    check_detail = "LAN Manager 인증 수준 설정 확인: "

    # 원격 시스템에서 LAN Manager 인증 수준 설정 확인을 위한 PowerShell 명령어
    policy_command = f"""
    try {{
        $lmCompatibilityLevel = (Get-ItemProperty -Path Registry::{registry_path} -Name 'LmCompatibilityLevel' -ErrorAction Stop).LmCompatibilityLevel
    }} catch {{
        $lmCompatibilityLevel = 'Not Set'
    }}
    return $lmCompatibilityLevel
    """

    try:
        policy_response = client.run_ps(policy_command)

        if policy_response.status_code == 0:
            lm_compatibility_level = policy_response.std_out.decode('utf-8').strip()
            check_detail += f"LmCompatibilityLevel: {lm_compatibility_level}"

            # 정책 값에 따라 결과 설정
            if lm_compatibility_level == "5":
                check_result = "양호"
            elif lm_compatibility_level == "Not Set":
                check_result = "n/a"
            else:
                check_result = "취약"
        else:
            check_detail += f"명령 실행 오류: {policy_response.std_err.decode('utf-8')}"
            check_result = "n/a"

    except Exception as e:
        check_detail += f"\nException: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
