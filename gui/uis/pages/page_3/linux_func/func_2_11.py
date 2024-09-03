def check_func_2_11(client):
    no = "2_11"
    check_detail = ""
    check_result = "n/a"

    # 보안에 민감한 폴더 목록
    critical_dirs = ["/etc", "/bin", "/usr/bin", "/sbin", "/usr/sbin", "/var", "/home"]

    try:
        for directory in critical_dirs:
            command = f"find {directory} -type f -perm -2 -exec ls -l {{}} \\;"
            stdin, stdout, stderr = client.exec_command(command)

            output = stdout.read().decode('utf-8').strip()

            if output:
                check_detail += f"{output}\n"
                check_result = "취약"

        if check_result != "취약":
            check_detail = "시스템의 중요 폴더 내에 world writable 파일이 발견되지 않음."
            check_result = "양호"

    except Exception as e:
        check_detail = f"오류 발생: {str(e)}"

    return no, check_detail, check_result
