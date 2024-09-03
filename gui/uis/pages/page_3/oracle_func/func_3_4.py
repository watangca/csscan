def check_func_3_4(oracle_conn):
    no = "3_4"
    check_result = "n/a"  # 초기 기본값 설정
    check_detail = "Object Owner: "

    try:
        # Object Owner 점검을 위한 쿼리
        query = """
        Select distinct owner from dba_objects 
        where owner not in ('SYS','SYSTEM', 'MDSYS','CTXSYS','ORDSYS','ORDPLUGINS', 
        'AURORA$JIS$UTILITY$','HR','ODM','ODM_MTR','OE','OLAPDBA','OLAPSYS',
        'OSE$HTTP$ADMIN','OUTLN','LBACSYS','DMSYS','PM', 'PUBLIC','QS','QS_ADM','QS_CB',
        'QS_CBADM','DBSNMP','QS_CS','QS_ES','QS_OS', 'QS_WS','RMAN', 'SH', 'WKSYS', 
        'WMSYS','XDB') 
        and owner not in (select grantee from dba_role_privs where granted_role='DBA')
        """
        
        # 쿼리 실행
        cursor = oracle_conn.cursor()
        cursor.execute(query)
        owners = cursor.fetchall()

        if not owners:
            # 양호: 제한된 관리자 계정으로만 Object Owner가 존재하는 경우
            check_result = "양호"
            check_detail += "관리자 계정으로 제한됨"
        else:
            # 취약: 일반 사용자 계정이 Object Owner로 존재하는 경우
            check_result = "취약"
            owner_list = ', '.join([owner[0] for owner in owners])
            check_detail += owner_list

    except Exception as e:
        print(f"Error checking Object Owners: {e}")
        check_result = "n/a"
        check_detail += "점검 중 오류 발생"

    return no, check_detail, check_result
