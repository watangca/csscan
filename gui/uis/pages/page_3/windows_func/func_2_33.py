def check_func_2_33(client):
    no = "2_33"
    check_detail = ""
    check_result = "n/a"

    try:
        # Check Telnet service status
        telnet_result = client.run_cmd('sc query tlntsvr')
        telnet_output = telnet_result.std_out.decode().strip()

        # Check SSH service status
        ssh_result = client.run_cmd('sc query sshd')
        ssh_output = ssh_result.std_out.decode().strip()

        # Initialize result as n/a
        check_result = "n/a"

        # Check if Telnet is running and determine authentication method
        if "RUNNING" in telnet_output:
            tlntadmn_result = client.run_cmd('tlntadmn config')
            tlntadmn_output = tlntadmn_result.std_out.decode().strip()
            check_detail += "Telnet service is running.\n"
            
            if "NTLM" in tlntadmn_output:
                check_detail += "Authentication method: NTLM\n"
                check_result = "양호"
            else:
                check_detail += "Authentication method: Not NTLM\n"
                check_result = "취약"
        else:
            check_detail += "Telnet service is not running.\n"

        # Check if SSH is running
        if "RUNNING" in ssh_output:
            check_detail += "SSH service is running.\n"
            check_result = "양호" if check_result != "취약" else check_result
        else:
            check_detail += "SSH service is not running.\n"

        # If both services are not running, set to n/a
        if "RUNNING" not in telnet_output and "RUNNING" not in ssh_output:
            check_result = "n/a"

    except Exception as e:
        check_detail += f"Error occurred: {e}"
        check_result = "오류"

    return no, check_detail, check_result
