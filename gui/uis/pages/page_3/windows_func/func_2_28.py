def check_func_2_28(client):
    no = "2_28"
    check_detail = "SNMP 서비스 구동 상태: "
    check_result = "양호"  # 기본적으로 양호로 설정 (SNMP 서비스가 없는 경우 포함)

    try:
        # SNMP 서비스 구동 여부 확인
        snmp_service_check_cmd = "Get-Service -Name 'SNMP'"
        snmp_service_result = client.run_ps(snmp_service_check_cmd)

        if snmp_service_result.status_code == 0:
            snmp_service_output = snmp_service_result.std_out.decode('utf-8').strip()
            check_detail += snmp_service_output

            if 'Running' in snmp_service_output:
                check_result = "취약"  # SNMP 서비스가 실행 중인 경우
            elif 'Stopped' in snmp_service_output:
                check_result = "양호"  # SNMP 서비스가 중지된 경우
        else:
            # SNMP 서비스가 시스템에 존재하지 않는 경우
            check_detail += "SNMP 서비스가 시스템에 존재하지 않음"
            check_result = "양호"

    except Exception as e:
        check_detail += "오류 발생: " + str(e)

    return no, check_detail, check_result
