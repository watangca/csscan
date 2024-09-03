def check_func_2_3(client):
    no = "2_3"
    # ORACLE_HOME 환경 변수 값을 얻어옵니다.
    stdin, stdout, stderr = client.exec_command("echo $ORACLE_HOME")
    oracle_home = stdout.read().decode('utf-8').strip()
    
    # ORACLE_HOME 값을 바탕으로 listener.ora 파일의 경로를 구성합니다.
    listener_file_path = f"{oracle_home}/network/admin/listener.ora"
    
    # listener.ora 파일 내에서 PASSWORDS_LISTENER 변수 존재 여부를 확인하는 명령을 구성합니다.
    command = f"grep 'PASSWORDS_LISTENER' {listener_file_path}"

    try:
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('utf-8').strip()

        if output:
            check_detail = "Listener 패스워드 보호 활성화 (암호화된 패스워드 발견)"
            check_result = "양호"
        else:
            check_detail = "Listener 패스워드 보호 비활성화 (암호화된 패스워드 미발견)"
            check_result = "취약"
    except Exception as e:
        check_detail = f"점검 중 예외 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
