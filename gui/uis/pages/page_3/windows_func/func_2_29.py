def check_func_2_29(client):
    no = "2_29"
    check_detail = "SNMP 커뮤니티 이름: "
    check_result = "n/a"

    try:
        # SNMP 커뮤니티 이름 조회
        community_command = "Get-ItemProperty 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\SNMP\\Parameters\\ValidCommunities'"
        community_response = client.run_ps(community_command)

        if community_response.status_code == 0 and community_response.std_out:
            # 결과를 바이트에서 문자열로 변환
            output = community_response.std_out.decode('utf-8') if isinstance(community_response.std_out, bytes) else community_response.std_out
            lines = output.strip().split('\r\n')
            communities = []
            for line in lines:
                if ":" in line and not line.startswith("PS"):
                    community_name = line.split(':')[0].strip()
                    communities.append(community_name)
            check_detail += ', '.join(communities)

            # 양호 및 취약 여부 판단
            if any(comm.lower() in ['public', 'private'] for comm in communities):
                check_result = "취약"
            else:
                check_result = "양호"
        else:
            # SNMP 서비스가 없거나 비활성화된 경우
            check_result = "양호"
            check_detail += "서비스 비활성화 또는 미설치"

    except Exception as e:
        check_detail += str(e)

    return no, check_detail, check_result
