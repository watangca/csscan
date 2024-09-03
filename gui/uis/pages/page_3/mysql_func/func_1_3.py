def check_func_1_3(mysql_conn):
    no = "1_3"
    check_detail = "패스워드 복잡도 정책 적용 여부: "
    check_result = "n/a"

    try:
        # MySQL에서 패스워드 복잡도 플러그인 설정 확인
        cursor = mysql_conn.cursor()
        cursor.execute("SHOW VARIABLES LIKE 'validate_password%';")
        policy_settings = {row[0]: row[1] for row in cursor}

        # 패스워드 정책 적용 여부 확인
        if policy_settings and all(value != 'OFF' for value in policy_settings.values()):
            check_result = "양호"
            check_detail += f"적용됨 (설정: {policy_settings})"
        else:
            check_result = "취약"
            check_detail += "적용되지 않음 또는 비활성화됨"

    except Exception as e:
        check_detail += f"점검 중 오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
