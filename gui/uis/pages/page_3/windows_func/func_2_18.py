def check_func_2_18(client):
    no = "2_18"
    check_detail = "NetBIOS over TCP/IP 설정: "

    # PowerShell 명령을 통해 레지스트리에서 모든 인터페이스의 NetBIOS 설정 확인
    ps_script = """
    Get-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\NetBT\\Parameters\\Interfaces\\Tcpip_*' | 
    ForEach-Object {
        $interface = $_.PSChildName
        $option = $_.NetbiosOptions
        "$interface : $option"
    }
    """
    result = client.run_ps(ps_script)
    output = result.std_out.decode()

    # 결과 분석 및 check_detail에 설정값 추가
    if output.strip():
        check_detail += output.strip()
    else:
        check_detail += "설정값 없음"

    # NetbiosOptions 값에 따른 check_result 설정
    if " : 2" in output:
        check_result = "양호"
    elif " : 0" in output or " : 1" in output:
        check_result = "취약"
    else:
        check_result = "n/a"

    return no, check_detail, check_result
