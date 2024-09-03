def check_func_1_4(client):
    no = "1_4"
    check_detail = ""
    check_result = "N/A"
    
    try:
        with open("/etc/passwd", "r") as f:
            lines = f.readlines()
            
            vulnerable_accounts = []
            for line in lines:
                parts = line.strip().split(":")
                if len(parts) > 1 and not parts[1] in ['x', '*', '!']:
                    vulnerable_accounts.append(parts[0])
            
            if vulnerable_accounts:
                check_detail = "취약한 계정들: " + ", ".join(vulnerable_accounts)
                check_result = "취약"
            else:
                check_detail = "모든 계정의 패스워드가 암호화됨"
                check_result = "양호"
    
    except FileNotFoundError:
        check_detail = "/etc/passwd 파일을 찾을 수 없음"
        check_result = "N/A"
    
    return no, check_detail, check_result