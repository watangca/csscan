def check_func_5_3(client):
    no = "5_3"
    check_detail = ""
    check_result = "n/a"

    # 화면보호기 설정 확인을 위한 PowerShell 명령어
    screensaver_check_command = """
    $screensaverStatus = (Get-ItemProperty 'HKCU:\\Control Panel\\Desktop').ScreenSaveActive
    $screensaverTime = (Get-ItemProperty 'HKCU:\\Control Panel\\Desktop').ScreenSaveTimeOut
    $screensaverPassword = (Get-ItemProperty 'HKCU:\\Control Panel\\Desktop').ScreenSaverIsSecure
    return $screensaverStatus, $screensaverTime, $screensaverPassword
    """

    try:
        screensaver_response = client.run_ps(screensaver_check_command)

        # 화면보호기 설정 파싱
        screensaver_info = screensaver_response.std_out.decode('utf-8').strip() if screensaver_response.std_out else ""

        if "ScreenSaveActive : 1" in screensaver_info:
            timeout = int(screensaver_info.split("ScreenSaveTimeOut : ")[1].split("\n")[0].strip())
            password_protected = "ScreenSaverIsSecure : 1" in screensaver_info
            check_detail = f"화면 보호기 활성화됨, 대기시간: {timeout}초, 비밀번호 보호: {password_protected}"

            if timeout <= 600 and password_protected:
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail = "화면 보호기 비활성화됨"
            check_result = "취약"

    except Exception as e:
        check_detail = f"Error: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result