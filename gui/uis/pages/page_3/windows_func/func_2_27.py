def check_func_2_27(client):
    no = "2_27"
    check_detail = "IIS 사용자 지정 오류 페이지 설정: "
    check_result = "양호"  # 기본적으로 양호로 설정

    try:
        # 사용자 지정 오류 페이지의 전체 경로 확인
        error_page_cmd = "Get-WebConfiguration -Filter 'system.webServer/httpErrors/error' -PSPath 'MACHINE/WEBROOT/APPHOST' | Select-Object statusCode, prefixLanguageFilePath, path"
        error_page_result = client.run_ps(error_page_cmd)

        if error_page_result.status_code == 0:
            error_pages = error_page_result.std_out.decode('utf-8').strip().splitlines()
            # 기본 오류 페이지 사용 여부 확인
            for line in error_pages:
                if '%SystemDrive%\\inetpub\\custerr' in line:
                    check_result = "취약"  # 기본 오류 페이지가 설정된 경우
                    break
            check_detail += "\n".join(error_pages)
        else:
            check_detail += "오류 페이지 설정 확인 실패: " + error_page_result.std_err.decode('utf-8')

    except Exception as e:
        check_detail += "오류 발생: " + str(e)

    return no, check_detail, check_result
