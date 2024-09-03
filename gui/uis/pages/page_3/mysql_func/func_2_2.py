def check_func_2_2(mysql_conn):
    no = "2_2"
    check_detail = "mysql.user 테이블에 접근권한이 있는 일반 사용자 계정: "
    check_result = "n/a"  # 초기 상태 설정

    try:
        cursor = mysql_conn.cursor()
        # mysql.tables_priv 테이블에서 mysql.user 테이블에 대한 권한을 확인
        query = """
        SELECT grantee
        FROM information_schema.table_privileges 
        WHERE table_schema = 'mysql' AND table_name = 'user'
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            # 일반 사용자 계정 이름 목록
            user_accounts = [row[0] for row in results]
            if user_accounts:
                check_detail += ", ".join(user_accounts)
                check_result = "취약"
            else:
                check_detail += "없음"
                check_result = "양호"
        else:
            check_detail += "없음"
            check_result = "양호"

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    finally:
        if cursor:
            cursor.close()

    return no, check_detail, check_result
