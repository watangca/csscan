def check_func_2_31(client):
    no = "2_31"
    check_detail = "DNS 서비스 동적 업데이트 설정: "
    check_result = "n/a"

    try:
        # DNS 존의 동적 업데이트 설정 조회
        dns_zone_update_command = """
        Get-DnsServerZone | ForEach-Object { $_ | Select-Object -Property ZoneName, DynamicUpdate }
        """
        dns_zone_update_response = client.run_ps(dns_zone_update_command)

        if dns_zone_update_response.status_code == 0 and dns_zone_update_response.std_out:
            output = dns_zone_update_response.std_out.decode('utf-8').strip()
            check_detail += output

            # 결과 분석 및 평가
            dynamic_updates = []
            for line in output.split('\n'):
                if "DynamicUpdate" in line:
                    parts = line.split()
                    if len(parts) > 1:
                        dynamic_updates.append(parts[-1])

            if all(update == "None" for update in dynamic_updates):
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail += "DNS 서비스 설정을 확인할 수 없음: " + dns_zone_update_response.std_err.decode('utf-8').strip()

    except Exception as e:
        check_detail += str(e)
        check_result = "n/a"

    return no, check_detail, check_result
