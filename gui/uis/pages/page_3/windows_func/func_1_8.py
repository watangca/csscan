def check_func_1_8(client):
    no = "1_8"
    check_detail = ""
    check_result = "n/a"

    # temp 디렉토리 생성 및 secedit 내보내기 명령어
    create_dir_command = "New-Item -Path 'C:\\temp' -ItemType Directory -Force"
    export_command = "secedit /export /cfg C:\\temp\\secpol.cfg"
    read_command = "Get-Content C:\\temp\\secpol.cfg"

    try:
        # temp 디렉토리 생성
        create_dir_result = client.run_ps(create_dir_command)
        if create_dir_result.status_code != 0:
            raise Exception("C:\\temp 디렉토리를 생성하는 데 실패했습니다.")

        # 보안 설정 내보내기 실행
        export_result = client.run_ps(export_command)
        if export_result.status_code != 0:
            raise Exception("보안 정책을 내보내는 데 실패했습니다.")

        # 내보낸 파일 읽기
        read_result = client.run_ps(read_command)
        if read_result.status_code != 0:
            raise Exception("내보낸 보안 정책 파일을 읽는 데 실패했습니다.")

        # 파일 내용 파싱하여 잠금 정책 정보 추출
        secpol_content = read_result.std_out.decode().split('\n')
        lockout_duration_line = next((line for line in secpol_content if "LockoutDuration" in line), None)
        reset_lockout_count_line = next((line for line in secpol_content if "ResetLockoutCount" in line), None)

        lockout_duration = int(lockout_duration_line.split('=')[1].strip()) if lockout_duration_line else None
        reset_lockout_count = int(reset_lockout_count_line.split('=')[1].strip()) if reset_lockout_count_line else None

        if lockout_duration and reset_lockout_count:
            check_detail += f"계정 잠금 기간: {lockout_duration}분, 잠금 기간 원래대로 설정 기간: {reset_lockout_count}분"
            lockout_duration = int(lockout_duration)
            reset_lockout_count = int(reset_lockout_count)

            # 정책 값에 따라 결과 설정
            if lockout_duration >= 60 and reset_lockout_count >= 60:
                check_result = "양호"
            else:
                check_result = "취약"

        else:
            check_detail += "계정 잠금 정책을 추출하는 데 실패했습니다."

    except Exception as e:
        check_detail += f"정책 확인 중 오류 발생: {str(e)}"

    return no, check_detail, check_result
