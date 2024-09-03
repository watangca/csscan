def check_func_2_13(client):
    no = "2_13"
    check_detail = "IIS Admin, IIS Adminpwd 가상 디렉토리 확인"
    check_result = "n/a"

    # IIS 가상 디렉토리 확인
    virtual_dir_cmd = "Import-Module WebAdministration; Get-WebVirtualDirectory"

    try:
        # 가상 디렉토리 결과 가져오기
        virtual_dir_result = client.run_ps(virtual_dir_cmd)
        virtual_dirs = virtual_dir_result.std_out.decode().strip()

        # IIS Admin, IIS Adminpwd 확인
        if 'IIS Admin' in virtual_dirs or 'IIS Adminpwd' in virtual_dirs:
            check_result = "취약"
            check_detail += ": 존재함"
        else:
            check_result = "양호"
            check_detail += ": 존재하지 않음"

    except Exception as e:
        print(f"Error: {e}")
        check_detail = "점검 중 오류 발생"

    return no, check_detail, check_result
