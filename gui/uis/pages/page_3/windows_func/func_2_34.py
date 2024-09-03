def check_func_2_34(client):
    no = "2_34"
    check_detail = "시스템 DSN Data Source 설정값: "
    check_result = "n/a"

    # 시스템 DSN 확인을 위한 PowerShell 명령어
    dsn_check_command = "Get-OdbcDsn -DsnType System"

    try:
        dsn_response = client.run_ps(dsn_check_command)

        # 시스템 DSN 설정 상세 내용 파싱
        dsn_config = dsn_response.std_out.decode('utf-8').strip() if dsn_response.std_out else "Not Configured"

        check_detail += f"\n{dsn_config}"

        # 시스템 DSN 설정 여부 확인
        if "Not Configured" in dsn_config:
            check_result = "취약"
        elif dsn_config:
            check_result = "양호"
        else:
            check_result = "n/a"

    except Exception as e:
        check_detail += f"\nError: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result