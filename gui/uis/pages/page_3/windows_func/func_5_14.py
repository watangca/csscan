def check_func_5_14(client):
    no = "5_14"
    registry_path = "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System"
    check_detail = "로그인 경고 메시지 설정: "

    # 원격 시스템에서 로그인 경고 메시지 설정 확인을 위한 PowerShell 명령어
    policy_command = f"""
    $registryPath = '{registry_path}'
    $caption = (Get-ItemProperty -Path Registry::$registryPath -Name 'LegalNoticeCaption' -ErrorAction SilentlyContinue).LegalNoticeCaption
    $text = (Get-ItemProperty -Path Registry::$registryPath -Name 'LegalNoticeText' -ErrorAction SilentlyContinue).LegalNoticeText
    if ($null -eq $caption) {{ $caption = 'Not Set' }}
    if ($null -eq $text) {{ $text = 'Not Set' }}
    return "Caption: " + $caption + "; Text: " + $text
    """

    try:
        policy_response = client.run_ps(policy_command)

        if policy_response.status_code == 0:
            policies = policy_response.std_out.decode('utf-8').strip().replace('\r\n', '').replace('\0', '')
            # 엑셀에서 인식할 수 있는 형식으로 문자열 처리
            policies = policies.replace('Caption: ; Text: ', 'Caption: Not Set; Text: Not Set')
            check_detail += policies

            if "Caption: Not Set" in policies or "Text: Not Set" in policies:
                check_result = "취약"
            else:
                check_result = "양호"
        else:
            check_detail += f"명령 실행 오류: {policy_response.std_err.decode('utf-8')}"
            check_result = "취약"

    except Exception as e:
        check_detail += f"\nException: {str(e)}"
        check_result = "취약"

    return no, check_detail, check_result
