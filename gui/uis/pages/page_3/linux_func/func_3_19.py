def check_func_3_19(client):
    no = "3_19"
    check_detail = ""
    check_result = "n/a"  # 기본 결과 설정

    # Apache 설정 파일 경로 목록
    apache_config_paths = [
        '/etc/apache2/apache2.conf',
        '/etc/httpd/conf/httpd.conf'
    ]

    try:
        # Apache 웹서버 실행 여부 확인
        stdin, stdout, stderr = client.exec_command('ps -A')
        output = stdout.read().decode('utf-8')
        if 'apache' in output.lower():
            found_config = False
            for config_path in apache_config_paths:
                # 설정 파일 존재 여부 확인
                stdin, stdout, stderr = client.exec_command(f'test -f {config_path} && echo exists')
                if stdout.read().decode('utf-8').strip() == 'exists':
                    found_config = True
                    # AllowOverride 설정값과 해당 디렉터리 경로 파싱
                    command = f"awk '/<Directory/,/Directory>/' {config_path} | grep -E 'Directory|AllowOverride'"
                    stdin, stdout, stderr = client.exec_command(command)
                    lines = stdout.readlines()

                    directory = ""
                    for line in lines:
                        if '<Directory' in line:
                            directory = line.split()[1].strip('>').strip('"')
                        elif 'AllowOverride' in line:
                            allow_override = line.strip().split()[1]
                            check_detail += f"{directory} 지시자: AllowOverride {allow_override}; "

                    if 'AllowOverride None' in check_detail:
                        check_result = "취약"
                    else:
                        # 'None' 설정이 전혀 없다면 양호로 판단할 수 있지만, 이는 보안 정책에 따라 달라질 수 있음
                        check_result = "양호"
                    break  # 첫 번째 발견한 설정 파일에서 판단 종료
            
            if not found_config:
                check_detail += "Apache 설정 파일을 찾을 수 없음. "
                check_result = "n/a"
        else:
            check_detail += "실행 중인 Apache 웹 서버가 발견되지 않음. "
    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"

    return no, check_detail.strip(), check_result
