Set-StrictMode -Version Latest

function Resolve-ZenProfile {
    param([string]$ProfilePath)
    if ($ProfilePath) {
        $item = Get-Item -LiteralPath $ProfilePath -ErrorAction Stop
        if (-not $item.PSIsContainer) { throw 'ProfilePath must be a profile folder.' }
        return $item.FullName
    }
    $config = Join-Path $env:APPDATA 'zen\profiles.ini'
    if (-not (Test-Path -LiteralPath $config)) { throw 'Zen profiles.ini not found. Pass -ProfilePath from about:profiles.' }
    $profiles = @(); $section = $null
    foreach ($line in [IO.File]::ReadAllLines($config)) {
        if ($line -match '^\[([^\]]+)\]') {
            if ($section -and $section.ContainsKey('Path')) { $profiles += ,$section }
            $section = if ($Matches[1] -match '^Profile\d+$') { @{} } else { $null }
        } elseif ($null -ne $section -and $line -match '^([^=]+)=(.*)$') { $section[$Matches[1]] = $Matches[2] }
    }
    if ($section -and $section.ContainsKey('Path')) { $profiles += ,$section }
    if ($profiles.Count -ne 1) { throw 'Multiple Zen profiles found. Pass -ProfilePath with the intended Root Directory from about:profiles.' }
    $zenProfile = $profiles[0]
    $candidate = if ($zenProfile['IsRelative'] -eq '1') { Join-Path (Split-Path $config) $zenProfile['Path'] } else { $zenProfile['Path'] }
    return (Get-Item -LiteralPath $candidate -ErrorAction Stop).FullName
}

function Assert-ProfileClosed {
    param([string]$ProfilePath)
    foreach ($filename in @('parent.lock','.parentlock')) {
        $lock = Join-Path $ProfilePath $filename
        if (Test-Path -LiteralPath $lock) {
            try { $stream = [IO.File]::Open($lock,'Open','ReadWrite','None'); $stream.Dispose() }
            catch { throw 'This Zen profile is running or locked. Close Zen completely before installing or removing the theme.' }
        }
    }
}

function Read-OptionalText {
    param([string]$Path)
    if (Test-Path -LiteralPath $Path) { return [IO.File]::ReadAllText($Path) }
    return ''
}

function Write-Utf8 {
    param([string]$Path,[AllowEmptyString()][string]$Text)
    [IO.File]::WriteAllText($Path,$Text,[Text.UTF8Encoding]::new($false))
}

function Remove-ThemeImport {
    param([string]$Text)
    return [regex]::Replace($Text,'(?m)^[ \t]*@import url\("UniverseLiquidGlass/(?:userChrome|userContent|wallpaper)\.css"\); /\* UniverseLiquidGlass(?: wallpaper)? \*/\r?\n?','')
}
