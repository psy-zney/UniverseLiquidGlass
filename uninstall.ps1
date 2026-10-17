[CmdletBinding(SupportsShouldProcess)]
param([string]$ProfilePath)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'scripts\Profile.ps1')
$zenProfile = Resolve-ZenProfile $ProfilePath
Assert-ProfileClosed $zenProfile
$chrome = Join-Path $zenProfile 'chrome'
$managed = Join-Path $chrome 'UniverseLiquidGlass'
if (-not (Test-Path -LiteralPath (Join-Path $managed 'install-state.json'))) { throw 'Managed installation not found. See the manual uninstall instructions.' }
if (-not $PSCmdlet.ShouldProcess($zenProfile,'Remove Universe Liquid Glass imports and managed theme files')) { return }
foreach ($file in @('userChrome.css','userContent.css')) {
    $entry = Join-Path $chrome $file
    if (Test-Path -LiteralPath $entry) { Write-Utf8 $entry (Remove-ThemeImport (Read-OptionalText $entry)) }
}
$userJs = Join-Path $zenProfile 'user.js'
if (Test-Path -LiteralPath $userJs) {
    $text = [regex]::Replace((Read-OptionalText $userJs),'(?ms)^// BEGIN UniverseLiquidGlass\r?\n.*?^// END UniverseLiquidGlass\r?\n?','')
    Write-Utf8 $userJs $text
}
# Resolve and validate the fixed child folder before any recursive removal.
$resolved = (Resolve-Path -LiteralPath $managed).Path
$expected = [IO.Path]::GetFullPath((Join-Path $chrome 'UniverseLiquidGlass'))
if (-not $resolved.Equals($expected,[StringComparison]::OrdinalIgnoreCase)) { throw 'Unexpected theme directory. Refusing removal.' }
Remove-Item -LiteralPath $resolved -Recurse -Force
Write-Host 'Universe Liquid Glass removed. Other custom CSS and backups are preserved. Restart Zen.'
