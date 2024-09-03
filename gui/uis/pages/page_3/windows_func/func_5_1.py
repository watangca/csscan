def check_func_5_1(client):
    no = "5_1"
    check_detail = "설치된 백신 프로그램: "
    check_result = "취약"  # 기본적으로 취약으로 설정

    # Windows Defender 상태 확인을 위한 PowerShell 명령어
    defender_check_command = "Get-MpComputerStatus | Select-Object -Property AMRunningMode"
    # 기타 설치된 바이러스 백신 확인을 위한 WMI 쿼리
    antivirus_check_command = "Get-WmiObject -Namespace 'root\\SecurityCenter2' -Class AntiVirusProduct | Select-Object -Property displayName"

    try:
        # Windows Defender 상태 확인
        defender_response = client.run_ps(defender_check_command)
        defender_status = defender_response.std_out.decode('utf-8').strip() if defender_response.std_out else ""
        
        # 기타 안티바이러스 소프트웨어 상태 확인
        antivirus_response = client.run_ps(antivirus_check_command)
        antivirus_list = antivirus_response.std_out.decode('utf-8').strip() if antivirus_response.std_out else ""

        # 결과 파싱 및 설정
        if "AMRunningMode" in defender_status:
            check_detail += "\nWindows Defender 설치됨."
            check_result = "양호"
        if antivirus_list:
            antivirus_names = "; ".join([line.split(":")[-1].strip() for line in antivirus_list.split("\n")])
            check_detail += f"\n기타 안티바이러스: {antivirus_names}"
            check_result = "양호"
        
        if not defender_status and not antivirus_list:
            check_detail += "\n설치된 백신 프로그램이 없음."

    except Exception as e:
        check_detail += f"\nException: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
