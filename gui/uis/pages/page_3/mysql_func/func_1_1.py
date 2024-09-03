def check_func_1_1(mysql_conn):
    no = "1_1"
    check_detail = "mysql dba 계정 중 패스워드 변경 이력 출력"
    check_result = "n/a"

    try:
        # MySQL 데이터베이스에 SQL 명령 실행
        cursor = mysql_conn.cursor()

        # dba 계정명에 해당하는 부분을 실제 DBA 계정명으로 교체해야 함
        dba_account_name = 'root'

        # 패스워드 변경 이력 확인 쿼리
        query = f"""
        SELECT user, password_last_changed
        FROM mysql.user
        WHERE user='{dba_account_name}';
        """
        cursor.execute(query)
        output = cursor.fetchall()

        # 패스워드 변경 이력 확인
        if output and output[0][1] is not None:
            check_result = "양호"
            check_detail += f"\n패스워드 변경된 계정: {output[0][0]}, 변경 시각: {output[0][1]}"
        else:
            check_result = "취약"
            check_detail += "\n패스워드 변경 이력 없음"

    except Exception as e:
        check_result = "오류"
        check_detail += f"\n점검 중 오류 발생: {e}"

    finally:
        if 'cursor' in locals():
            cursor.close()

    return no, check_detail, check_result
