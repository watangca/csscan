def check_func_3_21(client):
    no = "3_21"
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
            check_detail += "웹서버 실행 중 "

            # Apache 설정 파일에서 Options 지시자 확인
            found_options = False
            for config_path in apache_config_paths:
                stdin, stdout, stderr = client.exec_command(f'grep -i "Options" {config_path}')
                options = stdout.read().decode('utf-8').strip()

                if options:
                    found_options = True
                    # Options 설정 출력
                    check_detail += f"파일 {config_path} 내 현재 Options 설정: {options};\n"

                    if "FollowSymLinks" in options:
                        check_result = "취약"
                    else:
                        check_result = "양호"
                    break  # Options 설정을 찾으면 추가 검색 중단

            if not found_options:
                check_detail += "Apache 설정 파일에서 Options 지시자를 찾을 수 없음"
                check_result = "n/a"
        else:
            check_detail += "웹 서버 서비스가 발견되지 않음"
            check_result = "n/a"
    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"

    return no, check_detail, check_result
