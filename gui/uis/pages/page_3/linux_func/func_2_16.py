def check_func_2_16(client):
    no = "2_16"
    check_detail = ""
    check_result = "n/a"

    try:
        stdin, stdout, stderr = client.exec_command("umask")
        umask_value = stdout.read().decode().strip()

        if umask_value:
            check_detail = f"umask 값: {umask_value}"
            # umask 값이 022 이상이면 양호로 판단
            if int(umask_value, 8) >= 0o22:
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail = "umask 설정되지 않음"

    except Exception as e:
        check_detail = str(e)
        check_result = "오류"

    return no, check_detail, check_result
