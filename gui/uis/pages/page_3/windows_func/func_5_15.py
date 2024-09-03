def check_func_5_15(client):
    no = "5_15"
    user_folders_path = "C:\\Users\\"
    check_detail = "Everyone 권한이 발견된 계정:\n"
    found_everyone_permission = False

    # 원격 시스템에서 사용자 홈 디렉토리 권한 적절성 점검을 위한 PowerShell 명령어
    policy_command = f"""
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $userFolders = Get-ChildItem -Path '{user_folders_path}' -Directory -Force | 
                   Where-Object {{ $_.Name -notmatch '^(Public|Default|All Users)$' }} | 
                   Where-Object {{ $_.Name -ne 'Default User' }}
    foreach ($folder in $userFolders) {{
        $acl = Get-Acl -Path $folder.FullName
        $everyoneAccess = $acl.Access | Where-Object {{ $_.IdentityReference -eq 'Everyone' -and $_.AccessControlType -eq 'Allow' }}
        if ($everyoneAccess) {{
            $found_everyone_permission = $true
            $results = "$($folder.Name): 계정: Everyone, 권한: $($everyoneAccess.FileSystemRights), 접근 타입: $($everyoneAccess.AccessControlType)"
            Write-Output $results
        }}
    }}
    if (-not $found_everyone_permission) {{
        Write-Output "홈 디렉토리에 Everyone 권한이 발견되지 않음"
    }}
    """

    try:
        policy_response = client.run_ps(policy_command)
        
        if policy_response.status_code == 0:
            permissions = policy_response.std_out.decode('utf-8').strip()
            if "홈 디렉토리에 Everyone 권한이 없습니다." in permissions:
                check_detail += "홈 디렉토리에 Everyone 권한이 발견되지 않음"
                check_result = "양호"
            else:
                check_detail += permissions
                check_result = "취약" if permissions else "양호"
        else:
            error_output = policy_response.std_err.decode('utf-8').strip()
            check_detail += f"명령 실행 오류: {error_output}"
            check_result = "n/a"

    except Exception as e:
        check_detail += f"예외 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result
