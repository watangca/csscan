def check_func_5_1(client):
    no = "5_1"
    check_detail = ""
    check_result = "양호"

    log_files = {
        'utmp': '/var/log/utmp',
        'wtmp': '/var/log/wtmp',
        'btmp': '/var/log/btmp',
        'su': '/var/log/auth.log',  # 'su' 로그는 대개 '/var/log/auth.log'에 기록됩니다.
        'xferlog': '/var/log/xferlog'
    }

    try:
        for log, path in log_files.items():
            # 각 로그 파일의 존재 여부 확인
            stdin, stdout, stderr = client.exec_command(f'ls {path}')
            output = stdout.read().decode('utf-8').strip()
            error = stderr.read().decode('utf-8').strip()

            if output:
                check_detail += f"{log} 로그 파일({path}) 로깅 중\n"
            else:
                check_detail += f"{log} 로그 파일({path})이 존재하지 않음\n"
                check_result = "취약"

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
