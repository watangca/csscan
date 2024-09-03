def check_func_1_5(oracle_conn):
    no = "1_5"
    check_detail = ""
    check_result = "n/a"

    try:
        cursor = oracle_conn.cursor()

        # PASSWORD_REUSE_TIME 및 PASSWORD_REUSE_MAX 설정값 조회
        cursor.execute("""
            SELECT resource_name, limit
            FROM dba_profiles
            WHERE resource_name IN ('PASSWORD_REUSE_TIME', 'PASSWORD_REUSE_MAX')
            AND profile = 'DEFAULT'
        """)
        rows = cursor.fetchall()

        # 결과 처리
        settings = {}
        for row in rows:
            settings[row[0]] = row[1]

        # Check_detail 설정
        check_detail = f"PASSWORD_REUSE_TIME={settings.get('PASSWORD_REUSE_TIME', 'Not Set')}, PASSWORD_REUSE_MAX={settings.get('PASSWORD_REUSE_MAX', 'Not Set')}"

        if settings.get('PASSWORD_REUSE_TIME') != 'UNLIMITED' and settings.get('PASSWORD_REUSE_MAX') != 'UNLIMITED':
            check_result = "양호"
        else:
            check_result = "취약"

    except Exception as e:
        check_detail = f"오류 발생: {e}"
        check_result = "n/a"

    return no, check_detail, check_result
