def check_func_3_20(client):
    no = "3_20"
    check_detail = ""
    check_result = "n/a"

    try:
        # Apache 웹 서버 실행 여부 확인
        stdin, stdout, stderr = client.exec_command('ps -A | grep apache')
        apache_running = stdout.read().decode('utf-8').strip()

        if apache_running:
            check_detail += "웹서버 실행 중 "

            unnecessary_dirs = ['/var/www/htdocs/manual', '/var/www/manual']
            found_dirs = []
            for dir_path in unnecessary_dirs:
                stdin, stdout, stderr = client.exec_command(f'test -d {dir_path} && echo "found" || echo "not found"')
                if "found" in stdout.read().decode('utf-8').strip():
                    found_dirs.append(dir_path)

            if found_dirs:
                check_result = "취약"
                check_detail += f"다음의 불필요한 파일 및 디렉토리가 존재함: {', '.join(found_dirs)}"
            else:
                check_result = "양호"
                check_detail += "기본으로 생성되는 불필요한 파일 및 디렉토리가 없음"
        else:
            check_detail += "웹 서버가 실행 중이지 않습니다."
            check_result = "n/a"
    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"

    return no, check_detail, check_result
