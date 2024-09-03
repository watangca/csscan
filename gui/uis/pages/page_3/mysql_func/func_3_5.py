def check_func_3_5(mysql_conn):
    no = "3_5"
    check_detail = "일반 사용자 WITH_GRANT_OPTION 권한 설정 여부:"
    check_result = "n/a"  # 기본값 설정

    try:
        cursor = mysql_conn.cursor()
        # 사용자별 WITH_GRANT_OPTION 권한 점검, root 사용자를 제외
        cursor.execute("SELECT User, Host, Grant_priv FROM mysql.user WHERE Grant_priv = 'Y' AND User != 'root';")
        user_privs = cursor.fetchall()

        if user_privs:
            check_result = "취약"
            for user, host, grant_priv in user_privs:
                # 일반 사용자에게 WITH_GRANT_OPTION 권한이 부여된 경우
                check_detail += f"사용자 {user}@{host}에게 WITH_GRANT_OPTION 권한이 부여되어 있음. 실제로 DBA 계정인지 판단 필요"
        else:
            # 일반 사용자에게 WITH_GRANT_OPTION 권한이 부여되어 있지 않은 경우
            check_detail += "일반 사용자에게 WITH_GRANT_OPTION 권한이 부여되어 있지 않음."
            check_result = "양호"

    except Exception as e:
        check_detail += f"점검 중 오류 발생: {e}"
        check_result = "n/a"

    return no, check_detail.strip(), check_result
