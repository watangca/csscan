def check_func_6_1(client):
    no = "6_1"
    check_detail = "DB 로그인 시 Windows 인증 모드 적절성 점검 결과:\n"

    # PowerShell 스크립트: SQL Server 인증 모드 및 SA 계정 상태 확인, UTF-8 인코딩 명시
    policy_command = """
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $instances = Get-WmiObject -Namespace "root\\CIMV2" -Class "Win32_Service" | Where-Object { $_.Name -like "MSSQL*" -and $_.State -eq "Running" }
    $details = @()
    foreach ($instance in $instances) {
        $sqlInstance = if ($instance.Name -eq "MSSQLSERVER") { "." } else { $instance.Name -replace "MSSQL$", "" }
        $authModeQuery = "SELECT SERVERPROPERTY('IsIntegratedSecurityOnly')"
        $saStatusQuery = "SELECT is_disabled FROM sys.sql_logins WHERE name = 'sa'"
        $authMode = Invoke-Sqlcmd -Query $authModeQuery -ServerInstance $sqlInstance -ErrorAction SilentlyContinue
        $saStatus = Invoke-Sqlcmd -Query $saStatusQuery -ServerInstance $sqlInstance -ErrorAction SilentlyContinue
        $modeText = if ($authMode -and $authMode[0] -eq 1) { "Windows 인증 모드" } else { "혼합 인증 모드" }
        $saStatusText = if ($saStatus -and $saStatus.is_disabled -eq 1) { "SA 계정 비활성화" } else { "SA 계정 활성화" }
        $details += "$($instance.DisplayName): $modeText, $saStatusText"
    }
    if ($details.Count -eq 0) {
        "SQL Server 인스턴스가 실행 중이 아니거나 없습니다."
    } else {
        $details -join "`n"
    }
    """

    try:
        response = client.run_ps(policy_command)
        # PowerShell의 UTF-8 출력을 올바르게 디코딩
        check_detail += response.std_out.decode('utf-8').strip()

        if "인스턴스가 실행 중이 아니거나 없습니다" in check_detail:
            check_result = "n/a"
        elif "혼합 인증 모드" in check_detail or "SA 계정 활성화" in check_detail:
            check_result = "취약"
        else:
            check_result = "양호"
    except Exception as e:
        check_detail += f"\n스크립트 실행 중 예외 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result
