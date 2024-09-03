def check_func_5_18(client):
    no = "5_18"
    check_detail = "파일 시스템 유형: "

    # 원격 시스템에서 드라이브 파일 시스템 유형 확인을 위한 PowerShell 명령어
    policy_command = """
    Get-WmiObject -Class Win32_LogicalDisk | 
    Where-Object {$_.FileSystem -ne $null} |
    Select-Object DeviceID, FileSystem |
    ForEach-Object { $_.DeviceID + ": " + $_.FileSystem }
    """

    try:
        policy_response = client.run_ps(policy_command)

        if policy_response.status_code == 0:
            filesystems = policy_response.std_out.decode('utf-8').strip()
            check_detail += filesystems

            # 파일 시스템 유형에 따라 결과 설정
            if "FAT" in filesystems:
                check_result = "취약"
            elif "NTFS" in filesystems:
                check_result = "양호"
            else:
                check_result = "n/a"
        else:
            check_detail += f"명령 실행 오류: {policy_response.std_err.decode('utf-8')}"
            check_result = "n/a"

    except Exception as e:
        check_detail += f"\nException: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
