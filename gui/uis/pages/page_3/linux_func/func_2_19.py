def check_func_2_19(client):
    no = "2_19"
    check_detail = ""
    check_result = "양호"  # 기본값

    # 검사할 디렉토리 목록
    critical_dirs = ["/etc", "/var", "/bin", "/usr/bin", "/sbin", "/usr/sbin"]

    try:
        for directory in critical_dirs:
            # 숨겨진 폴더 찾기
            hidden_dirs_cmd = f"find {directory} -type d -name '.*'"
            stdin, stdout, stderr = client.exec_command(hidden_dirs_cmd)
            hidden_dirs = stdout.read().decode('utf-8').strip().split('\n')

            # 각 숨겨진 폴더 내에서 실행 가능한 파일 찾기
            for hidden_dir in hidden_dirs:
                if hidden_dir:  # 비어있는 결과는 제외
                    find_exec_cmd = f"find {hidden_dir} -type f -executable"
                    stdin, stdout, stderr = client.exec_command(find_exec_cmd)
                    exec_files = stdout.read().decode('utf-8').strip()

                    if exec_files:
                        check_detail += f"숨겨진 폴더 {hidden_dir}에서 발견된 실행 가능 파일:\n{exec_files}\n"
                        check_result = "취약"

            # 직접적으로 숨겨진 실행 가능한 파일 찾기
            hidden_exec_cmd = f"find {directory} -type f -name '.*' -executable"
            stdin, stdout, stderr = client.exec_command(hidden_exec_cmd)
            hidden_exec_files = stdout.read().decode('utf-8').strip()

            if hidden_exec_files:
                check_detail += f"경로 {directory}에서 발견된 숨겨진 실행 가능 파일:\n{hidden_exec_files}\n"
                check_result = "취약"

        if check_result == "양호":
            check_detail = "중요 디렉토리에 숨겨진 폴더 및 실행 가능 파일이 존재하지 않음."

    except Exception as e:
        check_detail = f"오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result