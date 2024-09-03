def check_func_1_2(mysql_conn):
    no = "1_2"
    check_detail = "데이터베이스 사용자 계정 목록: "
    check_result = "n/a"

    try:
        # MySQL 데이터베이스에서 사용자 계정 목록 조회
        cursor = mysql_conn.cursor()
        cursor.execute("SELECT User FROM mysql.user")
        accounts = [row[0] for row in cursor]

        # 전체 계정 목록 출력 (콤마와 공백으로 구분)
        check_detail += ", ".join(accounts)

        # 'test'를 포함하는 계정 검사
        found_test_accounts = [acc for acc in accounts if 'test' in acc]
        if found_test_accounts:
            check_result = "취약"
            check_detail += f"\n발견된 불필요한 계정('test' 포함): {', '.join(found_test_accounts)}"
        else:
            check_result = "양호"
            check_detail += "\n불필요한 계정이 발견되지 않음"

    except Exception as e:
        check_detail += f"\n점검 중 오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
