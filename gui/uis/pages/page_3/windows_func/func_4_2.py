def check_func_4_2(client):
    no = "4_2"
    check_detail = ""
    check_result = "n/a"

    try:
        # Remote Registry Service 상태 확인
        remote_registry_result = client.run_cmd('sc query RemoteRegistry')
        remote_registry_output = remote_registry_result.std_out.decode().strip()

        # 상태 분석 및 결과 설정
        if "RUNNING" in remote_registry_output:
            check_detail = "Remote Registry Service가 사용 중"
            check_result = "취약"
        elif "STOPPED" in remote_registry_output:
            check_detail = "Remote Registry Service 중지됨"
            check_result = "양호"
        else:
            check_detail = "Remote Registry Service 상태를 확인할 수 없음"
            check_result = "n/a"

    except Exception as e:
        check_detail = f"오류 발생: {e}"
        check_result = "오류"

    return no, check_detail, check_result