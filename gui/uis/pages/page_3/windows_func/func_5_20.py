def check_func_5_20(client):
    no = "5_20"
    check_result = "양호"  # 무조건 양호로 출력

    # 시작 프로그램 목록 확인을 위한 PowerShell 명령어
    policy_command = """
    $paths = @('HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run', 'HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run')
    $startUpPrograms = @()
    foreach ($path in $paths) {
        try {
            $programs = Get-ItemProperty -Path Registry::$path
            $startUpPrograms += $programs.PSObject.Properties | Where-Object { $_.Name -ne 'PSPath' }
        } catch {
            continue
        }
    }
    return $startUpPrograms | ForEach-Object { $_.Name + ": " + $_.Value }
    """

    try:
        policy_response = client.run_ps(policy_command)

        if policy_response.status_code == 0:
            programs = policy_response.std_out.decode('utf-8').strip()
            # 시작 프로그램 목록 출력 및 불필요한 경우 해제 설정 필요 안내 메시지
            check_detail = f"시작프로그램 목록: {programs}\n시작프로그램 목록을 확인하고, 불필요한 경우 시작 프로그램에서 해제 설정 필요"
        else:
            check_detail = f"명령 실행 오류: {policy_response.std_err.decode('utf-8')}"
            check_result = "n/a"

    except Exception as e:
        check_detail = f"시작프로그램 목록: \nException: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
