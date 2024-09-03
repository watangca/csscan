def check_func_3_9(client):
    no = "3_9"
    check_result = "n/a"
    check_detail = ""

    # rpcbind 서비스의 활성화 상태 확인
    active_command = "systemctl is-active rpcbind"
    stdin, stdout, stderr = client.exec_command(active_command)
    active_output = stdout.read().decode().strip()

    # 활성화 여부에 따라 상세 정보 및 결과 설정
    check_detail = f"RPC 서비스 상태: {active_output}"

    if active_output == "inactive":
        check_result = "양호"
    elif active_output == "active":
        check_result = "취약"
    else:
        check_result = "n/a"  # 활성화 상태를 알 수 없는 경우

    return no, check_detail, check_result
