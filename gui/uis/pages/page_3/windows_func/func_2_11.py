def check_func_2_11(client):
    no = "2_11"
    check_detail = "IIS 파일 업로드 및 다운로드 제한 설정 확인"
    check_result = "n/a"

    # IIS 파일 업로드 및 다운로드 제한 설정 확인
    upload_limit_cmd = "Import-Module WebAdministration; Get-WebConfigurationProperty -pspath 'MACHINE/WEBROOT/APPHOST' -filter 'system.webServer/security/requestFiltering/requestLimits' -name '*'"

    try:
        # 설정값 가져오기
        upload_limit_result = client.run_ps(upload_limit_cmd)
        upload_limit = upload_limit_result.std_out.decode().strip()

        if upload_limit:
            check_detail += f": 설정값 - {upload_limit}"
            # 설정값을 바탕으로 양호 또는 취약 판단
            if 'maxAllowedContentLength' in upload_limit or 'maxUrl' in upload_limit or 'maxQueryString' in upload_limit:
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail += ": 제한 설정 없음"

    except Exception as e:
        print(f"Error: {e}")
        check_detail = "점검 중 오류 발생"

    return no, check_detail, check_result
