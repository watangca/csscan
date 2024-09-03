import winrm
import logging

# 로깅 설정
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def perform_windows_checks(ip_address, username, password):
    session = winrm.Session(ip_address, auth=(username, password), transport='ntlm')
    results = []

    try:
        # 각 점검 함수 실행
        from .windows_func.func_1_1 import check_func_1_1
        from .windows_func.func_1_2 import check_func_1_2
        from .windows_func.func_1_3 import check_func_1_3
        from .windows_func.func_1_4 import check_func_1_4
        from .windows_func.func_1_5 import check_func_1_5
        from .windows_func.func_1_6 import check_func_1_6
        from .windows_func.func_1_7 import check_func_1_7
        from .windows_func.func_1_8 import check_func_1_8
        from .windows_func.func_1_9 import check_func_1_9
        from .windows_func.func_1_10 import check_func_1_10
        from .windows_func.func_1_11 import check_func_1_11
        from .windows_func.func_1_12 import check_func_1_12
        from .windows_func.func_1_13 import check_func_1_13
        from .windows_func.func_1_14 import check_func_1_14
        from .windows_func.func_1_15 import check_func_1_15
        from .windows_func.func_1_16 import check_func_1_16
        from .windows_func.func_1_17 import check_func_1_17
        from .windows_func.func_1_18 import check_func_1_18
        from .windows_func.func_2_1 import check_func_2_1
        from .windows_func.func_2_2 import check_func_2_2
        from .windows_func.func_2_3 import check_func_2_3
        from .windows_func.func_2_4 import check_func_2_4
        from .windows_func.func_2_5 import check_func_2_5
        from .windows_func.func_2_6 import check_func_2_6
        from .windows_func.func_2_7 import check_func_2_7
        from .windows_func.func_2_8 import check_func_2_8
        from .windows_func.func_2_9 import check_func_2_9
        from .windows_func.func_2_10 import check_func_2_10
        from .windows_func.func_2_11 import check_func_2_11
        from .windows_func.func_2_12 import check_func_2_12
        from .windows_func.func_2_13 import check_func_2_13
        from .windows_func.func_2_14 import check_func_2_14
        from .windows_func.func_2_15 import check_func_2_15
        from .windows_func.func_2_16 import check_func_2_16
        from .windows_func.func_2_17 import check_func_2_17
        from .windows_func.func_2_18 import check_func_2_18
        from .windows_func.func_2_19 import check_func_2_19
        from .windows_func.func_2_20 import check_func_2_20
        from .windows_func.func_2_21 import check_func_2_21
        from .windows_func.func_2_22 import check_func_2_22
        from .windows_func.func_2_23 import check_func_2_23
        from .windows_func.func_2_24 import check_func_2_24
        from .windows_func.func_2_25 import check_func_2_25
        from .windows_func.func_2_26 import check_func_2_26
        from .windows_func.func_2_27 import check_func_2_27
        from .windows_func.func_2_28 import check_func_2_28
        from .windows_func.func_2_29 import check_func_2_29
        from .windows_func.func_2_30 import check_func_2_30
        from .windows_func.func_2_31 import check_func_2_31
        from .windows_func.func_2_32 import check_func_2_32
        from .windows_func.func_2_33 import check_func_2_33
        from .windows_func.func_2_34 import check_func_2_34
        from .windows_func.func_2_35 import check_func_2_35
        from .windows_func.func_2_36 import check_func_2_36
        from .windows_func.func_3_1 import check_func_3_1
        from .windows_func.func_3_2 import check_func_3_2
        from .windows_func.func_3_3 import check_func_3_3
        from .windows_func.func_4_1 import check_func_4_1
        from .windows_func.func_4_2 import check_func_4_2
        from .windows_func.func_4_3 import check_func_4_3
        from .windows_func.func_4_4 import check_func_4_4
        from .windows_func.func_5_1 import check_func_5_1
        from .windows_func.func_5_2 import check_func_5_2
        from .windows_func.func_5_3 import check_func_5_3
        from .windows_func.func_5_4 import check_func_5_4
        from .windows_func.func_5_5 import check_func_5_5
        from .windows_func.func_5_6 import check_func_5_6
        from .windows_func.func_5_7 import check_func_5_7
        from .windows_func.func_5_8 import check_func_5_8
        from .windows_func.func_5_9 import check_func_5_9
        from .windows_func.func_5_10 import check_func_5_10
        from .windows_func.func_5_11 import check_func_5_11
        from .windows_func.func_5_12 import check_func_5_12
        from .windows_func.func_5_13 import check_func_5_13
        from .windows_func.func_5_14 import check_func_5_14
        from .windows_func.func_5_15 import check_func_5_15
        from .windows_func.func_5_16 import check_func_5_16
        from .windows_func.func_5_17 import check_func_5_17
        from .windows_func.func_5_18 import check_func_5_18
        from .windows_func.func_5_19 import check_func_5_19
        from .windows_func.func_5_20 import check_func_5_20
        from .windows_func.func_6_1 import check_func_6_1

        functions_to_check = [
        check_func_1_1, check_func_1_2, check_func_1_3, check_func_1_4, check_func_1_5, check_func_1_6,
        check_func_1_7, check_func_1_8, check_func_1_9, check_func_1_10, check_func_1_11, check_func_1_12,
        check_func_1_13, check_func_1_14, check_func_1_15,check_func_1_16, check_func_1_17, check_func_1_18,
        check_func_2_1, check_func_2_2, check_func_2_3, check_func_2_4, check_func_2_5, check_func_2_6,
        check_func_2_7, check_func_2_8, check_func_2_9, check_func_2_10, check_func_2_11, check_func_2_12,
        check_func_2_13, check_func_2_14, check_func_2_15, check_func_2_16, check_func_2_17, check_func_2_18,
        check_func_2_19, check_func_2_20, check_func_2_21, check_func_2_22, check_func_2_23, check_func_2_24,
        check_func_2_25, check_func_2_26, check_func_2_27, check_func_2_28, check_func_2_29,check_func_2_30,
        check_func_2_31, check_func_2_32, check_func_2_33, check_func_2_34, check_func_2_35, check_func_2_36,
        check_func_3_1, check_func_3_2, check_func_3_3, check_func_4_1, check_func_4_2, check_func_4_3,
        check_func_4_4, check_func_5_1, check_func_5_2, check_func_5_3, check_func_5_4, check_func_5_5,
        check_func_5_6, check_func_5_7, check_func_5_8, check_func_5_9, check_func_5_10, check_func_5_11,
        check_func_5_12, check_func_5_13, check_func_5_14, check_func_5_15, check_func_5_16, check_func_5_17,
        check_func_5_18, check_func_5_19, check_func_5_20, check_func_6_1
        ]

        for function in functions_to_check:
            try:
                logging.debug(f"Executing {function.__name__}")
                no, check_detail, check_result = function(session)
                if not isinstance(check_result, str) or not isinstance(no, str) or not isinstance(check_detail, str):
                    logging.error(f"{function.__name__} returned an unexpected value: no={no}, detail={check_detail}, result={check_result}")
                    continue  # 유효하지 않은 반환 값에 대해 다음 함수로 넘어갑니다.

                check_detail_processed = check_detail.replace('\n', '\\n')
                results.append({"no": no, "detail": check_detail_processed, "result": check_result})
                logging.debug(f"{function.__name__} executed successfully with result: {check_result}")
            except Exception as e:
                logging.error(f"Error in function {function.__name__}: {e}", exc_info=True)
                results.append({"error": f"{function.__name__} 실행 중 오류: {str(e)}"})

    except Exception as e:
        logging.error(f"WinRM 접속 실패: {e}", exc_info=True)
        results.append({"error": f"WinRM 접속 실패: {str(e)}"})

    return results
