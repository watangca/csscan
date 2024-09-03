def check_func_3_35(client):
    no = "3_35"
    check_detail = ""
    check_result = "양호"  # 기본값 설정

    config_files = ['/etc/apache2/apache2.conf', '/etc/httpd/conf/httpd.conf']
    required_settings = {
        'ServerTokens': 'Prod',
        'ServerSignature': 'Off',
    }
    settings_found = {
        'ServerTokens': False,
        'ServerSignature': False,
    }

    try:
        for config_file in config_files:
            # 각 설정 파일에서 ServerTokens 및 ServerSignature 설정 확인
            stdin, stdout, stderr = client.exec_command(f'grep -E "ServerTokens|ServerSignature" {config_file}')
            config_output = stdout.read().decode('utf-8').strip()
            error = stderr.read().decode('utf-8').strip()

            if not error and config_output:
                check_detail += f"{config_file} 설정:\n{config_output}\n"
                # 필요한 설정이 적절히 설정되었는지 확인
                for line in config_output.split('\n'):
                    for setting in required_settings:
                        if setting in line:
                            if required_settings[setting] in line.split():
                                settings_found[setting] = True

        # 모든 필요한 설정이 적절히 설정되었는지 최종 확인
        if all(settings_found.values()):
            check_result = "양호"
        else:
            check_result = "취약"
            if not settings_found['ServerTokens']:
                check_detail += "ServerTokens가 Prod로 설정되지 않음\n"
            if not settings_found['ServerSignature']:
                check_detail += "ServerSignature가 Off로 설정되지 않음\n"

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
