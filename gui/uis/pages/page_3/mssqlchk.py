import pyodbc
import winrm

def perform_mssql_checks(server, mssql_user, mssql_pass, database, windows_user, windows_pass):
    mssql_conn = None  # 초기값 설정
    try:
        mssql_conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={mssql_user};PWD={mssql_pass}'
        )
    except Exception as e:
        return [{"error": f"MSSQL 접속 실패: {str(e)}"}]

    win_conn = winrm.Session(server, auth=(windows_user, windows_pass), transport='ntlm')

    results = []

    try:
        # MSSQL 점검 함수 임포트
        from .mssql_func.func_1_1 import check_func_1_1
        from .mssql_func.func_1_2 import check_func_1_2
        from .mssql_func.func_1_3 import check_func_1_3
        from .mssql_func.func_1_4 import check_func_1_4
        from .mssql_func.func_1_5 import check_func_1_5
        from .mssql_func.func_1_6 import check_func_1_6
        from .mssql_func.func_2_1 import check_func_2_1
        from .mssql_func.func_2_2 import check_func_2_2
        from .mssql_func.func_2_3 import check_func_2_3
        from .mssql_func.func_2_4 import check_func_2_4
        from .mssql_func.func_2_5 import check_func_2_5  
        from .mssql_func.func_2_6 import check_func_2_6
        from .mssql_func.func_2_7 import check_func_2_7
        from .mssql_func.func_2_8 import check_func_2_8
        from .mssql_func.func_3_1 import check_func_3_1
        from .mssql_func.func_3_2 import check_func_3_2
        from .mssql_func.func_3_3 import check_func_3_3
        from .mssql_func.func_3_4 import check_func_3_4
        from .mssql_func.func_3_5 import check_func_3_5
        from .mssql_func.func_3_6 import check_func_3_6
        from .mssql_func.func_4_1 import check_func_4_1
        from .mssql_func.func_4_2 import check_func_4_2
        from .mssql_func.func_4_3 import check_func_4_3
        from .mssql_func.func_5_1 import check_func_5_1

        functions_to_check = [
            check_func_1_1, check_func_1_2, check_func_1_3, check_func_1_4, check_func_1_5,
            check_func_1_6, check_func_2_1, check_func_2_2, check_func_2_3, check_func_2_4, 
            check_func_2_5, check_func_2_6, check_func_2_7, check_func_2_8, check_func_3_1,
            check_func_3_2, check_func_3_3, check_func_3_4, check_func_3_5, check_func_3_6,
            check_func_4_1, check_func_4_2, check_func_4_3, check_func_5_1
        ]

        for function in functions_to_check:
            # 함수 이름을 기반으로 필요한 매개변수 결정
            if function.__name__ in ["check_func_1_5", "check_func_2_4","check_func_2_7"]:
                no, check_detail, check_result = function(win_conn)
            elif function.__name__ in ["check_func_2_5"]:
                no, check_detail, check_result = function(win_conn, mssql_conn)
            else:
                no, check_detail, check_result = function(mssql_conn)
            results.append({"no": no, "detail": check_detail.replace('\n', '\\n'), "result": check_result})
    except Exception as e:
        results.append({"error": f"전체 점검 실행 중 오류: {str(e)}"})
    finally:
        if mssql_conn:
            mssql_conn.close()

    return results
