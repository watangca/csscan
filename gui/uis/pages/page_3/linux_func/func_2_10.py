def check_func_2_10(client):
    no = "2_10"
    check_detail = ""
    check_result = "N/A"
    found_files = False  

    env_files = ['.bashrc', '.bash_profile', '.zshrc', '.profile','.kshrc','.cshrc','.login']

    try:
        for file in env_files:
            # 파일의 소유자 및 권한 확인
            stdin, stdout, stderr = client.exec_command(f'ls -l ~/{file}')
            file_info = stdout.read().decode('utf-8').strip()

            if file_info and 'No such file or directory' not in file_info:
                found_files = True  # 파일을 발견함
                check_detail += f"{file_info}\n"
                parts = file_info.split()

                # 권한 및 소유자 추출
                permissions = parts[0]
                owner = parts[2]

                # 소유자가 root 또는 해당 사용자이고, 쓰기 권한이 소유자와 root에게만 있는지 확인
                if (owner == 'root' or owner == client.get_transport().get_username()) and all(char in ['-', 'w'] for char in permissions[3:]):
                    check_result = "양호"
                else:
                    check_result = "취약"

        if not found_files:
            check_detail = "환경 파일을 찾을 수 없음"

    except Exception as e:
        check_detail = f"오류 발생: {str(e)}"
        check_result = "N/A"

    return no, check_detail.strip(), check_result