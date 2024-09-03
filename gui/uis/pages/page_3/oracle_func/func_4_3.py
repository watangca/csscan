def check_func_4_3(client):
    no = "4_3"
    check_detail = "시스템에 적용된 Critical Patch Updates (CPUs), Patch Set Updates (PSUs), Release Update (RUs): "

    try:
        # 원격 시스템의 .bashrc 및 .bash_profile 파일에서 ORACLE_HOME 환경 변수를 추출
        stdin, stdout, stderr = client.exec_command("grep ORACLE_HOME ~/.bashrc ~/.bash_profile | cut -d '=' -f2")
        ORACLE_HOME = stdout.read().decode('utf-8').strip().strip('"').strip("'")
        if not ORACLE_HOME:
            raise ValueError("ORACLE_HOME 환경 변수를 .bashrc 및 .bash_profile에서 찾을 수 없습니다.")

        # ORACLE_HOME을 기반으로 OPatch 명령어 실행하여 패치 정보 확인
        opatch_command = f"{ORACLE_HOME}/OPatch/opatch lsinventory"
        stdin, stdout, stderr = client.exec_command(opatch_command)
        patches_info = stdout.read().decode('utf-8').strip()
        if patches_info:
            check_detail += patches_info
        else:
            check_detail += "최신 CPUs, PSUs, RUs를 확인하여 영향도 평가를 실시하고 패치 적용여부를 판단해야함."

        check_result = "양호"  # 이 점검 항목은 결과에 상관없이 '양호'로 판단됩니다.

    except Exception as e:
        check_detail = f"패치 정보 확인 중 오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
