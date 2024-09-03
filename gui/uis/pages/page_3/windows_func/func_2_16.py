def check_func_2_16(client):
    no = "2_16"

    try:
        # IIS 버전 확인
        iis_version_cmd = "(Get-ItemProperty 'HKLM:\\SOFTWARE\\Microsoft\\InetStp').VersionString"
        version_result = client.run_ps(iis_version_cmd)
        iis_version = version_result.std_out.decode().strip()
        check_detail = f"IIS 버전: {iis_version}"

        # IIS 버전이 5.0인 경우 레지스트리 확인
        if "5.0" in iis_version:
            reg_cmd = "Get-ItemProperty 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\W3SVC\\Parameters' -Name 'DisableSocketPooling'"
            reg_result = client.run_ps(reg_cmd)
            reg_value = reg_result.std_out.decode().strip()

            check_detail += f", 레지스트리 값: {reg_value}"

            # 레지스트리 값에 따른 결과 설정
            if "DisableSocketPooling : 1" in reg_value:
                check_result = "취약"
            else:
                check_result = "양호"
        else:
            check_result = "양호"

    except Exception as e:
        check_detail = f"점검 중 오류 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result