import json

def check_func_2_6(client):
    no = "2_6"
    check_detail = "IIS CGI 실행 제한 설정 상세: "
    check_result = "n/a"

    # IIS CGI 실행 제한 설정을 확인하는 PowerShell 명령어
    ps_command = """
    $cgiRestrictions = Get-WebConfiguration -Filter '/system.webServer/security/isapiCgiRestriction' -PSPath 'MACHINE/WEBROOT/APPHOST'
    $restrictedCgi = $cgiRestrictions.Collection | Where-Object { $_.allowed -eq $false } | Select-Object path, allowed
    $isRestricted = $restrictedCgi.Count -gt 0
    $result = @{
        'CGIRestricted' = $isRestricted
        'RestrictedCGIDetails' = $restrictedCgi | ConvertTo-Json
    }
    $result | ConvertTo-Json
    """

    # 원격 서버에서 PowerShell 명령어 실행
    response = client.run_ps(ps_command)

    if response.status_code == 0 and response.std_out:
        output = response.std_out.decode().strip()
        data = json.loads(output)

        if data['RestrictedCGIDetails']:
            restrictedCgiDetails = json.loads(data['RestrictedCGIDetails'])
            detailsFormatted = json.dumps(restrictedCgiDetails, indent=4, ensure_ascii=False)
            check_detail += f"제한된 CGI 목록: {detailsFormatted}"
        else:
            check_detail += "제한된 CGI 스크립트 없음(CGIRestricted: False)"

        if data['CGIRestricted']:
            check_result = "양호"
        else:
            check_result = "취약"
    else:
        check_detail += " - 오류 발생: " + response.std_err.decode()
        check_result = "n/a"

    return no, check_detail, check_result
