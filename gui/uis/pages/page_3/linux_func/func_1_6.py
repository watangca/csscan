def check_func_1_6(client):
    no = "1_6"
    check_detail = "su 명령어 제한 설정: "
    check_result = "N/A"
    
    # 파일 경로 설정
    file_path = "/etc/pam.d/su"
    
    try:
        # 실제 설정 라인을 찾기 위한 grep 명령어 수정
        command = f"grep -E '^auth[[:space:]]+required[[:space:]]+pam_wheel.so[[:space:]]+use_uid' {file_path}"
        stdin, stdout, stderr = client.exec_command(command)
        content = stdout.read().decode().strip()
        
        # su 명령어 제한 설정 확인
        if content:  # content가 비어 있지 않으면 설정이 발견된 것임
            check_detail += content
            check_result = "양호"
        else:
            check_detail = "su 명령어 제한 설정이 발견되지 않음"
            check_result = "취약"
    except Exception as e:
        check_result = "N/A"
        check_detail = f"{file_path} 파일을 읽는 중 오류 발생: {str(e)}"
    
    return no, check_detail, check_result
