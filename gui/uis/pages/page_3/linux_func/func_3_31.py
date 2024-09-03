def check_func_3_31(client):
    no = "3_31"
    check_detail = ""
    check_result = "n/a"

    try:
        # SNMP Community 이름 설정 확인
        snmp_config_file = "/etc/snmp/snmpd.conf"
        stdin, stdout, stderr = client.exec_command(f'grep "com2sec" {snmp_config_file}')
        snmp_config = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()

        if error:
            check_detail += f"SNMP 설정 파일 확인 중 오류 발생: {error}"
            check_result = "n/a"
        elif snmp_config:
            check_detail += f"SNMP Community 설정: {snmp_config}\n"
            if 'public' in snmp_config or 'private' in snmp_config:
                check_result = "취약"
            else:
                check_result = "양호"
        else:
            check_detail += "SNMP Community 설정이 존재하지 않음"
            check_result = "양호"

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
