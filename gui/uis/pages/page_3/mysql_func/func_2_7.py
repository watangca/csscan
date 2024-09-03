def check_func_2_7(client):
    no = "2_7"
    check_detail = []
    check_result = "n/a"  # 기본값 설정

    # my.cnf 파일의 위치 목록
    config_files = [
        "/etc/my.cnf",
        "/etc/mysql/my.cnf",
        "~/.my.cnf"
    ]

    # 파일 권한을 체크하는 부분
    for file_path in config_files:
        # 파일 존재 여부 및 권한을 확인하는 커맨드
        command = f"if [ -f {file_path} ]; then ls -l {file_path}; else echo ''; fi"
        stdin, stdout, stderr = client.exec_command(command)
        result = stdout.read().decode('utf-8').strip()

        # 결과가 비어있지 않은 경우만 처리
        if result:
            # 권한 부분만 추출하여 취약 여부 확인
            parts = result.split()
            permissions = parts[0]
            name = parts[-1]
            if permissions in ['-rw-------', '-rw-r-----']:  # 파일 권한이 600 또는 640인지 확인
                check_detail.append(f"{name} 권한이 안전함: {permissions}")
            else:
                check_detail.append(f"{name} 권한이 안전하지 않음: {permissions}")

    # 결과 세팅
    if any('안전하지 않음' in detail for detail in check_detail):
        check_result = "취약"
    elif check_detail:  # check_detail이 비어있지 않고 모든 파일 권한이 안전한 경우
        check_result = "양호"
    else:
        check_result = "파일을 찾을 수 없음"  # 모든 파일이 존재하지 않는 경우

    return no, "\n".join(check_detail), check_result
