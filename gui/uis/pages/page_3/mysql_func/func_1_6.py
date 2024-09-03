def check_func_1_6(mysql_conn):
    no = "1_6"
    check_detail = "DBA 계정 외 계정: "
    check_result = "양호"  # 무조건 양호로 판단

    try:
        cursor = mysql_conn.cursor()
        query = "SELECT User, Host FROM mysql.user WHERE User NOT IN ('root', 'mysql.session', 'mysql.sys', 'debian-sys-maint', 'phpmyadmin')"
        cursor.execute(query)

        users = cursor.fetchall()
        if users:
            user_list = [f"{user[0]}@{user[1]}" for user in users]
            check_detail += ", ".join(user_list)
        else:
            check_detail += "없음"
        check_detail += ". 출력된 계정에 대한 공용계정으로 사용 여부 인터뷰 필요."

    except Exception as e:
        check_detail = f"오류 발생: {e}"
        check_result = "n/a"
    finally:
        cursor.close()

    return no, check_detail, check_result
