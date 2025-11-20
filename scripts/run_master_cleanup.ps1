param([switch]$DryRun)
$arg = if ($DryRun) { '--dry-run' } else { '' }
$wslCmd = "cd /home/tec_tgcr/luminai-codex && python3 scripts/master_cleanup.py $arg"
# call explicit wsl.exe
wsl.exe -d Ubuntu -- bash -lc $wslCmd
