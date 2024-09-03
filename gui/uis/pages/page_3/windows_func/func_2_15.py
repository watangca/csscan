def check_func_2_15(client):
    no = "2_15"
    check_result = "n/a"
    vulnerable_mappings = ['.htr', '.idc', '.stm', '.shtm', '.shtml', '.printer', '.htw', '.ida', '.idq']

    try:
        # 처리기 매핑 가져오기
        mapping_cmd = "Import-Module WebAdministration; Get-WebHandler | Select-Object -ExpandProperty Path"
        mapping_result = client.run_ps(mapping_cmd)
        mappings = mapping_result.std_out.decode().strip().split('\r\n')

        # 취약한 매핑 확인
        found_vulnerable_mappings = [m for m in mappings if any(vm in m for vm in vulnerable_mappings)]

        if found_vulnerable_mappings:
            check_detail = f"IIS 서버에 취약한 매핑 발견: {', '.join(found_vulnerable_mappings)}"
            check_result = "취약"
        else:
            check_detail = "IIS 서버에 취약한 매핑 발견 안됨"
            check_result = "양호"

    except Exception as e:
        check_detail = f"점검 중 오류 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result