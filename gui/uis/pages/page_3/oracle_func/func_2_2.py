def check_func_2_2(oracle_conn):
    no = "2_2"
    check_detail = "DBA만 접근 가능한 테이블에 접근 계정 및 권한 확인: "
    check_result = "n/a"  # 초기 상태 설정

    # SQL 쿼리
    query = """
    SELECT grantee, privilege, owner, table_name 
    FROM dba_tab_privs 
    WHERE (owner='SYS' OR table_name LIKE 'DBA_%') 
    AND privilege <> 'EXECUTE' 
    AND grantee NOT IN ('PUBLIC', 'AQ_ADMINISTRATOR_ROLE', 'AQ_USER_ROLE', 'AURORA$JIS$UTILITY$', 'OSE$HTTP$ADMIN', 'TRACESVR', 'CTXSYS', 'DBA', 'DELETE_CATALOG_ROLE', 'EXECUTE_CATALOG_ROLE', 'EXP_FULL_DATABASE', 'GATHER_SYSTEM_STATISTICS', 'HS_ADMIN_ROLE', 'IMP_FULL_DATABASE', 'LOGSTDBY_ADMINISTRATOR', 'MDSYS','ODM', 'OEM_MONITOR', 'OLAPSYS', 'ORDSYS', 'OUTLN', 'RECOVERY_CATALOG_OWNER', 'SELECT_CATALOG_ROLE', 'SNMPAGENT', 'SYSTEM', 'WKSYS', 'WKUSER', 'WMSYS', 'WM_ADMIN_ROLE', 'XDB', 'LBACSYS', 'PERFSTAT', 'XDBADMIN')
    AND grantee NOT IN (SELECT grantee FROM dba_role_privs WHERE granted_role='DBA') 
    ORDER BY grantee
    """

    try:
        cursor = oracle_conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            # 접근 권한이 있는 계정이 있는 경우
            for row in results:
                check_detail += f"\nGrantee: {row[0]}, Privilege: {row[1]}, Owner: {row[2]}, Table_Name: {row[3]}"
            check_result = "취약"
        else:
            # DBA만 접근 가능한 테이블에 대한 권한을 가진 계정이 없는 경우
            check_detail = "DBA만 접근 가능한 테이블에 대한 권한을 가진 계정 없음."
            check_result = "양호"

    except Exception as e:
        check_detail += f"오류 발생: {str(e)}"
        check_result = "n/a"

    finally:
        if cursor:
            cursor.close()

    return no, check_detail, check_result
