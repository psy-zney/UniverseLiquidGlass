[CmdletBinding()]
param([string]$Python='python',[string]$Zen='C:\Program Files\Zen Browser\zen.exe')
$ErrorActionPreference='Stop'
$renders=Join-Path (Split-Path $PSScriptRoot) 'renders'
$captureProfile=Join-Path $renders ('zen-profile-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $captureProfile -Force | Out-Null
$prefs=@'
user_pref("marionette.port", 2839);
user_pref("marionette.enabled", true);
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("browser.startup.homepage", "about:blank");
user_pref("browser.startup.page", 0);
user_pref("browser.aboutwelcome.enabled", false);
user_pref("browser.tabs.warnOnClose", false);
user_pref("zen.welcome-screen.seen", true);
user_pref("zen.welcome-screen.version", "999");
user_pref("zen.view.sidebar-expanded", true);
user_pref("zen.workspaces.enabled", true);
user_pref("datareporting.policy.dataSubmissionPolicyBypassNotification", true);
user_pref("browser.sessionstore.resume_from_crash", false);
'@
[IO.File]::WriteAllText((Join-Path $captureProfile 'user.js'),$prefs,[Text.UTF8Encoding]::new($false))
try {
    Start-Process -FilePath $Zen -ArgumentList @('-no-remote','-profile',('"'+$captureProfile+'"'),'--headless','--marionette','--remote-allow-system-access','about:blank') -WindowStyle Hidden -RedirectStandardOutput (Join-Path $renders 'zen-stdout.log') -RedirectStandardError (Join-Path $renders 'zen-stderr.log') | Out-Null
    Start-Sleep -Seconds 3
    & $Python (Join-Path $PSScriptRoot 'render.py') --profile $captureProfile
    if ($LASTEXITCODE -ne 0) { throw 'Video capture failed.' }
} finally {
    # Only this launcher-created, unique headless profile may be stopped.
    $matchesProfile=@(Get-CimInstance Win32_Process -Filter "Name='zen.exe'" | Where-Object {
        $_.CommandLine -and $_.CommandLine.Contains($captureProfile) -and $_.CommandLine.Contains('--headless') -and $_.CommandLine.Contains('-no-remote')
    })
    foreach ($captureProcess in $matchesProfile) { Stop-Process -Id $captureProcess.ProcessId -ErrorAction SilentlyContinue }
}
