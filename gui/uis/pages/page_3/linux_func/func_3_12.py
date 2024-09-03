import re

def check_func_3_12(client):
    no = "3_12"
    check_detail = ""
    check_result = "n/a"  

    service_command = "ps -ef | grep [s]endmail"
    stdin, stdout, stderr = client.exec_command(service_command)
    service_output = stdout.read().decode().strip()

    if service_output:
        check_detail += "Sendmail 서비스 실행 중.\n"

        version_command = "sendmail -d0.1 -bt < /dev/null"
        stdin, stdout, stderr = client.exec_command(version_command)
        version_output = stdout.read().decode().strip()

        version_info = re.search(r"Version (\d+\.\d+\.\d+)", version_output)
        if version_info:
            check_detail += f"현재 Sendmail 버전: {version_info.group(1)}\n"
            check_result = "양호"
        else:
            check_detail += "Sendmail 버전을 확인할 수 없음.\n"
    else:
        check_detail += "Sendmail 서비스가 실행중이 아님.\n"
        check_result = "n/a"

    check_detail += "sendmail 최신 버전을 확인하고 적용여부를 판단해야함\n"

    return no, check_detail, check_result