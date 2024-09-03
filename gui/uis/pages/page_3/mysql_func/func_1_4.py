def check_func_1_4(mysql_conn):
    no = "1_4"
    check_detail = ""
    check_result = "n/a"

    try:
        # MySQL 데이터베이스에 연결
        cursor = mysql_conn.cursor()

        # 모든 권한을 가진 사용자 조회
        cursor.execute("""
            SELECT User, Host 
            FROM mysql.user 
            WHERE Select_priv='Y' AND Insert_priv='Y' AND Update_priv='Y' AND Delete_priv='Y' 
                AND Create_priv='Y' AND Drop_priv='Y' AND Reload_priv='Y' AND Shutdown_priv='Y' 
                AND Process_priv='Y' AND File_priv='Y' AND Grant_priv='Y' AND References_priv='Y' 
                AND Index_priv='Y' AND Alter_priv='Y' AND Show_db_priv='Y' AND Super_priv='Y' 
                AND Create_tmp_table_priv='Y' AND Lock_tables_priv='Y' AND Execute_priv='Y' 
                AND Repl_slave_priv='Y' AND Repl_client_priv='Y' AND Create_view_priv='Y' 
                AND Show_view_priv='Y' AND Create_routine_priv='Y' AND Alter_routine_priv='Y' 
                AND Create_user_priv='Y' AND Event_priv='Y' AND Trigger_priv='Y' 
                AND User != 'root'
        """)
        sysadmin_users = cursor.fetchall()
        if sysadmin_users:
            check_detail += "root 외 sysadmin 계정: {}\n".format(", ".join([f"{user[0]}@{user[1]}" for user in sysadmin_users]))
            check_result = "취약"
        else:
            check_detail = "root 외 sysadmin 계정 없음"
            check_result = "양호"

    except Exception as e:
        check_detail = f"데이터베이스 접속 오류: {e}"
        check_result = "n/a"


    return no, check_detail, check_result
