def check_func_2_24(client):
    no = "2_24"
    check_detail = "RDS 서비스 상태: "
    check_result = "n/a"

    try:
        # RDS 서비스 구동 여부 확인
        rds_service_check_cmd = "Get-Service -Name 'TermService'"
        rds_service_result = client.run_ps(rds_service_check_cmd)

        if rds_service_result.status_code == 0:
            rds_service_output = rds_service_result.std_out.decode('utf-8').strip()
            check_detail += rds_service_output

            if 'Running' in rds_service_output:
                check_result = "취약"  # RDS 서비스가 실행 중인 경우
            elif 'Stopped' in rds_service_output:
                check_result = "양호"  # RDS 서비스가 중지된 경우
            else:
                check_result = "n/a"
        else:
            check_detail += "RDS 서비스 상태 확인 실패: " + rds_service_result.std_err.decode('utf-8')

    except Exception as e:
        check_detail += "오류 발생: " + str(e)

    return no, check_detail, check_result
