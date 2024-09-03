def check_func_5_10(client):
    no = "5_10"
    check_detail = "폴더 데이터 보호를 위해 내용 암호화 설정 확인: "
    check_result = "n/a"

    # 폴더 목록 정의 (예: C:\, D:\)
    folders = ["C:\\", "D:\\"]

    # 원격 시스템에서 폴더의 암호화 설정 확인을 위한 PowerShell 명령어
    policy_command = """
    $result = @()
    $folders = @('C:\\', 'D:\\')
    foreach ($folder in $folders) {
        if (Test-Path $folder) {
            $attributes = (Get-Item $folder).Attributes
            $encrypted = $attributes -band [System.IO.FileAttributes]::Encrypted
            $result += "$folder : " + (($encrypted -ne 0) -as [Boolean])
        } else {
            $result += "$folder : Not Found"
        }
    }
    return $result -join '; '
    """

    try:
        policy_response = client.run_ps(policy_command)

        if policy_response.status_code == 0:
            folder_statuses = policy_response.std_out.decode('utf-8').strip().split('; ')
            check_detail += "; ".join(folder_statuses)

            # 모든 폴더가 암호화되어 있으면 '양호', 하나라도 암호화되지 않았으면 '취약'
            if all("True" in status for status in folder_statuses):
                check_result = "양호"
            elif any("False" in status for status in folder_statuses):
                check_result = "취약"
            else:
                check_result = "n/a"
        else:
            check_detail += f"명령 실행 오류: {policy_response.std_err.decode('utf-8')}"
            check_result = "n/a"

    except Exception as e:
        check_detail += f"\nException: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
