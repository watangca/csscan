def check_func_3_29(client):
    no = "3_29"
    check_detail = ""
    check_result = "양호"  # 기본값을 "양호"로 설정

    at_files = ['/etc/at.allow', '/etc/at.deny']

    try:
        # at 명령어 실행 권한 확인
        stdin, stdout, stderr = client.exec_command('ls -l $(which at)')
        at_permission = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()

        # at 명령어의 권한을 확인할 수 없는 경우 출력
        if error:
            check_detail += f"at 명령어 권한 확인 중 오류 발생: {error}\n"
        elif 'rwx------' not in at_permission:
            check_result = "취약"
            check_detail += "at 명령어 일반사용자 사용가능\n"
        else:
            check_detail += "at 명령어 일반사용자 사용금지\n"

        # at.allow 및 at.deny 파일 권한 확인
        for file_path in at_files:
            stdin, stdout, stderr = client.exec_command(f'ls -l {file_path}')
            file_permission = stdout.read().decode('utf-8').strip()
            error = stderr.read().decode('utf-8').strip()

            if file_permission:
                check_detail += f"{file_path} 권한: {file_permission}\n"
                permissions, _, owner, *_ = file_permission.split()
                # 파일 권한을 8진수로 변환하여 확인
                if not (owner == 'root' and permissions.startswith('-rw-------')):
                    check_result = "취약"
            elif 'No such file or directory' not in error:
                check_detail += f"{file_path} 파일 확인 중 오류 발생: {error}\n"
            else:
                check_detail += f"{file_path} 파일이 존재하지 않습니다.\n"

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
