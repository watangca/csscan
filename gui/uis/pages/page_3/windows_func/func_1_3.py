def check_func_1_3(client):
    no = "1_3"
    check_detail = ""
    check_result = ""

    # 변경 또는 제거 대상 계정 목록
    target_accounts = ['Administrator', 'Guest']
    # Windows 서버에서 일반적으로 사용되는 내장 계정 목록
    essential_accounts = [
        'DefaultAccount', 'WDAGUtilityAccount',
        'NetworkService', 'LocalService',
        'System', 'TrustedInstaller'
    ]

    try:
        # 원격 서버에서 모든 사용자 계정의 목록을 가져옴
        result = client.run_ps("Get-LocalUser | Select-Object -ExpandProperty 'Name'")

        if result.status_code == 0:
            user_list = [user.lower().strip() for user in result.std_out.decode().strip().split('\n')]
            non_essential_accounts = [user for user in user_list if user not in [acc.lower() for acc in essential_accounts + target_accounts]]
            found_target_accounts = [user for user in user_list if user in [acc.lower() for acc in target_accounts]]

            if non_essential_accounts or found_target_accounts:
                check_detail = "변경 또는 제거 대상 계정: " + ', '.join(found_target_accounts).title() if found_target_accounts else ""
                check_detail += " | 필수 계정 외 추가 계정: " + ', '.join(non_essential_accounts).title() if non_essential_accounts else ""
                check_result = "취약"
            else:
                check_detail = "변경 또는 제거 대상 계정이 발견되지 않음"
                check_result = "양호"
        else:
            check_detail = "사용자 계정 목록을 가져오는 데 실패했습니다."
            check_result = "n/a"

    except Exception as e:
        check_detail = f"계정 점검 중 오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
