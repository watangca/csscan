def check_func_5_19(client):
    no = "5_19"
    registry_path = "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Netlogon\\Parameters"
    check_detail = "도메인 구성원 정책 설정 확인: "

    # 원격 시스템에서 도메인 구성원 정책 설정 확인을 위한 PowerShell 명령어
    policy_command = f"""
    $registryPath = '{registry_path}'
    $disablePasswordChange = (Get-ItemProperty -Path Registry::$registryPath -Name 'DisablePasswordChange' -ErrorAction SilentlyContinue).DisablePasswordChange
    $maximumPasswordAge = (Get-ItemProperty -Path Registry::$registryPath -Name 'MaximumPasswordAge' -ErrorAction SilentlyContinue).MaximumPasswordAge
    if ($null -eq $disablePasswordChange) {{ $disablePasswordChange = 'Not Set' }}
    if ($null -eq $maximumPasswordAge) {{ $maximumPasswordAge = 'Not Set' }}
    return "DisablePasswordChange: " + $disablePasswordChange + "; MaximumPasswordAge: " + $maximumPasswordAge
    """

    try:
        policy_response = client.run_ps(policy_command)

        if policy_response.status_code == 0:
            policies = policy_response.std_out.decode('utf-8').strip()
            check_detail += policies

            # 정책 값에 따라 결과 설정
            if "DisablePasswordChange: 0" in policies and "MaximumPasswordAge: 90" in policies:
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
