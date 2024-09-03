def check_func_1_1(oracle_conn):
    no = "1_1"
    check_detail = "DBA 계정 중 패스워드 변경이력 점검"
    check_result = "n/a"

    try:
        # Oracle 데이터베이스에 SQL 명령 실행
        cursor = oracle_conn.cursor()

        # 패스워드 변경 이력 확인 쿼리
        query = """
        SELECT name, ptime
        FROM sys.user$
        WHERE name IN ('SYS', 'SYSTEM')
        """

        cursor.execute(query)
        output = cursor.fetchall()

        # 패스워드 변경 이력 확인
        altered_accounts = []
        for row in output:
            username, ptime = row
            if ptime is not None:
                altered_accounts.append(f"{username}: {ptime}")

        # 결과 결정
        if altered_accounts:
            check_result = "양호"
            check_detail += f"\n변경된 계정: {', '.join(altered_accounts)}"
        else:
            check_result = "취약"
            check_detail += "\n패스워드 변경 이력 없음"

    except Exception as e:
        check_result = "n/a"
        check_detail += f"\n점검 중 오류 발생: {e}"

    finally:
        if 'cursor' in locals():
            cursor.close()

    return no, check_detail, check_result
