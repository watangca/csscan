import os

def check_func_2_1(client):
    no = "2_1"
    check_detail = ""
    check_result = "N/A"
    
    try:
        # PATH 환경변수 값을 가져옴
        path_value = os.environ.get("PATH")
        if path_value:
            check_detail = f"echo $PATH 결과: {path_value}"
            
            # PATH 값에서 . (현재 디렉터리) 위치 확인
            paths = path_value.split(":")
            if "." in paths and paths.index(".") != len(paths) - 1:
                check_result = "취약"
            else:
                check_result = "양호"
        else:
            check_detail = "PATH 환경 변수가 설정되어 있지 않음."
            check_result = "N/A"
    
    except Exception as e:
        check_detail = f"오류 발생: {e}"
        check_result = "N/A"
    
    return no, check_detail, check_result