def check_func_5_13(client):
    no = "5_13"
    registry_path = "HKLM\\System\\CurrentControlSet\\Services\\LanmanServer\\Parameters"
    check_detail = "Microsoft 네트워크 서버 정책 설정 확인: "

    # 원격 시스템에서 해당 정책 확인을 위한 PowerShell 명령어
    policy_command = f"""
    $registryPath = '{registry_path}'
    $disconnectPolicy = (Get-ItemProperty -Path Registry::$registryPath -Name 'AutoDisconnect' -ErrorAction SilentlyContinue).AutoDisconnect
    $idleTimePolicy = (Get-ItemProperty -Path Registry::$registryPath -Name 'IdleSessionTime' -ErrorAction SilentlyContinue).IdleSessionTime
    if ($null -eq $disconnectPolicy) {{ $disconnectPolicy = 'Not Set' }}
    if ($null -eq $idleTimePolicy) {{ $idleTimePolicy = 'Not Set' }}
    return "Disconnect Policy: " + $disconnectPolicy + "; Idle Time Policy: " + $idleTimePolicy
    """

    try:
        policy_response = client.run_ps(policy_command)

        if policy_response.status_code == 0:
            policies = policy_response.std_out.decode('utf-8').strip()
            check_detail += policies

            # 정책 값에 따라 결과 설정
            if "Disconnect Policy: 1" in policies and "Idle Time Policy: 900" in policies:
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
