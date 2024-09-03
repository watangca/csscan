def check_func_2_1(mysql_conn):
    no = "2_1"
    check_detail = "원격에서 db 서버로의 관리자 계정 접속제한 설정값: "
    check_result = "n/a"  # 초기 상태는 평가 불가능으로 설정

    try:
        cursor = mysql_conn.cursor()
        # 모든 권한을 가진 사용자 조회
        cursor.execute("""
            SELECT user, host FROM mysql.user 
            WHERE Select_priv = 'Y' 
            AND Insert_priv = 'Y' 
            AND Update_priv = 'Y'
            AND Delete_priv = 'Y' 
            AND Create_priv = 'Y' 
            AND Drop_priv = 'Y'
            AND Reload_priv = 'Y' 
            AND Shutdown_priv = 'Y' 
            AND Process_priv = 'Y'
            AND File_priv = 'Y' 
            AND Grant_priv = 'Y' 
            AND References_priv = 'Y'
            AND Index_priv = 'Y' 
            AND Alter_priv = 'Y' 
            AND Show_db_priv = 'Y'
            AND Super_priv = 'Y' 
            AND Create_tmp_table_priv = 'Y' 
            AND Lock_tables_priv = 'Y'
            AND Execute_priv = 'Y' 
            AND Repl_slave_priv = 'Y' 
            AND Repl_client_priv = 'Y'
            AND Create_view_priv = 'Y' 
            AND Show_view_priv = 'Y' 
            AND Create_routine_priv = 'Y'
            AND Alter_routine_priv = 'Y' 
            AND Create_user_priv = 'Y'
            AND Event_priv = 'Y' 
            AND Trigger_priv = 'Y'
        """)
        results = cursor.fetchall()

        if results:
            for user, host in results:
                if host == '%':
                    check_detail += f"사용자 {user}는 모든 호스트(%)에서 접속 허용됨 "
                    check_result = "취약"
                else:
                    check_detail += f"사용자 {user}는 접속 허용 호스트: {host} "
                    # 여러 관리자 계정 중 하나라도 모든 호스트에서 접속 허용되면 취약으로 설정
                    if check_result != "취약":
                        check_result = "양호"
        else:
            check_detail += "모든 권한을 가진 사용자 계정이 없습니다."
            check_result = "n/a"
    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"
    finally:
        if cursor:
            cursor.close()

    return no, check_detail, check_result
