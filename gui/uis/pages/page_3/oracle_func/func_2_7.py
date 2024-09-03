def check_func_2_7(client):
    no = "2_7"
    check_detail = []
    check_result = "n/a"  # 기본값 설정

    # 원격 시스템의 .bashrc 파일에서 ORACLE_HOME과 ORACLE_SID 환경 변수를 추출하는 함수
    def get_env_variable(command):
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('utf-8').strip()
        return output

    # .bashrc에서 ORACLE_HOME과 ORACLE_SID 값을 추출하는 커맨드
    oracle_home_command = "grep 'export ORACLE_HOME' ~/.bashrc | cut -d '=' -f2"
    oracle_sid_command = "grep 'export ORACLE_SID' ~/.bashrc | cut -d '=' -f2"

    ORACLE_HOME = get_env_variable(oracle_home_command).replace('"', '').replace("'", "")
    ORACLE_SID = get_env_variable(oracle_sid_command).replace('"', '').replace("'", "")

    if not ORACLE_HOME or not ORACLE_SID:
        check_detail.append("ORACLE_HOME or ORACLE_SID environment variable is not set.")
        return no, check_detail, check_result

    files_to_check = [
        f"{ORACLE_HOME}/bin/sqlplus",
        f"{ORACLE_HOME}/bin/lsnrctl",
        f"{ORACLE_HOME}/network/admin/listener.ora",
        f"{ORACLE_HOME}/network/admin/tnsnames.ora",
        f"{ORACLE_HOME}/dbs/init{ORACLE_SID}.ora",
    ]

    # 파일 권한을 체크하는 부분
    for file_path in files_to_check:
        # 파일 존재 여부 및 권한을 확인하는 커맨드
        command = f"if [ -f {file_path} ]; then ls -l {file_path}; else echo 'File not found: {file_path}'; fi"
        stdin, stdout, stderr = client.exec_command(command)
        result = stdout.read().decode('utf-8').strip()

        # 'File not found'를 체크하여 파일 존재 여부 확인
        if 'File not found' in result:
            check_detail.append(result)
        else:
            # 권한 부분만 추출하여 취약 여부 확인
            permissions, _, _, _, _, _, _, _, name = result.split()
            if 'w' in permissions[2:]:  # 다른 사용자의 쓰기 권한 확인
                check_detail.append(f"{name} vulnerable permissions: {permissions}")
            else:
                check_detail.append(f"{name} permissions are secure: {permissions}")

    # 결과 세팅
    check_result = "양호" if all('secure' in detail for detail in check_detail) else "취약"

    return no, check_detail, check_result

