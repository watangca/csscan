def check_func_1_15(client):
    no = "1_15"
    check_detail = ""
    check_result = "취약"  # 'TMOUT' 설정이 없거나 600초 이상일 경우 취약으로 기본 설정

    # 설정 파일 목록
    config_files = ["/etc/profile", "/etc/bash.bashrc", "/etc/zsh/zshrc", "/etc/csh.cshrc", "/etc/csh.login"]

    # 'TMOUT' 설정을 찾기 위한 명령어
    check_command = "grep '^TMOUT=' {}"

    # 설정 파일들을 확인
    for file in config_files:
        stdin, stdout, stderr = client.exec_command(check_command.format(file))
        output = stdout.read().decode('utf-8').strip()
        
        # 에러가 있는 경우, 다음 파일 확인
        if stderr.read().decode('utf-8').strip():
            continue

        # 'TMOUT' 설정이 있는 경우
        if output:
            # 설정값 추출
            timeout_value = int(output.split('=')[1])
            check_detail = f"Session Timeout 설정값: {timeout_value}초"
            
            # 설정값이 600초 이하인 경우
            if timeout_value <= 600:
                check_result = "양호"
            else:
                check_result = "취약"
            
            break  # 설정값을 찾았으니 루프 탈출

    # 'check_detail'이 비어있다면 'TMOUT' 설정이 없는 것으로 간주
    if not check_detail:
        check_detail = "Session Timeout 설정값이 없음"

    return no, check_detail, check_result
