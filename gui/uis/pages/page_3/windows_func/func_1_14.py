def check_func_1_14(client):
    no = "1_14"
    check_detail = "로컬 로그온 허용 정책에 포함된 계정: "
    check_result = "n/a"  

    # PowerShell 스크립트를 사용하여 '로컬 로그온 허용' 정책에 포함된 계정을 SID에서 이름으로 변환하여 조회
    ps_script = """
    $policy = "SeInteractiveLogonRight"
    $userRight = secedit /export /areas USER_RIGHTS /cfg user_rights.cfg
    $content = Get-Content -Path user_rights.cfg
    $line = $content | Select-String -Pattern $policy
    Remove-Item -Path user_rights.cfg -Force
    if ($line -ne $null) {
        $sids = $line.Line.Split('=')[1].Trim().Split(',')
        $accounts = $sids | ForEach-Object {
            $sidString = $_.Trim('*')  # Remove any leading asterisks
            try {
                $sid = New-Object System.Security.Principal.SecurityIdentifier $sidString
                $account = $sid.Translate([System.Security.Principal.NTAccount])
                $account.Value
            } catch {
                $_ + " (Invalid SID)"
            }
        }
        return $accounts -join ', '
    } else {
        return "정책 없음"
    }
    """

    try:
        result = client.run_ps(ps_script)
        if result.status_code == 0:
            output = result.std_out.decode().strip()
            check_detail += output
            allowed_accounts = ['Administrators', 'IUSR'] 
            output_accounts = output.split(', ')
            if all(account in allowed_accounts for account in output_accounts) and len(output_accounts) == len(allowed_accounts):
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail += "명령어 실행 실패: " + result.std_err.decode().strip()
    except Exception as e:
        check_detail += "스크립트 실행 중 예외 발생: " + str(e)

    return no, check_detail, check_result

