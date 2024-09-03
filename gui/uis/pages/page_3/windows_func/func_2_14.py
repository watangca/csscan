def check_func_2_14(client):
    no = "2_14"
    check_result = "n/a"

    try:
        # IIS 홈 디렉토리의 실제 경로 가져오기
        path_cmd = "Import-Module WebAdministration; (Get-Website | Select-Object -ExpandProperty physicalPath)"
        path_result = client.run_ps(path_cmd)
        iis_home_path = path_result.std_out.decode().strip()

        # Everyone 권한 확인
        acl_check_cmd = f"Get-Acl -Path '{iis_home_path}' | ForEach-Object {{ $_.Access }} | Where-Object {{ $_.IdentityReference -eq 'Everyone' }} | Format-List"
        acl_result = client.run_ps(acl_check_cmd)
        acl_info = acl_result.std_out.decode().strip()

        if acl_info:
            check_detail = f"IIS 홈디렉토리 '{iis_home_path}'의 Everyone 권한 확인하고 출력: 권한 존재 - {acl_info}"
            check_result = "취약"
        else:
            check_detail = f"IIS 홈디렉토리 '{iis_home_path}'의 Everyone 권한 확인하고 출력: Everyone 권한 없음"
            check_result = "양호"

    except Exception as e:
        check_detail = f"IIS 홈디렉토리 점검 중 오류 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result
