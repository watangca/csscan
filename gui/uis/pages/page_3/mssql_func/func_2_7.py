def check_func_2_7(win_conn):
    no = "2_7"
    check_detail = "파일 접근 권한 점검 결과: "

    # PowerShell 스크립트: SQL Server 구성 파일의 접근 권한을 체크
    ps_script = """
    $sqlServerConfigFiles = @(
        [System.IO.Path]::Combine($env:ProgramFiles, 'Microsoft SQL Server', '*', 'MSSQL', 'Binn', 'sqlservr.exe.config'),
        [System.IO.Path]::Combine($env:ProgramFiles, 'Microsoft SQL Server', '*', 'Reporting Services', 'ReportServer', 'rsreportserver.config'),
        [System.IO.Path]::Combine($env:ProgramFiles, 'Microsoft SQL Server', '*', 'Reporting Services', 'ReportServer', 'reportingservices.config'),
        "$env:SystemRoot\\Microsoft.NET\\Framework64\\v*\\CONFIG\\machine.config",
        "$env:SystemRoot\\Microsoft.NET\\Framework64\\v*\\CONFIG\\web.config"
    )

    foreach ($filePattern in $sqlServerConfigFiles) {
        $files = Get-ChildItem $filePattern -ErrorAction SilentlyContinue
        foreach ($file in $files) {
            $acl = Get-Acl $file.FullName
            $acl.Access | Where-Object {
                $_.FileSystemRights -match 'Write' -and 
                $_.IdentityReference -notmatch '^(BUILTIN\\Administrators|NT AUTHORITY\\SYSTEM|.*Owner)$'
            } | ForEach-Object {
                "$($file.FullName) - $($_.IdentityReference) has write permission"
            }
        }
    }
    """

    try:
        # WinRM을 사용하여 원격 서버에서 PowerShell 스크립트 실행
        result = win_conn.run_ps(ps_script)
        if result.status_code == 0 and result.std_out.strip():
            # PowerShell 명령의 성공적인 출력 결과를 check_detail에 추가
            check_detail += result.std_out.strip()
        else:
            # 파일이 없거나 접근 권한이 적절히 설정된 경우
            check_detail += "모든 지정된 파일들이 적절한 접근 권한 설정을 가지고 있습니다."
    except Exception as e:
        # 예외 발생 시 처리
        check_detail += f"점검 중 오류 발생: {str(e)}"
        check_result = "n/a"
        return no, check_detail, check_result

    # 점검 결과 설정
    check_result = "양호" if "has write permission" not in check_detail else "취약"

    return no, check_detail, check_result
