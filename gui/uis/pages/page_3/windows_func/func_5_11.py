import json

def check_func_5_11(client):
    no = "5_11"
    registry_path = "HKLM\\System\\CurrentControlSet\\Services\\Tcpip\\Parameters"
    check_detail = "DoS 공격 방어 레지스트리 설정 확인: "

    # 원격 시스템에서 DoS 방어 레지스트리 설정 확인을 위한 PowerShell 명령어
    policy_command = f"""
    $registryPath = '{registry_path}'
    $keys = @('SynAttackProtect', 'EnableDeadGWDetect', 'KeepAliveTime', 'NoNameReleaseOnDemand')
    $values = @{{}}
    foreach ($key in $keys) {{
        try {{
            $value = (Get-ItemProperty -Path Registry::$registryPath -Name $key -ErrorAction SilentlyContinue).$key
            $values[$key] = if ($null -eq $value) {{ 'Not Set' }} else {{ $value }}
        }} catch {{
            $values[$key] = 'Not Set'
        }}
    }}
    ConvertTo-Json $values
    """

    try:
        policy_response = client.run_ps(policy_command)

        if policy_response.status_code == 0:
            values = json.loads(policy_response.std_out.decode('utf-8').strip())
            check_detail += str(values)

            # DoS 방어 설정 검사
            syn_attack_protect = values.get('SynAttackProtect', 'Not Set')
            enable_dead_gw_detect = values.get('EnableDeadGWDetect', 'Not Set')
            keep_alive_time = values.get('KeepAliveTime', 'Not Set')
            no_name_release_on_demand = values.get('NoNameReleaseOnDemand', 'Not Set')

            if (syn_attack_protect != 'Not Set' and syn_attack_protect is not None and int(syn_attack_protect) >= 1 and
                enable_dead_gw_detect != 'Not Set' and enable_dead_gw_detect is not None and int(enable_dead_gw_detect) == 0 and
                keep_alive_time != 'Not Set' and keep_alive_time is not None and int(keep_alive_time) <= 300000 and
                no_name_release_on_demand != 'Not Set' and no_name_release_on_demand is not None and int(no_name_release_on_demand) == 1):
                check_result = "양호"
            else:
                check_result = "취약"
        else:
            check_detail += f"명령 실행 오류: {policy_response.std_err.decode('utf-8')}"
            check_result = "취약"

    except Exception as e:
        check_detail += f"\nException: {str(e)}"
        check_result = "취약"

    return no, check_detail, check_result
