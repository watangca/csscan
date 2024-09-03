def check_func_3_28(client):
    no = "3_28"
    check_detail = ""
    check_result = "n/a"

    ftpusers_files = ['/etc/ftpusers', '/etc/ftpd/ftpusers']

    try:
        for file_path in ftpusers_files:
            # ftpusers 파일에서 root 계정 확인
            stdin, stdout, stderr = client.exec_command(f'cat {file_path} | grep -w root')
            root_entry = stdout.read().decode('utf-8').strip()
            error = stderr.read().decode('utf-8').strip()

            if root_entry:
                check_result = "취약"
                check_detail += f"{file_path} 파일에서 root 계정 접속 허용 설정: {root_entry}\n"
                break
            elif error:
                check_detail += f"{file_path} 파일 확인 중 오류 발생: {error}\n"
            else:
                check_result = "양호"
                check_detail += f"{file_path} 파일에서 root 계정 접속이 차단 설정\n"

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
