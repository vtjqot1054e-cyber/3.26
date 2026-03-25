Set-Location "E:\----2"
$status = git status --porcelain
if ($status) {
    git add -A
    git commit -m "auto-sync $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git push
}
