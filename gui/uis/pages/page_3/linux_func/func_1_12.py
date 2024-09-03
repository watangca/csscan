def check_func_1_12(client):
    no = "1_12"
    check_detail = ""
    check_result = "N/A"

    try:
        # 그룹 파일에서 GID와 그룹명 가져오기
        stdin, stdout, stderr = client.exec_command('cut -d: -f1,3 /etc/group')
        group_info = stdout.read().decode().strip().split('\n')
        group_dict = {gid: name for name, gid in (line.split(':') for line in group_info)}

        # 패스워드 파일에서 GID 가져오기
        stdin, stdout, stderr = client.exec_command('cut -d: -f4 /etc/passwd')
        passwd_gids = set(stdout.read().decode().strip().split('\n'))

        # 계정이 없는 GID 찾기
        orphan_gids = set(group_dict.keys()) - passwd_gids

        if orphan_gids:
            orphan_group_names = [group_dict[gid] for gid in orphan_gids]
            check_detail = f"계정이 존재하지 않는 그룹명: {', '.join(orphan_group_names)}"
            check_detail += " 계정이 존재하지 않는 그룹명 사용여부 판단 필요"
            check_result = "취약"
        else:
            check_detail = "계정이 존재하지 않는 GID가 발견되지 않음"
            check_result = "양호"

    except Exception as e:
        check_detail = f"설정을 확인하는 동안 오류가 발생했습니다: {e}"
        check_result = "N/A"

    return no, check_detail, check_result
