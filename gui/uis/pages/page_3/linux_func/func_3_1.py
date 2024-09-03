def check_func_3_1(client):
    no = "3_1"
    check_detail = ""  # 상세 검사 결과를 저장할 변수 초기화
    check_result = ""  # 검사 결과를 저장할 변수 초기화

    try:
        # OS 확인
        stdin, stdout, stderr = client.exec_command("cat /etc/*release")
        os_info = stdout.read().decode('utf-8').lower()
        if not os_info:
            raise ValueError("OS 정보를 확인할 수 없습니다.")

        # 패키지 설치 및 서비스 상태 확인 명령 선택
        if "ubuntu" in os_info or "debian" in os_info:
            check_command = "dpkg -l | grep -i finger; systemctl is-active inetd"
        elif "centos" in os_info or "red hat" in os_info or "fedora" in os_info or "amazon linux" in os_info:
            check_command = "rpm -q finger; systemctl is-active xinetd"
        else:
            raise ValueError("지원하지 않는 OS입니다.")

        # 패키지 및 서비스 상태 확인
        stdin, stdout, stderr = client.exec_command(check_command)
        output = stdout.read().decode('utf-8')
        if "no package" in output.lower() or "not installed" in output.lower():
            check_detail = "Finger 패키지 미설치"
            check_result = "n/a"
        elif "active" in output.lower():
            check_detail = "Finger 패키지 설치됨, 서비스 활성화됨"
            check_result = "취약"
        else:
            check_detail = "Finger 패키지 설치됨, 서비스 비활성화됨"
            check_result = "양호"

    except ValueError as e:
        check_detail = str(e)
        check_result = "n/a"
    except Exception as e:
        check_detail = "검사 중 예외 발생: " + str(e)
        check_result = "오류"

    return no, check_detail, check_result
