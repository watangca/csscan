def check_func_1_6(oracle_conn):
    no = "1_6"
    check_detail = "DBA 계정 외에 생성된 계정: "
    check_result = "양호"  # 기본적으로 "양호"로 설정

    try:
        cursor = oracle_conn.cursor()
        query = "SELECT username FROM dba_users WHERE username NOT IN ('SYS', 'SYSTEM') AND account_status = 'OPEN'"
        cursor.execute(query)

        # 쿼리 실행 결과를 저장하는 리스트
        users = [row[0] for row in cursor.fetchall()]

        if users:
            check_detail += ", ".join(users)
            check_detail += ". 출력된 계정에 대한 공용계정으로 사용 여부 인터뷰 필요."
        else:
            check_detail += "없음."

    except Exception as e:
        check_detail = f"오류 발생: {e}"
        check_result = "n/a"

    finally:
        if 'cursor' in locals():
            cursor.close()

    return no, check_detail, check_result
