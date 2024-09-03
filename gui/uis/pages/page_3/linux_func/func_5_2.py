def check_func_5_2(client):
    no = "5_2"
    check_detail = ""
    check_result = "n/a"

    try:
        # syslogd 서비스 활성 여부 확인
        stdin, stdout, stderr = client.exec_command('ps -ef | grep syslogd | grep -v grep')
        syslogd_active = stdout.read().decode('utf-8').strip()

        if syslogd_active:
            check_detail += "syslogd 서비스 활성화\n"
        else:
            check_detail += "syslogd 서비스 비활성화\n"

        # syslog.conf 및 rsyslog.conf 설정 확인
        config_files = ['/etc/syslog.conf', '/etc/rsyslog.conf']
        required_settings = [
            'mail.debug /var/log/mail.log',
            '*.info /var/log/syslog.log',
            '*.alert /var/log/syslog.log',
            '*.alert /dev/console',
            '*.alert root',
            '*.emerg *'
        ]
        settings_found = {setting: False for setting in required_settings}

        for file_path in config_files:
            stdin, stdout, stderr = client.exec_command(f'cat {file_path}')
            config_content = stdout.read().decode('utf-8').strip()
            error = stderr.read().decode('utf-8').strip()

            if error:
                check_detail += f"{file_path} 파일 확인 중 오류 발생: {error}\n"
            else:
                for setting in required_settings:
                    if setting in config_content:
                        settings_found[setting] = True

        # 설정된 내용 확인
        for setting, found in settings_found.items():
            if found:
                check_detail += f"{setting} 설정됨\n"
            else:
                check_detail += f"{setting} 미설정\n"
                check_result = "취약"

        if all(settings_found.values()):
            check_result = "양호"

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
