def check_func_2_2(client):
    no = "2_2"
    check_detail = ""
    check_result = "양호"

    # 검사할 디렉토리 목록
    directories_to_check = ["/etc", "/bin", "/sbin", "/usr/bin", "/usr/sbin", "/home", "/var", "/root"]

    try:
        orphan_files = ""

        for dir in directories_to_check:
            # 소유자가 없는 파일 및 디렉토리 찾기
            stdin, stdout, stderr = client.exec_command(f'find {dir} -nouser -print')
            no_user_files = stdout.read().decode('utf-8').strip()

            # 그룹이 없는 파일 및 디렉토리 찾기
            stdin, stdout, stderr = client.exec_command(f'find {dir} -nogroup -print')
            no_group_files = stdout.read().decode('utf-8').strip()

            orphan_files += no_user_files + "\n" + no_group_files

        if orphan_files.strip():
            check_detail = "소유자 또는 그룹이 없는 파일/디렉토리:\n" + orphan_files
            check_result = "취약"
        else:
            check_detail = "시스템 내 소유자 또는 그룹이 없는 파일 및 디렉토리가 발견되지 않음"

    except Exception as e:
        check_detail = f"오류 발생: {str(e)}"
        check_result = "N/A"

    return no, check_detail, check_result
