def check_func_4_2(mysql_conn):
    no = "4_2"
    check_detail = "감사로그 설정 점검: "
    check_result = "n/a"  # 기본값 설정

    try:
        cursor = mysql_conn.cursor()
        # 모든 플러그인의 상태 확인
        cursor.execute("SHOW PLUGINS;")
        plugins = cursor.fetchall()

        # 특정 플러그인이 활성화되어 있는지 검사
        audit_log_active = False
        for plugin in plugins:
            if plugin[0] == 'audit_log' and plugin[1] == 'ACTIVE':
                audit_log_active = True
                check_detail += f"활성화된 감사 로그 플러그인: {plugin[0]}, 상태: {plugin[1]}"
                break
        
        if audit_log_active:
            check_result = "양호"
        else:
            check_detail += "감사 로그 플러그인이 활성화되지 않음."
            check_result = "취약"

    except Exception as e:
        check_detail += f"점검 중 오류 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result
