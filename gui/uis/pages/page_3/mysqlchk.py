import mysql.connector
import paramiko

def perform_mysql_checks(ip_address, ssh_username, ssh_password, mysql_user, mysql_password, mysql_db):
    # MySQL 데이터베이스에 접속
    mysql_conn = mysql.connector.connect(host=ip_address, user=mysql_user, password=mysql_password, database=mysql_db)
    
    # SSH 연결 설정
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # SSH로 원격 서버에 연결 시도
        client.connect(ip_address, username=ssh_username, password=ssh_password)
    except Exception as e:
        return [{"error": f"SSH 접속 실패: {str(e)}"}]
    
    results = []

    try:
        # MySQL 점검 함수 임포트
        from .mysql_func.func_1_1 import check_func_1_1
        from .mysql_func.func_1_2 import check_func_1_2
        from .mysql_func.func_1_3 import check_func_1_3
        from .mysql_func.func_1_4 import check_func_1_4
        from .mysql_func.func_1_5 import check_func_1_5
        from .mysql_func.func_1_6 import check_func_1_6
        from .mysql_func.func_2_1 import check_func_2_1
        from .mysql_func.func_2_2 import check_func_2_2
        from .mysql_func.func_2_3 import check_func_2_3
        from .mysql_func.func_2_4 import check_func_2_4
        from .mysql_func.func_2_5 import check_func_2_5
        from .mysql_func.func_2_6 import check_func_2_6
        from .mysql_func.func_2_7 import check_func_2_7
        from .mysql_func.func_2_8 import check_func_2_8
        from .mysql_func.func_3_1 import check_func_3_1
        from .mysql_func.func_3_2 import check_func_3_2
        from .mysql_func.func_3_3 import check_func_3_3
        from .mysql_func.func_3_4 import check_func_3_4
        from .mysql_func.func_3_5 import check_func_3_5
        from .mysql_func.func_3_6 import check_func_3_6
        from .mysql_func.func_4_1 import check_func_4_1
        from .mysql_func.func_4_2 import check_func_4_2
        from .mysql_func.func_4_3 import check_func_4_3
        from .mysql_func.func_5_1 import check_func_5_1


        functions_to_check = [
            check_func_1_1, check_func_1_2, check_func_1_3, check_func_1_4, check_func_1_5,
            check_func_1_6, check_func_2_1, check_func_2_2, check_func_2_3, check_func_2_4,
            check_func_2_5, check_func_2_6, check_func_2_7, check_func_2_8, check_func_3_1,
            check_func_3_2, check_func_3_3, check_func_3_4, check_func_3_5, check_func_3_6,
            check_func_4_1, check_func_4_2, check_func_4_3, check_func_5_1
        ]

        for function in functions_to_check:
            try:
                # SSH를 사용하는 특정 함수에 대한 처리
                if function.__name__ in ["check_func_2_6","check_func_2_7","check_func_5_1"]:
                    no, check_detail, check_result = function(client)  # SSH 연결 사용
                else:
                    # MySQL 연결을 사용하는 함수에 대한 처리
                    no, check_detail, check_result = function(mysql_conn)
                results.append({"no": no, "detail": check_detail.replace('\n', '\\n'), "result": check_result})
            except Exception as e:
                results.append({"error": f"{function.__name__} 실행 중 오류: {str(e)}"})
    except Exception as e:
        results.append({"error": f"MySQL 접속 실패: {str(e)}"})
    finally:
        # MySQL 연결이 열려있으면 닫기
        if mysql_conn.is_connected():
            mysql_conn.close()
        # SSH 클라이언트 연결 닫기
        client.close()

    return results
