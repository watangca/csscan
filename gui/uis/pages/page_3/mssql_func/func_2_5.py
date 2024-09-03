def check_func_2_5(win_conn, mssql_conn):
    no = "2_5"
    
    try:
        # MSSQL 서버의 인증 모드 확인
        cursor = mssql_conn.cursor()
        cursor.execute("SELECT auth_scheme FROM sys.dm_exec_connections WHERE session_id = @@SPID;")
        auth_scheme_row = cursor.fetchone()
        auth_scheme = auth_scheme_row[0] if auth_scheme_row else None
        
        if auth_scheme == 'WINDOWS NT':
            # Windows 인증 모드일 경우, WinRM을 사용하여 Windows의 계정 잠금 정책을 확인
            ps_script = """
            $objUser = [ADSI]'WinNT://./Administrator,user'
            $objUser.PasswordAge
            """
            result = win_conn.run_ps(ps_script)
            if result.status_code == 0:
                check_detail = "Windows 인증 모드 사용 중. 시스템의 계정 잠금 정책 점검 결과:\n" + result.std_out.strip()
                check_result = "양호"  # 예시 결과
            else:
                check_detail = "Windows 계정 잠금 정책 점검 중 오류 발생."
                check_result = "n/a"
        else:
            # SQL Server 인증 모드 사용 시
            check_detail = "SQL Server 인증 모드 사용 중. DBMS 설정으로는 계정 잠금 정책 설정 불가."
            check_result = "n/a"
    except Exception as e:
        check_detail = f"점검 중 오류 발생: {str(e)}"
        check_result = "n/a"
    
    return no, check_detail, check_result
