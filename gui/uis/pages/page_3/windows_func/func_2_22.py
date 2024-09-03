def check_func_2_22(client):
    no = "2_22"
    check_detail = "IIS 서버에서 FTP Authorization Rules: "
    check_result = "n/a"

    try:
        # FTP 인증 규칙 확인 명령
        auth_rules_cmd = "Get-WebConfiguration -Filter 'system.ftpServer/security/authorization' -PSPath 'IIS:\\' | Select-Object -ExpandProperty Collection"
        auth_rules_result = client.run_ps(auth_rules_cmd)

        if auth_rules_result.status_code == 0:
            auth_rules_output = auth_rules_result.std_out.decode('utf-8').strip()
            check_detail += auth_rules_output

            # 규칙 분석
            if 'roles' in auth_rules_output and 'accessType' in auth_rules_output and 'Allow' in auth_rules_output:
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail += "명령 실행 실패: " + auth_rules_result.std_err.decode('utf-8')

    except Exception as e:
        check_detail += "오류 발생: " + str(e)

    return no, check_detail, check_result


