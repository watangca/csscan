def check_func_3_24(client):
    no = "3_24"
    check_detail = ""
    ssh_running = False
    telnet_running = False

    try:
        # Check if SSH service is running
        stdin, stdout, stderr = client.exec_command('ps -ef | grep sshd | grep -v grep')
        ssh_output = stdout.read().decode('utf-8').strip()
        if ssh_output:
            ssh_running = True
            check_detail += f"SSH 서비스 실행 중: {ssh_output}\n"

        # Check if Telnet service is running
        stdin, stdout, stderr = client.exec_command('ps -ef | grep telnetd | grep -v grep')
        telnet_output = stdout.read().decode('utf-8').strip()
        if telnet_output:
            telnet_running = True
            check_detail += f"Telnet 서비스 실행 중: {telnet_output}\n"

        # Determine the result based on service status
        if ssh_running or telnet_running:
            if telnet_running:
                check_result = "취약"
            else:
                check_result = "양호"
        else:
            check_detail += "SSH,Telnet 서비스가 실행 중이지 않음"
            check_result = "n/a"

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
