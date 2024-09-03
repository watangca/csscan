def check_func_2_21(client):
    no = "2_21"
    check_detail = "IIS FTP Anonymous FTP Authentication "
    check_result = "n/a"

    try:
        # 익명 FTP 인증 상태 확인 명령
        auth_status_cmd = "Get-WebConfiguration -Filter '/system.applicationHost/sites/siteDefaults/ftpServer/security/authentication/anonymousAuthentication' -PSPath 'IIS:\\' | Select-Object -ExpandProperty Enabled"
        auth_status_result = client.run_ps(auth_status_cmd)

        if auth_status_result.status_code == 0:
            auth_status_output = auth_status_result.std_out.decode('utf-8').strip()
            check_detail += f"Enabled: {auth_status_output}"

            if auth_status_output == "False":
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail += "명령 실행 실패: " + auth_status_result.std_err.decode('utf-8')

    except Exception as e:
        check_detail += "오류 발생: " + str(e)

    return no, check_detail, check_result
