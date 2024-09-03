def check_func_2_10(client):
    no = "2_10"
    check_detail = "심볼링 링크, aliases, 바로가기 파일 확인"
    check_result = "n/a"

    # IIS 웹사이트의 실제 경로 가져오기
    path_cmd = "Import-Module WebAdministration; (Get-Website | Select-Object -ExpandProperty physicalPath)"

    try:
        # 실제 경로 가져오기
        path_result = client.run_ps(path_cmd)
        home_directory = path_result.std_out.decode().strip()

        # 심볼릭 링크 등 확인
        link_cmd = f"Get-ChildItem -Path '{home_directory}' -Recurse -Force | Where-Object {{ $_.Attributes -like '*ReparsePoint*' }} | Select-Object -ExpandProperty FullName"
        link_result = client.run_ps(link_cmd)
        links = link_result.std_out.decode().strip()

        if links:
            check_detail += f": 발견된 링크 - {links}"
            check_result = "취약"
        else:
            check_detail += ": 링크 없음"
            check_result = "양호"

    except Exception as e:
        check_detail = f"점검 중 오류 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result

