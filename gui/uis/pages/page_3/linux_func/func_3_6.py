def check_func_3_6(client):
    no = "3_6"
    check_result = "n/a"  # 기본값 설정
    check_detail = ""

    # NFS 관련 프로세스 확인 명령어
    ps_cmd = "ps -ef | egrep '/nfsd|/rpc.statd|/rpc.lockd' | grep -v grep"
    stdin, stdout, stderr = client.exec_command(ps_cmd)
    output = stdout.read().decode().strip()

    # 실제 NFS 관련 데몬이 실행 중인지 확인하기 위한 검사
    if output:
        # 실행 중인 데몬 정보를 상세 내용에 추가
        check_detail = "활성화된 NFS 데몬:\n" + output
        check_result = "취약"
    else:
        check_detail = "활성화된 NFS 데몬 없음"
        check_result = "양호"

    return no, check_detail, check_result
