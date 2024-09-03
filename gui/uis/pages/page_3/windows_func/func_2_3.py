def check_func_2_3(client):
    no = "2_3"
    check_detail = "구동중인 서비스: "
    check_result = "n/a"

    # 점검할 서비스 목록
    services_to_check = [
        "Alerter", "Clipbook", "Browser", "Messenger", 
        "NetMeeting Remote Desktop Sharing", "Spooler", "RemoteRegistry"
    ]

    # 서비스 상태를 확인하는 PowerShell 명령어
    ps_command = """
    $servicesToCheck = @('Alerter', 'ClipSrv', 'Browser', 'Messenger', 'NetMeetingSvc', 'Spooler', 'RemoteRegistry')
    $runningServices = Get-Service | Where-Object {$_.Status -eq 'Running' -and $_.Name -in $servicesToCheck} | Select-Object -ExpandProperty DisplayName
    $runningServices -join ', '
    """

    # 원격 서버에서 PowerShell 명령어 실행
    response = client.run_ps(ps_command)

    if response.status_code == 0 and response.std_out:
        running_services = response.std_out.decode().strip()
        
        if running_services:
            check_detail += running_services
            check_result = "취약"
        else:
            check_detail += "없음"
            check_result = "양호"
    else:
        check_detail += " - 오류 발생: " + response.std_err.decode()
        check_result = "n/a"

    return no, check_detail, check_result