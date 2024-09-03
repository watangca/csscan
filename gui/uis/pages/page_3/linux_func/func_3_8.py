def check_func_3_8(client):
    no = "3_8"
    check_result = "n/a"
    check_detail = ""

    # autofs 서비스의 활성화 상태 확인
    check_command = "systemctl is-active autofs"
    stdin, stdout, stderr = client.exec_command(check_command)
    service_status = stdout.read().decode().strip()
    error_message = stderr.read().decode().strip()

    # 명령어 실행 오류 확인
    if error_message:
        check_detail = f"autofs 서비스 상태 확인 중 오류 발생: {error_message}"
        check_result = "n/a"
    elif service_status == "active":
        check_detail = "autofs 서비스 상태: active"
        check_result = "취약"
    elif service_status == "inactive" or service_status == "failed":
        check_detail = "autofs 서비스 상태: inactive"
        check_result = "양호"
    else:
        check_detail = f"autofs 서비스 상태를 확인할 수 없음: {service_status}"
        check_result = "n/a"

    return no, check_detail, check_result
