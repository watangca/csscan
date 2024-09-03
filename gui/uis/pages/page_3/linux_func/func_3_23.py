def check_func_3_23(client):
    no = "3_23"
    check_detail = ""
    check_result = "n/a"

    try:
        # Apache 웹 서버 실행 여부 확인
        stdin, stdout, stderr = client.exec_command('ps -A | grep apache2')
        apache_running = stdout.read().decode('utf-8').strip()

        if apache_running:
            check_detail += "웹서버 실행 중,"
            config_files = ['/etc/apache2/apache2.conf', '/etc/httpd/conf/httpd.conf']
            document_root_found = False

            # 기본 디렉터리 리스트
            default_dirs = [
                '"/usr/local/apache/htdocs"',
                '"/usr/local/apache2/htdocs"',
                '"/var/www/html"'
            ]

            # 각 설정 파일에서 DocumentRoot 확인
            for config_file in config_files:
                stdin, stdout, stderr = client.exec_command(f'cat {config_file} | grep -i "DocumentRoot"')
                document_root = stdout.read().decode('utf-8').strip()
                if document_root:
                    document_root_found = True
                    if any(default_dir in document_root for default_dir in default_dirs):
                        check_result = "취약"
                        check_detail += f"DocumentRoot가 기본 디렉터리로 설정됨: {document_root}\n"
                        break
                    else:
                        check_result = "양호"
                        check_detail += f"DocumentRoot가 별도의 디렉터리로 설정됨: {document_root}\n"

            if not document_root_found:
                check_result = "취약"
                check_detail += "DocumentRoot 설정이 없으므로 기본 디렉터리를 사용 중임\n"
        else:
            check_detail += "웹서버 비활성화"
            check_result = "n/a"
    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"

    return no, check_detail, check_result
