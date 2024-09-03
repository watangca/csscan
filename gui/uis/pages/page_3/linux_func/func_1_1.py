import re

def check_func_1_1(client):
    no = "1_1"
    check_detail = "root 원격접속 제한:"
    check_result = "n/a"

    try:
        # telnet 서비스 점검
        stdin, stdout, stderr = client.exec_command('ps -A | grep telnet')
        telnet_services = stdout.read().decode('utf-8').strip()
        if telnet_services:
            check_detail += "telnet 서비스 사용 중\n"
            check_result = "취약"
        else:
            check_detail += "telnet 서비스 사용 안 함\n"

        # 파일 권한 확인을 위해 SFTP 클라이언트 사용
        sftp = client.open_sftp()
        sshd_config_attr = sftp.stat('/etc/ssh/sshd_config')
        file_mode = oct(sshd_config_attr.st_mode)[-3:]
        
        # 파일 권한에 따라 sudo 사용 결정
        if file_mode == '644':
            command = 'cat /etc/ssh/sshd_config'
        else:
            command = 'sudo cat /etc/ssh/sshd_config'

        stdin, stdout, stderr = client.exec_command(command)
        sshd_config_contents = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        if not sshd_config_contents and error:
            check_detail += f"sshd_config 파일 읽기 실패: {error}\n"
            check_result = "n/a"
        else:
            matches = re.findall(r'^\s*PermitRootLogin\s+(\w+)', sshd_config_contents, re.MULTILINE)
            if matches:
                permit_root_login = matches[-1].lower()
                check_detail += f"PermitRootLogin 설정: {permit_root_login}\n"
                check_result = "취약" if permit_root_login == 'yes' else "양호"
            else:
                check_detail += "PermitRootLogin 설정 발견되지 않음\n"
                check_result = "양호"

    except Exception as e:
        check_detail += f"점검 중 예외 발생: {e}\n"
        check_result = "n/a"

    finally:
        if sftp:
            sftp.close()

    return no, check_detail, check_result
