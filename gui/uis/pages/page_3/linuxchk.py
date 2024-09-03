import paramiko
import concurrent.futures

def perform_linux_checks(ip_address, username, password):
    session = paramiko.SSHClient()
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    results = []

    try:
        session.connect(ip_address, username=username, password=password)

        from .linux_func.func_1_1 import check_func_1_1
        from .linux_func.func_1_2 import check_func_1_2
        from .linux_func.func_1_3 import check_func_1_3
        from .linux_func.func_1_4 import check_func_1_4
        from .linux_func.func_1_5 import check_func_1_5
        from .linux_func.func_1_6 import check_func_1_6
        from .linux_func.func_1_7 import check_func_1_7
        from .linux_func.func_1_8 import check_func_1_8
        from .linux_func.func_1_9 import check_func_1_9
        from .linux_func.func_1_10 import check_func_1_10
        from .linux_func.func_1_11 import check_func_1_11
        from .linux_func.func_1_12 import check_func_1_12
        from .linux_func.func_1_13 import check_func_1_13
        from .linux_func.func_1_14 import check_func_1_14
        from .linux_func.func_1_15 import check_func_1_15
        from .linux_func.func_2_1 import check_func_2_1
        from .linux_func.func_2_2 import check_func_2_2
        from .linux_func.func_2_3 import check_func_2_3
        from .linux_func.func_2_4 import check_func_2_4
        from .linux_func.func_2_5 import check_func_2_5
        from .linux_func.func_2_6 import check_func_2_6
        from .linux_func.func_2_7 import check_func_2_7
        from .linux_func.func_2_8 import check_func_2_8
        from .linux_func.func_2_9 import check_func_2_9
        from .linux_func.func_2_10 import check_func_2_10
        from .linux_func.func_2_11 import check_func_2_11
        from .linux_func.func_2_12 import check_func_2_12
        from .linux_func.func_2_13 import check_func_2_13
        from .linux_func.func_2_14 import check_func_2_14
        from .linux_func.func_2_15 import check_func_2_15
        from .linux_func.func_2_16 import check_func_2_16
        from .linux_func.func_2_17 import check_func_2_17
        from .linux_func.func_2_18 import check_func_2_18
        from .linux_func.func_2_19 import check_func_2_19
        from .linux_func.func_3_1 import check_func_3_1
        from .linux_func.func_3_2 import check_func_3_2
        from .linux_func.func_3_3 import check_func_3_3
        from .linux_func.func_3_4 import check_func_3_4
        from .linux_func.func_3_5 import check_func_3_5
        from .linux_func.func_3_6 import check_func_3_6
        from .linux_func.func_3_7 import check_func_3_7
        from .linux_func.func_3_8 import check_func_3_8
        from .linux_func.func_3_9 import check_func_3_9
        from .linux_func.func_3_10 import check_func_3_10
        from .linux_func.func_3_11 import check_func_3_11
        from .linux_func.func_3_12 import check_func_3_12
        from .linux_func.func_3_13 import check_func_3_13
        from .linux_func.func_3_14 import check_func_3_14
        from .linux_func.func_3_15 import check_func_3_15
        from .linux_func.func_3_16 import check_func_3_16
        from .linux_func.func_3_17 import check_func_3_17
        from .linux_func.func_3_18 import check_func_3_18
        from .linux_func.func_3_19 import check_func_3_19
        from .linux_func.func_3_20 import check_func_3_20
        from .linux_func.func_3_21 import check_func_3_21
        from .linux_func.func_3_22 import check_func_3_22
        from .linux_func.func_3_23 import check_func_3_23
        from .linux_func.func_3_24 import check_func_3_24
        from .linux_func.func_3_25 import check_func_3_25
        from .linux_func.func_3_26 import check_func_3_26
        from .linux_func.func_3_27 import check_func_3_27
        from .linux_func.func_3_28 import check_func_3_28
        from .linux_func.func_3_29 import check_func_3_29
        from .linux_func.func_3_30 import check_func_3_30
        from .linux_func.func_3_31 import check_func_3_31
        from .linux_func.func_3_32 import check_func_3_32
        from .linux_func.func_3_33 import check_func_3_33
        from .linux_func.func_3_34 import check_func_3_34
        from .linux_func.func_3_35 import check_func_3_35
        from .linux_func.func_4_1 import check_func_4_1
        from .linux_func.func_5_1 import check_func_5_1
        from .linux_func.func_5_2 import check_func_5_2

        functions_to_check = [
            check_func_1_1, check_func_1_2, check_func_1_3, check_func_1_4, check_func_1_5,
            check_func_1_6, check_func_1_7, check_func_1_8, check_func_1_9, check_func_1_10,
            check_func_1_11, check_func_1_12, check_func_1_13, check_func_1_14, check_func_1_15,
            check_func_2_1, check_func_2_2, check_func_2_3, check_func_2_4, check_func_2_5, 
            check_func_2_6, check_func_2_7, check_func_2_8, check_func_2_9, check_func_2_10,
            check_func_2_11, check_func_2_12, check_func_2_13,check_func_2_14, check_func_2_15,
            check_func_2_16, check_func_2_17, check_func_2_18, check_func_2_19, check_func_3_1,
            check_func_3_2, check_func_3_3, check_func_3_4, check_func_3_5, check_func_3_6,
            check_func_3_7, check_func_3_8, check_func_3_9, check_func_3_10, check_func_3_11,
            check_func_3_12, check_func_3_13, check_func_3_14, check_func_3_15, check_func_3_16,
            check_func_3_17, check_func_3_18, check_func_3_19, check_func_3_20, check_func_3_21,
            check_func_3_22, check_func_3_23, check_func_3_24, check_func_3_25, check_func_3_26,
            check_func_3_27, check_func_3_28, check_func_3_29, check_func_3_30, check_func_3_31,
            check_func_3_32, check_func_3_33, check_func_3_34, check_func_3_35, check_func_4_1,
            check_func_5_1, check_func_5_2
        ]

        def execute_check(func):
            try:
                return func(session)
            except Exception as e:
                # 예외 발생 시 오류 메시지를 포함한 튜플 반환
                return None, None, f"Error executing {func.__name__}: {e}"

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(execute_check, func): func for func in functions_to_check}
            for future in concurrent.futures.as_completed(futures):
                try:
                    no, check_detail, check_result = future.result()
                    # 결과가 유효한 경우에만 리스트에 추가
                    if no is not None and check_detail is not None and check_result is not None:
                        results.append({"no": no, "detail": check_detail, "result": check_result})
                    else:
                        # 여기서 오류 처리
                        print(f'Error in executing a function, received: {future.result()}')
                except Exception as exc:
                    print(f'A function execution generated an exception: {exc}')

    except Exception as e:
        results.append({"error": f"SSH connection failed: {e}"})
    finally:
        session.close()

    return results
