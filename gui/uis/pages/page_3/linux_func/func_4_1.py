def check_func_4_1(client):
    no = "4_1"
    check_detail = ""
    check_result = "n/a"

    try:
        # 운영체제 확인
        stdin, stdout, stderr = client.exec_command('cat /etc/*release')
        os_info = stdout.read().decode('utf-8').lower()

        if 'ubuntu' in os_info or 'debian' in os_info:
            # Ubuntu/Debian 시스템 업데이트 목록 확인
            client.exec_command('sudo apt update')  # 업데이트 정보 갱신
            stdin, stdout, stderr = client.exec_command('apt list --upgradable')
            updates = stdout.read().decode('utf-8').strip()
            if 'upgradable' in updates:
                check_result = "취약"
                check_detail += "업데이트 가능한 보안 패치 목록 (Ubuntu/Debian):\n" + updates
            else:
                check_result = "양호"
                check_detail += "업데이트 가능한 보안 패치가 존재하지 않음 (Ubuntu/Debian)"
        elif 'centos' in os_info or 'red hat' in os_info or 'fedora' in os_info:
            # Red Hat/CentOS/Fedora 시스템 업데이트 목록 확인
            stdin, stdout, stderr = client.exec_command('sudo yum check-update || sudo dnf check-update')
            updates = stdout.read().decode('utf-8').strip()
            if updates and not updates.startswith('Last metadata expiration check'):
                check_result = "취약"
                check_detail += "업데이트 가능한 보안 패치 목록 (Red Hat/CentOS/Fedora):\n" + updates
            else:
                check_result = "양호"
                check_detail += "업데이트 가능한 보안 패치가 존재하지 않음 (Red Hat/CentOS/Fedora)"
        else:
            check_detail += "지원되지 않는 운영체제입니다."
            return no, check_detail, check_result

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
