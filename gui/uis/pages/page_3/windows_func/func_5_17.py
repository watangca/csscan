def check_func_5_17(client):
    no = "5_17"
    registry_path = "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Netlogon\\Parameters"
    check_detail = "보안 채널 데이터 정책 설정 확인: "

    # 원격 시스템에서 보안 채널 데이터 정책 설정 확인을 위한 PowerShell 명령어
    policy_command = f"""
    $registryPath = '{registry_path}'
    $requireSignOrSeal = (Get-ItemProperty -Path Registry::$registryPath -Name 'RequireSignOrSeal' -ErrorAction SilentlyContinue).RequireSignOrSeal
    $requireStrongKey = (Get-ItemProperty -Path Registry::$registryPath -Name 'RequireStrongKey' -ErrorAction SilentlyContinue).RequireStrongKey
    $sealSecureChannel = (Get-ItemProperty -Path Registry::$registryPath -Name 'SealSecureChannel' -ErrorAction SilentlyContinue).SealSecureChannel
    if ($null -eq $requireSignOrSeal) {{ $requireSignOrSeal = 'Not Set' }}
    if ($null -eq $requireStrongKey) {{ $requireStrongKey = 'Not Set' }}
    if ($null -eq $sealSecureChannel) {{ $sealSecureChannel = 'Not Set' }}
    return "RequireSignOrSeal: " + $requireSignOrSeal + "; RequireStrongKey: " + $requireStrongKey + "; SealSecureChannel: " + $sealSecureChannel
    """

    try:
        policy_response = client.run_ps(policy_command)

        if policy_response.status_code == 0:
            policies = policy_response.std_out.decode('utf-8').strip()
            check_detail += policies

            # 정책 값에 따라 결과 설정
            if all(policy.endswith("1") for policy in policies.split("; ")):
                check_result = "양호"
            elif any(policy.endswith("0") or policy.endswith("Not Set") for policy in policies.split("; ")):
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
