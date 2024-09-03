def check_func_2_35(client):
    no = "2_35"

    cmd = "reg query 'HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\Terminal Services' /v MaxDisconnectionTime"

    # WinRM을 통해 원격 명령 실행
    result = client.run_cmd(cmd)
    output = result.std_out.decode().strip()

    # 결과 분석
    if "MaxDisconnectionTime" in output:
        # 값이 설정된 경우
        value = output.split()[-1]  # 레지스트리 값 추출
        check_detail = f"원격 데스크톱 세션 호스트 세션 시간 제한 값: {value}"
        check_result = "양호" if value != "0" else "취약"
    else:
        # 설정이 존재하지 않는 경우
        check_detail = "원격 데스크톱 세션 호스트 세션 시간 제한 값: 설정되지 않음"
        check_result = "취약"

    return no, check_detail, check_result
