def check_func_2_17(client):
    no = "2_17"
    check_detail = ""
    check_result = "n/a"  # 기본값

    try:
        # /etc/passwd 파일에서 사용자 정보 가져오기
        stdin, stdout, stderr = client.exec_command("cat /etc/passwd")
        passwd_output = stdout.read().decode('utf-8').strip()

        # /home 디렉토리에 있는 사용자 계정에 대해서만 권한 확인
        for line in passwd_output.split('\n'):
            parts = line.split(':')
            if len(parts) > 6:
                username = parts[0]
                home_dir = parts[5]
                if home_dir.startswith("/home/") and username != "nobody":  # 홈 디렉토리가 /home으로 시작하고 nobody 사용자가 아닌 경우에만 점검
                    command = f"ls -ald {home_dir}"
                    stdin, stdout, stderr = client.exec_command(command)
                    ls_output = stdout.read().decode('utf-8').strip()

                    if ls_output and not ls_output.startswith("ls:"):
                        try:
                            permissions, _, owner, _ = ls_output.split()[:4]
                            # 권한 상세 정보 추가
                            detail_info = f"홈디렉토리: {home_dir}, 소유자: {owner}, 권한: {permissions}"
                            if owner != username:
                                check_detail += f"{username}: 홈 디렉토리 소유자 불일치, {detail_info}\n"
                                check_result = "취약"
                            elif 'w' in permissions[7]:  # 타 사용자의 쓰기 권한 확인
                                check_detail += f"{username}: 타 사용자의 쓰기 권한 존재, {detail_info}\n"
                                check_result = "취약"
                            else:
                                check_detail += f"{detail_info}\n"
                                check_result = "양호"
                        except ValueError:
                            check_detail += f"{username}: ls 명령 결과 형식 오류\n"
                    else:
                        # 홈 디렉토리 정보가 없거나 ls 명령에 오류가 있는 경우는 출력하지 않음
                        pass

    except Exception as e:
        check_detail = f"오류 발생: {str(e)}"

    return no, check_detail, check_result
