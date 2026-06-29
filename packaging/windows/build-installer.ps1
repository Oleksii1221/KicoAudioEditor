param(
    [string]$Version = "0.1.0"
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path "$PSScriptRoot\..\.."
Set-Location $root

$python = Join-Path $root ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    python -m venv .venv
}
$python = Join-Path $root ".venv\Scripts\python.exe"

$env:KAE_VERSION = $Version
& $python -m pip install -e ".[dev]"
& $python -m PyInstaller packaging\kae.spec --noconfirm

$iscc = Get-Command iscc -ErrorAction SilentlyContinue
$isccPath = if ($iscc) { $iscc.Source } else { $null }
if (-not $isccPath) {
    $candidates = @(
        "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe",
        "$env:ProgramFiles\Inno Setup 6\ISCC.exe",
        "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe"
    )
    $isccPath = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
}

if (-not $isccPath) {
    throw "Inno Setup Compiler (iscc) is required to build KAE-Setup-$Version.exe."
}

& $isccPath packaging\windows\KAE.iss
