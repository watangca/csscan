def check_func_2_1(client):
    no = "2_1"
    check_detail = ""
    check_result = "n/a"

    ps_script = """
    $defaultShares = @('ADMIN$', 'C$', 'IPC$')
    $shares = Get-SmbShare -Special $false | Where-Object { $defaultShares -notcontains $_.Name }
    $result = @()

    foreach ($share in $shares) {
        $permissions = Get-SmbShareAccess -Name $share.Name
        foreach ($permission in $permissions) {
            if ($permission.AccountName -eq "Everyone") {
                $result += "$($share.Name) - Everyone"
            }
        }
    }

    if ($result.Count -eq 0) {
        Write-Output "No additional shares with Everyone permission"
    } else {
        Write-Output $result
    }
    """

    try:
        response = client.run_ps(ps_script)
        if response.status_code == 0:
            output = response.std_out.decode('utf-8').strip()
            if "No additional shares with Everyone permission" in output:
                check_detail = "기본공유 폴더외 공유폴더 존재하지 않음"
                check_result = "양호"
            else:
                check_detail = output
                check_result = "취약"
        else:
            error_output = response.std_err.decode('utf-8').strip()
            check_detail = f"Error: {error_output}"
            check_result = "n/a"
    except Exception as e:
        check_detail = f"Exception: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result




