# Reproduction script for act-based verification — 2026-05-24
# Run from the repository root: C:\Users\devic\source\marketplace
#
# Prerequisites:
#   - nektos/act 0.2.63+ in PATH (act --version)
#   - Docker Desktop running
#   - catthehacker/ubuntu:act-latest image available (pulled below)
#
# This script does NOT install CLIs on the host — all installs happen
# inside ephemeral Docker containers torn down after each run.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

$RepoRoot = $PSScriptRoot | Split-Path -Parent | Split-Path -Parent
$LogDir = Join-Path $RepoRoot "docs\VERIFICATION_2026-05\logs"
$WorkflowDir = Join-Path $RepoRoot "docs\VERIFICATION_2026-05\workflows"

Write-Host "=== Pulling Docker image (idempotent) ==="
docker pull catthehacker/ubuntu:act-latest

$ActBaseArgs = @(
    "workflow_dispatch",
    "-P", "ubuntu-latest=catthehacker/ubuntu:act-latest",
    "--container-architecture", "linux/amd64",
    "--pull=false"
)

$workflows = @(
    @{ Name = "verify-codex"; Log = "verify-codex-run.log" },
    @{ Name = "verify-gemini"; Log = "verify-gemini-run.log" },
    @{ Name = "verify-cursor"; Log = "verify-cursor-run.log" },
    @{ Name = "verify-claude"; Log = "verify-claude-run.log" }
)

foreach ($wf in $workflows) {
    $YmlPath = Join-Path $WorkflowDir "$($wf.Name).yml"
    $LogPath = Join-Path $LogDir $wf.Log

    Write-Host ""
    Write-Host "=== Running $($wf.Name) ===" -ForegroundColor Cyan
    Write-Host "  Workflow: $YmlPath"
    Write-Host "  Log:      $LogPath"

    $allArgs = $ActBaseArgs + @("-W", $YmlPath)
    & act @allArgs 2>&1 | Tee-Object -FilePath $LogPath

    Write-Host "  Done. Exit: $LASTEXITCODE"
}

Write-Host ""
Write-Host "=== All workflows complete. Log files in: $LogDir ===" -ForegroundColor Green
Write-Host ""
Write-Host "To verify specific claims, grep the logs:"
Write-Host "  Select-String -Path '$LogDir\verify-codex-run.log' -Pattern 'C1_EXIT|C2_EXIT|C3_EXIT|C4_FOUND|C5_EXIT'"
Write-Host "  Select-String -Path '$LogDir\verify-gemini-run.log' -Pattern 'G[1-6]_EXIT|G[1-6]=|G[1-6]_FOUND'"
Write-Host "  Select-String -Path '$LogDir\verify-cursor-run.log' -Pattern 'CU[1-3]_EXIT|CU[1-3]='"
Write-Host "  Select-String -Path '$LogDir\verify-claude-run.log' -Pattern 'CL[1-3]_EXIT|CL[1-3]=|CL[1-3]_FOUND'"
