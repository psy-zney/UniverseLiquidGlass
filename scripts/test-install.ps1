$ErrorActionPreference='Stop'
$repo=Split-Path $PSScriptRoot
$fixture=Join-Path ([IO.Path]::GetTempPath()) ('UniverseLiquidGlass-test-'+[Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path (Join-Path $fixture 'chrome') -Force | Out-Null
$utf8=[Text.UTF8Encoding]::new($false)
$chromeFile=Join-Path $fixture 'chrome\userChrome.css'
$contentFile=Join-Path $fixture 'chrome\userContent.css'
$prefFile=Join-Path $fixture 'user.js'
$original='@charset "UTF-8";' + "`r`n" + '/* Existing custom theme */' + "`r`n" + ':root { --my-color: red; }'
[IO.File]::WriteAllText($chromeFile,$original,$utf8)
[IO.File]::WriteAllText($contentFile,'/* Existing content rules */',$utf8)
[IO.File]::WriteAllText($prefFile,'user_pref("browser.startup.page", 0);',$utf8)
& (Join-Path $repo 'install.ps1') -ProfilePath $fixture -WhatIf
if (Test-Path -LiteralPath (Join-Path $fixture 'chrome\UniverseLiquidGlass')) { throw 'WhatIf modified the profile' }
& (Join-Path $repo 'install.ps1') -ProfilePath $fixture
& (Join-Path $repo 'install.ps1') -ProfilePath $fixture
$installed=[IO.File]::ReadAllText($chromeFile)
if (($installed.Split([string[]]@('/* UniverseLiquidGlass */'),[StringSplitOptions]::None).Length-1) -ne 1) { throw 'Duplicate import after repeated install' }
if (-not $installed.StartsWith('@charset "UTF-8";')) { throw 'CSS charset moved' }
if (-not $installed.Contains(':root { --my-color: red; }')) { throw 'Custom CSS lost' }
if (-not [IO.File]::ReadAllText($prefFile).Contains('browser.startup.page')) { throw 'Existing preferences lost' }
if (@(Get-ChildItem -LiteralPath (Join-Path $fixture '.universe-liquid-glass-backups') -Directory).Count -ne 2) { throw 'Missing backups' }
$wallpaperSample=Join-Path $fixture 'sample-wallpaper.png'
[IO.File]::WriteAllBytes($wallpaperSample,[Convert]::FromBase64String('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jG8EAAAAASUVORK5CYII='))
1..2 | ForEach-Object { & (Join-Path $PSScriptRoot 'use-desktop-wallpaper.ps1') -ProfilePath $fixture -WallpaperPath $wallpaperSample }
$wallpaperCss=[IO.File]::ReadAllText((Join-Path $fixture 'chrome\UniverseLiquidGlass\wallpaper.css'))
if (-not $wallpaperCss.Contains('data:image/png;base64,') -or -not $wallpaperCss.Contains('@-moz-document') -or $wallpaperCss.Contains('url-prefix("http')) { throw 'Local wallpaper data scope failed' }
if (([regex]::Matches([IO.File]::ReadAllText($chromeFile),'UniverseLiquidGlass wallpaper')).Count -ne 1) { throw 'Duplicate wallpaper import' }
$later="`r`n/* Added after installation */"
[IO.File]::AppendAllText($chromeFile,$later,$utf8)
& (Join-Path $repo 'uninstall.ps1') -ProfilePath $fixture
$restored=[IO.File]::ReadAllText($chromeFile)
if ($restored -ne ($original+$later)) { throw 'Uninstall did not preserve custom CSS exactly' }
if ([IO.File]::ReadAllText($prefFile).Contains('BEGIN UniverseLiquidGlass')) { throw 'Managed preference block remains' }
if (Test-Path -LiteralPath (Join-Path $fixture 'chrome\UniverseLiquidGlass')) { throw 'Theme folder remains' }
$lock=[IO.File]::Open((Join-Path $fixture 'parent.lock'),'Create','ReadWrite','None')
try {
    $rejected=$false
    try { & (Join-Path $repo 'install.ps1') -ProfilePath $fixture } catch { $rejected=$_.Exception.Message.Contains('running or locked') }
    if (-not $rejected) { throw 'Locked profile was not rejected' }
} finally { $lock.Dispose() }
Write-Host 'PASS: WhatIf, repeated install, CSS import order, backups, local wallpaper, uninstall preservation, profile lock.'
Write-Host ('Test profile retained for inspection: '+$fixture)
