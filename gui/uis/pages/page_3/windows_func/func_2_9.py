def check_func_2_9(client):
    no = "2_9"

    # PowerShell 명령어를 사용하여 ApplicationPoolIdentity 설정 확인
    cmd = "Import-Module WebAdministration; Get-ItemProperty IIS:\\AppPools\\DefaultAppPool -name processModel | Select -ExpandProperty identityType"
    try:
        result = client.run_ps(cmd)
        output = result.std_out.decode().strip()

        # 결과 분석
        if "ApplicationPoolIdentity" in output:
            check_detail = f"ApplicationPoolIdentity 설정 적용: {output}"
            check_result = "양호"
        else:
            check_detail = f"ApplicationPoolIdentity 설정 미적용: {output}"
            check_result = "취약"

    except Exception as e:
        print(f"Error checking ApplicationPoolIdentity: {e}")
        check_detail = "ApplicationPoolIdentity 설정 확인 실패"
        check_result = "n/a"

    return no, check_detail, check_result

