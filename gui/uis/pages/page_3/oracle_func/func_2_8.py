def check_func_2_8(client):
    no = "2_8"
    check_detail = []
    permissions_result = None
    admin_restrictions_result = None

    # 원격 시스템의 .bashrc 파일에서 ORACLE_HOME 환경 변수를 추출
    try:
        stdin, stdout, stderr = client.exec_command("grep ORACLE_HOME ~/.bashrc | cut -d '=' -f2")
        ORACLE_HOME = stdout.read().decode('utf-8').strip().strip('"').strip("'")
        if not ORACLE_HOME:
            raise ValueError("ORACLE_HOME environment variable is not found in .bashrc")
    except Exception as e:
        check_detail.append(f"Error finding ORACLE_HOME: {str(e)}")
        permissions_result = admin_restrictions_result = "n/a"

    if ORACLE_HOME:
        listener_ora_path = f"{ORACLE_HOME}/network/admin/listener.ora"

        # listener.ora 파일의 퍼미션 체크
        try:
            stdin, stdout, stderr = client.exec_command(f"stat -c '%a' {listener_ora_path}")
            permissions = stdout.read().decode('utf-8').strip()
            if permissions != "640":
                permissions_result = "취약"
                check_detail.append(f"listener.ora permissions are not set to 640: {permissions}")
            else:
                permissions_result = "양호"
                check_detail.append(f"listener.ora permissions: {permissions}")
        except Exception as e:
            check_detail.append(f"Error checking listener.ora permissions: {str(e)}")
            permissions_result = "n/a"

        # listener.ora 파일에서 ADMIN_RESTRICTIONS_LISTENER 설정값 파싱
        try:
            stdin, stdout, stderr = client.exec_command(f"grep 'ADMIN_RESTRICTIONS_LISTENER' {listener_ora_path}")
            admin_restrictions_config = stdout.read().decode('utf-8').strip()
            if "ADMIN_RESTRICTIONS_LISTENER=on" not in admin_restrictions_config:
                admin_restrictions_result = "취약"
                check_detail.append("ADMIN_RESTRICTIONS_LISTENER is not set to 'on'")
            else:
                admin_restrictions_result = "양호"
                check_detail.append("ADMIN_RESTRICTIONS_LISTENER setting is 'on'")
        except Exception as e:
            check_detail.append(f"Error reading ADMIN_RESTRICTIONS_LISTENER setting: {str(e)}")
            admin_restrictions_result = "n/a"

    # 결론 도출 로직
    if permissions_result == "n/a" and admin_restrictions_result == "n/a":
        check_result = "n/a"
    elif permissions_result == "취약" or admin_restrictions_result == "취약":
        check_result = "취약"
    elif permissions_result == "양호" and admin_restrictions_result == "양호":
        check_result = "양호"
    else:
        check_result = "n/a"  # 혹시 모를 상황에 대비

    return no, check_detail, check_result
