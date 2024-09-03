def check_func_3_30(client):
    no = "3_30"
    check_detail = ""
    check_result = "n/a"

    try:
        # SNMP 서비스 실행 여부 확인
        stdin, stdout, stderr = client.exec_command('ps -ef | grep snmp | grep -v grep')
        snmp_output = stdout.read().decode('utf-8').strip()

        if snmp_output:
            check_result = "취약"
            check_detail += "SNMP 서비스 실행증"
        else:
            check_result = "양호"
            check_detail += "SNMP 서비스 비활성화"

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
