def check_func_2_19(client):
    no = "2_19"
    
    # FTP 서비스 상태 확인
    check_ftp_service_cmd = "Get-Service -Name 'ftpsvc' | Select-Object Status"
    ftp_service_status = client.run_ps(check_ftp_service_cmd).std_out.decode().strip()

    # OpenSSH 서비스 (SFTP) 상태 확인
    check_ssh_service_cmd = "Get-Service -Name 'sshd' | Select-Object Status"
    ssh_service_status = client.run_ps(check_ssh_service_cmd).std_out.decode().strip()

    # FTP 서비스와 SFTP 서비스 상태에 따라 결과 결정
    if 'Running' not in ftp_service_status and 'Running' in ssh_service_status:
        check_detail = "Secure FTP 서비스가 실행 중입니다."
        check_result = "양호"
    elif 'Running' in ftp_service_status:
        check_detail = "일반 FTP 서비스가 실행 중입니다."
        check_result = "취약"
    else:
        check_detail = "FTP 또는 SFTP 서비스가 실행 중이지 않습니다."
        check_result = "n/a"
    
    return no, check_detail, check_result
