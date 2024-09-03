def check_func_3_33(client):
    no = "3_33"
    check_detail = ""
    check_result = "n/a"

    try:
        # /etc/exports 파일의 소유자 및 권한 확인
        exports_file_path = "/etc/exports"
        stdin, stdout, stderr = client.exec_command(f'ls -l {exports_file_path}')
        exports_info = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()

        if error:
            check_detail += f"/etc/exports 파일 확인 중 오류 발생: {error}"
            check_result = "n/a"
        elif exports_info:
            permissions, _, owner, *_ = exports_info.split()
            check_detail += f"/etc/exports - 소유자: {owner}, 권한: {permissions}\n"

            # 소유자가 root이고 권한이 644 이하인지 확인
            if owner == 'root' and permissions[1:4] in ['rw-r--r--', 'r--r--r--']:
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail += "/etc/exports 파일이 존재하지 않습니다."
            check_result = "n/a"

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
