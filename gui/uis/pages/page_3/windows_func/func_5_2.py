def check_func_5_2(client):
    no = "5_2"
    check_detail = "SAM 파일 접근권한: "
    check_result = "n/a"

    # SAM 파일 접근권한 확인을 위한 PowerShell 명령어 수정
    sam_acl_command = "Get-Acl -Path $env:systemroot\\system32\\config\\SAM | Select-Object -ExpandProperty Access | Format-Table IdentityReference, FileSystemRights -AutoSize"

    try:
        sam_acl_response = client.run_ps(sam_acl_command)

        # SAM 파일 접근 권한 목록 파싱
        sam_acl = sam_acl_response.std_out.decode('utf-8').strip() if sam_acl_response.std_out else "접근 권한 정보를 가져올 수 없음"

        check_detail += sam_acl

        # SAM 파일 접근권한 검사
        if "Administrator" in sam_acl and "System" in sam_acl and "Everyone" not in sam_acl and "Users" not in sam_acl:
            check_result = "양호"
        else:
            check_result = "취약"

    except Exception as e:
        check_detail = f"Error: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result