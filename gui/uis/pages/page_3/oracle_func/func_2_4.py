def check_func_2_4(client):
    no = "2_4"
    check_detail = "ORACLE DBMS에서 ODBC/OLE-DB를 사용하지 않음, N/A 처리"
    check_result = "n/a"  # Oracle DBMS는 Windows OS의 ODBC/OLE-DB 점검 대상이 아님
    
    return no, check_detail, check_result