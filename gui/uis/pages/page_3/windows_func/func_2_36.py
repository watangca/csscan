def check_func_2_36(client):
    no = "2_36"
    check_detail = "등록된 예약 작업 목록:\n"
    tasks_list = []

    # 원격 서버에서 'schtasks' 명령 실행하여 예약된 작업 조회
    try:
        response = client.run_cmd('schtasks /query /fo LIST /v')
        tasks = response.std_out.decode()

        # 등록된 예약 작업 목록 생성
        for line in tasks.split('\n'):
            if line.startswith("TaskName:"):
                task_name = line.split(":", 1)[1].strip()
                tasks_list.append(task_name)

        # 결과 설정
        if len(tasks_list) > 0:
            check_detail += '\n'.join(tasks_list) + "\n\n각 작업의 필요 여부를 확인하고, 불필요한 작업은 제거하세요."
            check_result = "양호"
        else:
            check_detail += "등록된 예약 작업이 없습니다."
            check_result = "양호"

    except Exception as e:
        check_detail = f"schtasks 실행 오류: {e}"
        check_result = "n/a"

    return no, check_detail, check_result
