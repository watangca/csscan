def check_func_3_27(client):
    no = "3_27"
    check_detail = ""
    check_result = "n/a"

    ftpusers_paths = ['/etc/ftpusers', '/etc/ftpd/ftpusers']

    try:
        found_files = False
        for path in ftpusers_paths:
            # ftpusers 파일의 소유자 및 권한 확인
            stdin, stdout, stderr = client.exec_command(f'ls -l {path}')
            output = stdout.read().decode('utf-8').strip()
            error = stderr.read().decode('utf-8').strip()

            if output:
                found_files = True
                parts = output.split()
                permissions, owner = parts[0], parts[2]
                check_detail += f"{path} - 소유자: {owner}, 권한: {permissions}\n"

                # 권한 문자열을 분석하여 root 소유 및 640 이하인지 확인
                owner_permissions = permissions[1:4]
                group_permissions = permissions[4:7]
                other_permissions = permissions[7:10]

                # rw- 또는 r-- 시작하고, 그룹 및 기타 사용자에게 쓰기 권한이 없는지 확인
                if owner == 'root' and owner_permissions in ['rw-', 'r--'] and 'w' not in group_permissions + other_permissions:
                    check_result = "양호"
                else:
                    check_result = "취약"
                    break  # 취약한 경우 바로 반복문 종료

            elif error:
                check_detail += f"{path} 확인 중 오류 발생: {error}\n"

        if not found_files:
            check_detail += "ftpusers 파일을 찾을 수 없습니다."

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
