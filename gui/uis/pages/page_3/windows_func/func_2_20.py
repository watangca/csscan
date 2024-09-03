def check_func_2_20(client):
    no = "2_20"
    # FTP 홈 디렉토리 경로 설정
    # 예시: ftp_home_directory = "C:\\inetpub\\ftproot"
    ftp_home_directory = "여기에 FTP 홈 디렉토리 경로를 입력하세요"

    # 원격 PowerShell 명령 실행
    ps_script = f"icacls {ftp_home_directory}"
    result = client.run_ps(ps_script)
    output = result.std_out.decode().strip()

    # Everyone 권한 확인
    if "Everyone" in output:
        check_detail = f"ftp 홈디렉토리 everyone 권한 설정: {output}"
        check_result = "취약"
    else:
        check_detail = "ftp 홈디렉토리에 everyone 권한 발견되지 않음"
        check_result = "양호"

    return no, check_detail, check_result
