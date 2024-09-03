def check_func_3_22(client):
    no = "3_22"
    check_detail = ""
    check_result = "n/a"

    # Ubuntu와 Red Hat 계열에서 Apache 설정 파일 경로
    apache_config_paths = [
        '/etc/apache2/apache2.conf',  # Ubuntu 기본 경로
        '/etc/httpd/conf/httpd.conf'  # Red Hat 계열 기본 경로
    ]

    try:
        # Apache 웹 서버 실행 여부 확인
        stdin, stdout, stderr = client.exec_command('ps -A | grep -E "apache2|httpd"')
        apache_running = stdout.read().decode('utf-8').strip()

        if apache_running:
            found_limit = False
            for config_path in apache_config_paths:
                # Apache 설정 파일에서 LimitRequestBody 확인
                stdin, stdout, stderr = client.exec_command(f'grep "LimitRequestBody" {config_path}')
                limit_body = stdout.read().decode('utf-8').strip()

                if limit_body:
                    found_limit = True
                    check_detail += f"LimitRequestBody 설정: {limit_body}."
                    check_result = "양호"
                    break  # 설정을 찾으면 추가 검색 중단

            if not found_limit:
                check_detail += "LimitRequestBody 설정 미발견."
                check_result = "취약"
        else:
            check_detail += "웹서버 비활성화"
            check_result = "n/a"
    except Exception as e:
        check_detail += f"오류: {str(e)}"

    return no, check_detail, check_result
