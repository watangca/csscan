def check_func_2_12(client):
    no = "2_12"
    check_detail = ".asa / .asax 스크립트 매핑 및 파일 필터링 확인"
    check_result = "n/a"

    # 스크립트 매핑 확인
    script_mapping_cmd = "Import-Module WebAdministration; Get-WebHandler | Where-Object { $_.Path -like '*.asa' -or $_.Path -like '*.asax' }"
    script_mapping_result = client.run_ps(script_mapping_cmd)
    script_mappings = script_mapping_result.std_out.decode().strip()

    # 파일 필터링 확인
    file_filtering_cmd = "Get-WebConfigurationProperty -Filter 'system.webServer/security/requestFiltering/fileExtensions' -Name '*'"
    file_filtering_result = client.run_ps(file_filtering_cmd)
    file_filterings = file_filtering_result.std_out.decode().strip()

    # 결과 처리
    if "allowUnlisted" in file_filterings and "True" in file_filterings:
        check_result = "취약"
    elif script_mappings:
        check_result = "취약"
    else:
        check_result = "양호"

    check_detail += f": 매핑값 - {script_mappings}, 필터링값 - {file_filterings}"

    return no, check_detail, check_result

