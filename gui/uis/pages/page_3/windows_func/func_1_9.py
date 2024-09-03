def check_func_1_9(client):
    no = "1_9"
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

        # 파일 내용 파싱하여 암호 복잡성 정보 추출
        secpol_content = read_result.std_out.decode().split('\n')
        password_complexity_line = next((line for line in secpol_content if "PasswordComplexity" in line), None)

        password_complexity = int(password_complexity_line.split('=')[1].strip()) if password_complexity_line else None

        if password_complexity is not None:
            check_detail += f"암호 복잡성 정책 설정값: {'사용' if password_complexity == 1 else '사용 안 함'}"
            check_result = "양호" if password_complexity == 1 else "취약"
        else:
            check_detail += "암호 복잡성 정책을 추출하는 데 실패했습니다."

    except Exception as e:
        check_detail += f"정책 확인 중 오류 발생: {str(e)}"

    return no, check_detail, check_result
