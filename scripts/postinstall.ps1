# log_file.ps1
$LogPath = "$env:APPDATA\csscan_install.log"
"Starting postinstall script" | Out-File -FilePath $LogPath

# 설치된 애플리케이션의 경로
$AppPath = "C:\Program Files (x86)\csscan\_internal\"
"Application Path: $AppPath" | Out-File -FilePath $LogPath -Append

# 사용자로부터 관리자 계정 정보를 입력 받음
Add-Type -AssemblyName Microsoft.VisualBasic
$adminUsername = [Microsoft.VisualBasic.Interaction]::InputBox("Enter Admin Username:", "User Input")
"Username: $adminUsername" | Out-File -FilePath $LogPath -Append

$adminPassword = [Microsoft.VisualBasic.Interaction]::InputBox("Enter Admin Password:", "User Input", "", -1, -1)
"Password entered" | Out-File -FilePath $LogPath -Append

# Standalone 실행 파일 경로
$exePath = "$AppPath\login\create_admin_account.exe"
"Executing: $exePath $adminUsername $adminPassword" | Out-File -FilePath $LogPath -Append
try {
    & $exePath $adminUsername $adminPassword >> $LogPath 2>&1
    "Postinstall script finished successfully" | Out-File -FilePath $LogPath -Append
} catch {
    "Error during postinstall: $_" | Out-File -FilePath $LogPath -Append
}
