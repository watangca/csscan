def check_func_3_18(client):
    no = "3_18"
    check_detail = ""
    check_result = "n/a"

    # Apache 서비스 실행 여부 확인
    cmd = "ps -ef | grep apache2 | grep -v grep"
    stdin, stdout, stderr = client.exec_command(cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()

    if error:
        check_detail += f"Apache 서비스 확인 중 오류 발생: {error}\n"
    elif output:
        check_detail += "Apache 웹 서비스 실행 중\n"
        webserver_running = "apache"
    else:
        check_detail += "실행 중인 Apache 웹 서버가 발견되지 않음\n"
        return no, check_detail, check_result

    # Apache 데몬 권한 확인
    if webserver_running == "apache":
        stdin, stdout, stderr = client.exec_command("ps -e -o pid,user,cmd | grep apache2 | grep -v grep")
        processes = stdout.read().decode().strip().split('\n')
        root_processes = [process for process in processes if ' root ' in process]

        if root_processes:
            check_result = "취약"
            check_detail += f"Apache 데몬이 root 권한으로 실행 중: {', '.join(root_processes)}\n"
        else:
            check_result = "양호"
            check_detail += "Apache 데몬이 root 권한으로 실행되지 않음\n"

    return no, check_detail, check_result
