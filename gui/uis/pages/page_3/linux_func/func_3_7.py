def check_func_3_7(client):
    no = "3_7"
    check_result = "n/a"  # 기본값 설정
    check_detail = "점검 결과:\n"

    # /etc/exports 파일 내용 읽기
    stdin, stdout, stderr = client.exec_command('cat /etc/exports')
    exports_content = stdout.read().decode()

    if not exports_content.strip():
        # /etc/exports 파일이 비어 있거나 존재하지 않는 경우
        check_detail += "NFS 설정 파일(/etc/exports)이 비어 있거나 존재하지 않음"
        check_result = "n/a"
    else:
        # everyone 공유를 제한하지 않거나 no_root_squash 옵션을 사용하는 경우를 찾습니다.
        potentially_unsafe_exports = [line for line in exports_content.split('\n') if "*" in line or "no_root_squash" in line]
        
        if potentially_unsafe_exports:
            # 제한 없이 모든 사용자에게 접근을 허용하거나, no_root_squash 옵션을 사용하는 경우
            check_result = "취약"
            check_detail += "위험한 NFS 공유 설정이 발견됨:\n" + "\n".join(potentially_unsafe_exports)
        else:
            # 위험 요소가 발견되지 않는 경우
            check_result = "양호"
            check_detail += "모든 NFS 공유 설정이 안전하게 적용되어 있거나, NFS 공유가 사용되지 않음."

    return no, check_detail, check_result
