def check_func_3_4(client):
    no = "3_4"
    check_detail = "crontab 파일 및 사용 권한 확인"
    check_result = "N/A"  # 초기 결과를 'N/A'로 설정

    # crontab 명령어 위치 찾기
    stdin, stdout, stderr = client.exec_command("which crontab")
    crontab_path = stdout.read().decode().strip()
    if not crontab_path:
        check_detail = "crontab 파일을 찾을 수 없음"
        return no, check_detail, "n/a"

    # /etc/cron.deny 파일 존재 및 내용 확인 (일반 사용자의 crontab 사용 금지 여부)
    stdin, stdout, stderr = client.exec_command("cat /etc/cron.deny")
    cron_deny_content = stdout.read().decode().strip()
    if "ALL" in cron_deny_content.upper():
        user_crontab_denied = True
    else:
        user_crontab_denied = False

    # crontab 파일 권한 확인
    stdin, stdout, stderr = client.exec_command(f"ls -l {crontab_path}")
    crontab_permission = stdout.read().decode().strip()
    if not crontab_permission:
        check_detail = "crontab 파일의 권한을 확인할 수 없음"
        return no, check_detail, "n/a"

    check_detail = crontab_permission
    permission_part = crontab_permission.split()[0]

    # 권한 문자열 분석 및 검사 개선
    user_perm = permission_part[1:4]
    group_perm = permission_part[4:7]
    others_perm = permission_part[7:10]

    # 사용자 및 그룹 권한이 적절한지, 그리고 기타 사용자에게 권한이 없는지 확인
    is_permission_ok = (user_perm in ['rw-', 'r--', '-w-', '---'] and
                        group_perm in ['r--', '---'] and
                        others_perm == '---')

    # 권한이 640 이하이고 일반 사용자의 crontab 사용이 금지된 경우 양호
    if is_permission_ok and user_crontab_denied:
        check_result = "양호"
    else:
        check_result = "취약"

    return no, check_detail, check_result
