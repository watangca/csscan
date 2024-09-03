import paramiko
import oracledb

def perform_oracle_checks(ip_address, ssh_username, ssh_password, oracle_username, oracle_password, oracle_dsn):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    results = []

    try:
        client.connect(ip_address, username=ssh_username, password=ssh_password)

        from .oracle_func.func_1_1 import check_func_1_1
        from .oracle_func.func_1_2 import check_func_1_2
        from .oracle_func.func_1_3 import check_func_1_3
        from .oracle_func.func_1_4 import check_func_1_4
        from .oracle_func.func_1_5 import check_func_1_5
        from .oracle_func.func_1_6 import check_func_1_6
        from .oracle_func.func_2_1 import check_func_2_1
        from .oracle_func.func_2_2 import check_func_2_2
        from .oracle_func.func_2_3 import check_func_2_3
        from .oracle_func.func_2_4 import check_func_2_4
        from .oracle_func.func_2_5 import check_func_2_5
        from .oracle_func.func_2_6 import check_func_2_6
        from .oracle_func.func_2_7 import check_func_2_7
        from .oracle_func.func_2_8 import check_func_2_8
        from .oracle_func.func_3_1 import check_func_3_1
        from .oracle_func.func_3_2 import check_func_3_2
        from .oracle_func.func_3_3 import check_func_3_3
        from .oracle_func.func_3_4 import check_func_3_4
        from .oracle_func.func_3_5 import check_func_3_5
        from .oracle_func.func_3_6 import check_func_3_6
        from .oracle_func.func_4_1 import check_func_4_1
        from .oracle_func.func_4_2 import check_func_4_2
        from .oracle_func.func_4_3 import check_func_4_3
        from .oracle_func.func_5_1 import check_func_5_1

        functions_to_check = [
            check_func_1_1, check_func_1_2, check_func_1_3, check_func_1_4, check_func_1_5,
            check_func_1_6, check_func_2_1, check_func_2_2, check_func_2_3, check_func_2_4,
            check_func_2_5, check_func_2_6, check_func_2_7, check_func_2_8, check_func_3_1,
            check_func_3_2, check_func_3_3, check_func_3_4, check_func_3_5, check_func_3_6,
            check_func_4_1, check_func_4_2, check_func_4_3, check_func_5_1
        ]

        with oracledb.connect(user=oracle_username, password=oracle_password, dsn=oracle_dsn) as oracle_conn:
            for function in functions_to_check:
                try:
                    if function.__name__ in [
                        "check_func_2_3", "check_func_2_6", "check_func_2_7", "check_func_2_8",
                        "check_func_4_3"]:
                        no, check_detail, check_result = function(client)
                    else:
                        no, check_detail, check_result = function(oracle_conn)
                    
                    # Replace may not work if check_detail is not a string, adding condition
                    if isinstance(check_detail, str):
                        check_detail_processed = check_detail.replace('\n', '\\n')
                    else:
                        check_detail_processed = str(check_detail)
                    
                    results.append({"no": no, "detail": check_detail_processed, "result": check_result})
                except Exception as e:
                    results.append({"error": f"{function.__name__} 실행 중 오류: {str(e)}"})

    except Exception as e:
        results.append({"error": f"SSH/Oracle 접속 실패: {str(e)}"})
    finally:
        client.close()

    return results
