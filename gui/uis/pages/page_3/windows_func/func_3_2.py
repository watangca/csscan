def check_func_3_2(client):
    no = "3_2"
    
    # PowerShell 명령 실행
    ps_script = "Get-MpComputerStatus"
    result = client.run_ps(ps_script)

    # 결과 디코딩
    std_out = result.std_out.decode('utf-8') if result.std_out else ""

    # 결과 파싱
    if "AntivirusEnabled" in std_out:
        antivirus_enabled = "AntivirusEnabled" in std_out
        auto_update_enabled = "AntispywareSignatureAutoUpdate" in std_out

        check_detail = f"백신 설치 여부: {'설치됨' if antivirus_enabled else '설치되지 않음'}, 자동 업데이트 설정: {'설정됨' if auto_update_enabled else '설정되지 않음'}"
        
        if antivirus_enabled and auto_update_enabled:
            check_result = "양호"
        elif not antivirus_enabled or not auto_update_enabled:
            check_result = "취약"
    else:
        check_detail = "백신 정보를 확인할 수 없습니다."
        check_result = "n/a"

    return no, check_detail, check_result