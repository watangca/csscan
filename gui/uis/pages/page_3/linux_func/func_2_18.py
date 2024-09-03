def check_func_2_18(client):
    no = "2_18"
    check_detail = ""
    check_result = "N/A"

    try:
        # /etc/passwd 파일에서 사용자 정보를 가져옵니다.
        stdin, stdout, stderr = client.exec_command('cat /etc/passwd')
        passwd_content = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()

        if passwd_content:
            # 실제 사용자별 홈 디렉토리 확인 (UID가 1000 이상이고 /home/으로 시작하는 경우)
            missing_homes = []
            for line in passwd_content.splitlines():
                parts = line.split(':')
                if len(parts) > 6 and parts[2].isdigit() and int(parts[2]) >= 1000 and parts[5].startswith("/home/"):
                    user = parts[0]
                    home_dir = parts[5]
                    # 홈 디렉토리 존재 여부 확인
                    stdin, stdout, stderr = client.exec_command(f'test -d {home_dir} && echo "exists" || echo "not exists"')
                    dir_exists = stdout.read().decode().strip()
                    if dir_exists == "not exists":
                        missing_homes.append(user)

            if missing_homes:
                check_detail = f"홈 디렉토리가 없는 사용자: {', '.join(missing_homes)}"
                check_result = "취약"
            else:
                check_detail = "모든 사용자의 홈 디렉토리가 존재함"
                check_result = "양호"
        else:
            # /etc/passwd 파일이 없거나 읽을 수 없는 경우
            check_detail = f"Error: {error if error else 'Unable to read /etc/passwd'}"
            check_result = "N/A"

    except Exception as e:
        check_detail = f"오류 발생: {str(e)}"
        check_result = "N/A"

    return no, check_detail, check_result
