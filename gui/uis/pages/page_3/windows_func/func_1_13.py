def check_func_1_13(client):
    no = "1_13"
    # 초기화
    check_detail = "대화형 로그온: 마지막 사용자 이름 표시 안 함"
    check_result = "n/a"

    ps_script = """
    $key = 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System'
    $name = 'DontDisplayLastUserName'
    $value = (Get-ItemProperty -Path $key -Name $name).$name
    if ($null -ne $value) {
        if ($value -eq 0) {
            "Disabled"
        } elseif ($value -eq 1) {
            "Enabled"
        } else {
            "n/a"
        }
    } else {
        "설정값 없음"
    }
    """

    try:
        result = client.run_ps(ps_script)
        if result.status_code == 0:
            output = result.std_out.decode().strip()
            if output == "Disabled":
                check_result = "취약"
                check_detail += ": 사용 안 함"
            elif output == "Enabled":
                check_result = "양호"
                check_detail += ": 사용"
            else:
                check_detail += ": 설정값 없음"
        else:
            # 에러 발생 시
            check_detail += ": 명령어 실행 실패"
    except Exception as e:
        check_detail += ": 스크립트 실행 중 예외 발생"

    return no, check_detail, check_result

