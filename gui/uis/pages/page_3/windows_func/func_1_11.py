def check_func_1_11(client):
    no = "1_11"
    check_detail = "최대 암호 사용 기간: "
    check_result = "n/a"

    # temp 디렉토리 생성 및 secedit 내보내기 명령어
    create_dir_command = "New-Item -Path 'C:\\temp' -ItemType Directory -Force"
    export_command = "secedit /export /cfg C:\\temp\\secpol.cfg"
    read_command = "Get-Content C:\\temp\\secpol.cfg"

    try:
        # temp 디렉토리 생성
        client.run_ps(create_dir_command)

        # 보안 설정 내보내기 실행
        client.run_ps(export_command)

        # 내보낸 파일 읽기
        result = client.run_ps(read_command)
        secpol_content = result.std_out.decode()

        # 파일 내용 파싱하여 최대 암호 사용 기간 정보 추출
        max_password_age_line = next((line for line in secpol_content.split('\n') if "MaximumPasswordAge" in line), None)

        if max_password_age_line:
            max_password_age = int(max_password_age_line.split('=')[1].strip())
            check_detail += f"{max_password_age}일"
            if max_password_age <= 90:
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_result = "n/a"
    except Exception as e:
        check_result = "오류 - 설정값을 확인할 수 없음"

    return no, check_detail, check_result

