def check_func_2_32(client):
    no = "2_32"
    check_detail = "http/ftp 배너 차단 설정값: "
    check_result = "n/a"

    # HTTP 서버 헤더 제거 설정 확인을 위한 PowerShell 명령어
    http_check_command = "Get-WebConfigurationProperty -pspath 'MACHINE/WEBROOT/APPHOST' -filter 'system.webServer/security/requestFiltering' -name 'removeServerHeader'"
    # FTP 기본 배너 숨김 설정 확인을 위한 PowerShell 명령어
    ftp_check_command = "Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\FtpSvc\\Parameters' -Name 'SuppressDefaultBanner'"

    try:
        http_response = client.run_ps(http_check_command)
        ftp_response = client.run_ps(ftp_check_command)

        # HTTP 및 FTP 설정 상세 내용 파싱
        http_config = http_response.std_out.decode('utf-8').strip() if http_response.std_out else "Not Configured"
        ftp_config = ftp_response.std_out.decode('utf-8').strip() if ftp_response.std_out else "Not Configured"

        check_detail += f"\nHTTP Server Header Removal: {http_config}\nFTP Default Banner Suppression: {ftp_config}"

        # 배너 설정 여부 확인
        http_vulnerable = "Value                       : False" in http_config
        ftp_vulnerable = "SuppressDefaultBanner" not in ftp_config or "SuppressDefaultBanner : 0" in ftp_config

        if http_vulnerable or ftp_vulnerable:
            check_result = "취약"
        else:
            check_result = "양호"

    except Exception as e:
        check_detail += f"\nError: {str(e)}"
        check_result = "취약"  # 오류가 발생할 경우 취약으로 간주

    return no, check_detail, check_result