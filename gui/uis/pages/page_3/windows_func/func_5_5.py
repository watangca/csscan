def check_func_5_5(client):
    no = "5_5"
    check_detail = "원격 시스템에서 강제로 시스템 종료 정책에 존재하는 계정 및 그룹: "
    check_result = "n/a"

    # 원격 시스템에서 강제로 시스템 종료 정책 확인을 위한 PowerShell 명령어
    shutdown_policy_command = """
    $secpol = secedit /export /cfg C:\\secpol.cfg
    $policyContent = Get-Content -Path C:\\secpol.cfg
    $shutdownPolicy = $policyContent | Where-Object {$_ -like "*SeShutdownPrivilege*"}
    return $shutdownPolicy
    """

    try:
        policy_response = client.run_ps(shutdown_policy_command)

        # 정책 설정 파싱
        shutdown_policy = policy_response.std_out.decode('utf-8').strip() if policy_response.std_out else ""

        check_detail += shutdown_policy

        # 정책 검사
        if "SeShutdownPrivilege" in shutdown_policy:
            if "Administrators" in shutdown_policy and "Administrators" == shutdown_policy.split("=")[1].strip():
                check_result = "양호"
            else:
                check_result = "취약"

    except Exception as e:
        check_detail += f"\nError: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
