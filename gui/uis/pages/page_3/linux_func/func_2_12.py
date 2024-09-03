def check_func_2_12(client):
    no = "2_12"
    check_detail = ""
    check_result = "n/a"

    try:
        # /dev 디렉터리 내 파일 검색
        command = "find /dev -type f -exec ls -l {} \\;"
        stdin, stdout, stderr = client.exec_command(command)

        output = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()

        if error:
            check_detail = f"오류 발생: {error}"
        else:
            if output:
                check_detail = output
                check_result = "취약"  # 존재하지 않는 device 파일이 발견된 경우
            else:
                check_detail = "존재하지 않는 device 파일이 발견되지 않음"
                check_result = "양호"  # 존재하지 않는 device 파일이 발견되지 않은 경우

    except Exception as e:
        check_detail = f"오류 발생: {str(e)}"

    return no, check_detail, check_result

