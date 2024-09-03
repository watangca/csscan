def check_func_1_13(client):
    no = "1_13"
    check_detail = ""
    check_result = "N/A"

    try:
        # /etc/passwd에서 모든 UID 가져오기
        stdin, stdout, stderr = client.exec_command('cut -d: -f3 /etc/passwd')
        uids = stdout.read().decode().strip().split('\n')
        
        # UID별로 계정 이름 가져오기
        stdin, stdout, stderr = client.exec_command('cut -d: -f1,3 /etc/passwd')
        accounts = stdout.read().decode().strip().split('\n')

        # 각 UID에 대한 계정 이름을 저장하는 딕셔너리 생성
        uid_to_accounts = {}
        for account in accounts:
            name, uid = account.split(':')
            if uid in uid_to_accounts:
                uid_to_accounts[uid].append(name)
            else:
                uid_to_accounts[uid] = [name]
        
        # 동일한 UID를 공유하는 계정 확인
        duplicate_uids = {uid: names for uid, names in uid_to_accounts.items() if len(names) > 1}

        if duplicate_uids:
            details = []
            for uid, names in duplicate_uids.items():
                details.append(f"UID {uid}: " + ", ".join(names))
            check_detail = "\n".join(details)
            check_result = "취약"
        else:
            check_detail = "동일한 UID로 설정된 사용자 계정이 존재하지 않음"
            check_result = "양호"

    except Exception as e:
        check_detail = f"/etc/passwd 파일을 확인하는 중 오류가 발생했습니다: {e}"
        check_result = "N/A"

    return no, check_detail, check_result
