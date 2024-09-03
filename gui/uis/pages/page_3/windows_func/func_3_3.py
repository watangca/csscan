def check_func_3_3(client):
    no = "3_3"
    audit_policy_cmd = 'auditpol /get /category:*'
    result = client.run_ps(audit_policy_cmd)

    # Initialize audit policy settings string
    check_detail = "Audit Policy Settings:\n"
    check_result = "n/a"  # Default value

    if result.status_code == 0 and result.std_out:
        result_text = result.std_out.decode('utf-8').strip()
        if not result_text:
            check_detail += "Unable to retrieve audit policy settings.\n"
            return no, check_detail, check_result

        required_policies = {
            "Account Management": "Account Management Audit: Success",
            "Logon/Logoff\\Logon": "Account Logon Events Audit: Success",
            "Logon/Logoff\\Logoff": "Logoff Events Audit: Success",
            "Object Access\\Directory Service Access": "Directory Service Access Audit: Success",
            "System\\Security State Change": "System Events Audit: Success",
            "Policy Change": "Policy Change Audit: Success",
        }

        policy_settings = {}
        for line in result_text.split('\n'):
            if ": " in line:
                policy, setting = line.split(": ", 1)
                policy_settings[policy.strip()] = setting.strip()

        check_result = "Compliant"
        for policy, description in required_policies.items():
            current_setting = policy_settings.get(policy, None)
            if current_setting and "Success" in current_setting:
                check_detail += f"{description}\n"
            else:
                check_result = "Non-Compliant"
                # Adjust the description to show not configured
                check_detail += f"{description.replace('Success', 'Success: Not Configured')}\n"

    else:
        error_output = result.std_err.decode('utf-8').strip() if result.std_err else "Failed to retrieve audit policy"
        check_detail += f"Error: {error_output}\n"

    return no, check_detail, check_result
