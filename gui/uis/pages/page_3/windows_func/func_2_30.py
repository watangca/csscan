def check_func_2_30(client):
    no = "2_30"
    check_detail = "SNMP 서비스 ACL 설정: "
    check_result = "n/a"

    try:
        # SNMP 서비스 'Permitted Managers' 설정 조회
        permitted_managers_command = "Get-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\SNMP\\Parameters\\PermittedManagers'"
        permitted_managers_response = client.run_ps(permitted_managers_command)

        if permitted_managers_response.status_code == 0:
            output = permitted_managers_response.std_out.decode('utf-8').strip()

            if output:
                lines = output.split('\r\n')
                managers = {}
                for line in lines:
                    if ":" in line and not line.startswith("PS"):
                        key, value = line.split(':', 1)
                        managers[key.strip()] = value.strip()

                check_detail += str(managers)

                # 양호 및 취약 여부 판단
                if len(managers) == 0 or "1" in managers and managers["1"] in ["public", "1"]:
                    check_result = "취약"
                else:
                    check_result = "양호"
            else:
                check_detail += "설정 없음 (모든 호스트로부터 패킷 허용)"
                check_result = "취약"
        else:
            check_detail += "SNMP 서비스 설정을 확인할 수 없음"
            check_result = "n/a"

    except Exception as e:
        check_detail += str(e)
        check_result = "n/a"

    return no, check_detail, check_result
