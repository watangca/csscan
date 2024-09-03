def check_func_1_3(oracle_conn):
    no = "1_3"
    check_detail = "패스워드 복잡도 정책 적용 여부: "
    check_result = "n/a"

    try:
        # Oracle 데이터베이스에서 패스워드 정책 설정 확인
        cursor = oracle_conn.cursor()
        cursor.execute("""
            SELECT resource_name, limit 
            FROM dba_profiles 
            WHERE profile = 'DEFAULT' AND 
            resource_name IN ('FAILED_LOGIN_ATTEMPTS', 'PASSWORD_LIFE_TIME', 'PASSWORD_REUSE_TIME', 'PASSWORD_REUSE_MAX')
        """)
        policy_settings = {row[0]: row[1] for row in cursor}

        # 패스워드 정책 적용 여부 확인
        if all(policy_settings.values()):
            check_result = "양호"
            check_detail += f"적용됨 (설정: {policy_settings})"
        else:
            check_result = "취약"
            check_detail += "적용되지 않음"

    except Exception as e:
        check_detail += f"점검 중 오류 발생: {str(e)}"
        check_result = "n/a"

    return no, check_detail, check_result
