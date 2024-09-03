def check_func_1_11(client):
    no = "1_11"
    check_detail = ""
    check_result = "N/A"
    
    try:
        # root 그룹에 포함된 계정 확인
        stdin, stdout, stderr = client.exec_command('getent group root')
        root_group_output = stdout.read().decode('utf-8').strip()
        
        # root 그룹에 포함된 계정 파싱
        root_accounts_str = root_group_output.split(':')[3]  # 계정 부분만 추출
        root_accounts = root_accounts_str.split(',') if root_accounts_str else []
        
        # root 계정 외 추가된 계정이 없는 경우 'root_accounts_str'은 비어있음
        if root_accounts_str:
            # root 계정 외 추가된 계정이 있는지 확인
            additional_accounts = [account for account in root_accounts if account != 'root']
            if additional_accounts:
                check_detail += f"root 그룹에 추가된 계정: {', '.join(additional_accounts)}\n"
                check_detail += "추가된 계정에 대한 사용여부 판단 필요\n"
                check_result = "취약"
            else:
                check_detail += "root 그룹에 root 계정 외 추가된 계정 없음\n"
                check_result = "양호"
        else:
            check_detail += "root 그룹에 root 계정 외 추가된 계정 없음\n"
            check_result = "양호"
        
    except Exception as e:
        check_detail += f"점검 중 오류 발생: {e}\n"
        check_result = "N/A"

    return no, check_detail, check_result
