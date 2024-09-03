def check_func_2_17(client):
    no = "2_17"

    try:
        # WebDAV 설정 확인
        webdav_cmd = "Get-WebConfigurationProperty -Filter system.webServer/webdav/authoring -Name enabled -PSPath 'MACHINE/WEBROOT/APPHOST'"
        webdav_result = client.run_ps(webdav_cmd)
        webdav_config = webdav_result.std_out.decode().strip()

        # WebDAV 설정의 'Value'가 'False'인지 확인
        is_webdav_disabled = "Value                       : False" in webdav_config

        # check_detail 설정
        check_detail = f"WebDAV 설정: {webdav_config}"

        # WebDAV 비활성화 여부에 따른 결과 설정
        if is_webdav_disabled:
            check_result = "양호"
        else:
            check_result = "취약"

    except Exception as e:
        check_detail = f"점검 중 오류 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result