def check_func_1_5(client):
    no = "1_5"
    check_detail = ""
    check_result = "N/A"

    try:
        # 원격 서버에서 /etc/passwd 파일의 내용을 가져옴
        stdin, stdout, stderr = client.exec_command("cat /etc/passwd")
        lines = stdout.readlines()

        # UID 값이 0인 계정 찾기
        uid_zero_accounts = [line.split(":")[0] for line in lines if line.split(":")[2] == "0"]
        
        # UID 값이 0인 계정의 이름을 check_detail에 직접 출력
        check_detail = "UID 값이 0인 계정: " + ", ".join(uid_zero_accounts)
        
        if set(uid_zero_accounts) == {"root"}:
            check_result = "양호"
        else:
            check_result = "취약"
    except Exception as e:
        check_detail = "Error occurred while checking: " + str(e)
        check_result = "n/a"
    
    return no, check_detail, check_result
