def check_func_2_23(client):
    no = "2_23"
    check_detail = "DNS 영역 전송 설정: "
    check_result = "n/a"

    try:
        # DNS 서비스 설치 여부 확인
        dns_service_check_cmd = "Get-WindowsFeature -Name DNS"
        dns_service_result = client.run_ps(dns_service_check_cmd)

        if dns_service_result.status_code == 0:
            dns_service_output = dns_service_result.std_out.decode('utf-8').strip()
            if 'Installed: False' in dns_service_output:
                check_detail += "DNS 서비스가 설치되지 않음"
                check_result = "양호"
            else:
                # 각 DNS 영역에 대한 영역 전송 설정 확인
                zones_cmd = "Get-DnsServerZone | Select-Object ZoneName, ZoneTransfer"
                zones_result = client.run_ps(zones_cmd)

                if zones_result.status_code == 0:
                    zones_output = zones_result.std_out.decode('utf-8').strip()
                    check_detail += zones_output
                    if not zones_output or 'ToAnyServer' not in zones_output:
                        check_result = "양호"
                    else:
                        check_result = "취약"
                else:
                    check_detail += "영역 전송 설정 확인 실패: " + zones_result.std_err.decode('utf-8')
        else:
            check_detail += "DNS 서비스 설치 여부 확인 실패: " + dns_service_result.std_err.decode('utf-8')

    except Exception as e:
        check_detail += "오류 발생: " + str(e)

    return no, check_detail, check_result

