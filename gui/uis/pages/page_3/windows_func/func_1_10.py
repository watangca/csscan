def check_func_1_10(client):
    no = "1_10"
    check_detail = "최소 암호 길이: "
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

        # 파일 내용 파싱하여 최소 암호 길이 정보 추출
        secpol_content = read_result.std_out.decode().split('\n')
        min_password_length_line = next((line for line in secpol_content if "MinimumPasswordLength" in line), None)

        min_password_length = int(min_password_length_line.split('=')[1].strip()) if min_password_length_line else None

        if min_password_length is not None:
            check_detail += f"{min_password_length} 문자"
            check_result = "양호" if min_password_length >= 8 else "취약"
        else:
            check_detail += "정보를 확인할 수 없음"

    except Exception as e:
        check_detail += f"정책 확인 중 오류 발생: {str(e)}"

    return no, check_detail, check_result
