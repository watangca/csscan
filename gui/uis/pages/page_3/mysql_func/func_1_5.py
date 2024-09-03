def check_func_1_5(mysql_conn):
    no = "1_5"
    check_detail = ""
    check_result = "n/a"

    try:
        cursor = mysql_conn.cursor()

        # password_history와 password_reuse_interval 설정값 조회
        cursor.execute("SHOW VARIABLES LIKE 'password_history';")
        password_history = cursor.fetchone()

        cursor.execute("SHOW VARIABLES LIKE 'password_reuse_interval';")
        password_reuse_interval = cursor.fetchone()

        # 결과 처리
        history_setting = password_history[1] if password_history else "Not Set"
        interval_setting = password_reuse_interval[1] if password_reuse_interval else "Not Set"

        check_detail = f"PASSWORD_HISTORY={history_setting}, PASSWORD_REUSE_INTERVAL={interval_setting}"

        if history_setting != '0' and interval_setting != '0':
            check_result = "양호"
        else:
            check_result = "취약"

    except Exception as e:
        check_detail = f"오류 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result
