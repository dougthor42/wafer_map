Write-Host "Installing 7-Zip ..."
$instPath = "$env:ProgramFiles\7-Zip\7z.exe"
if (!(Test-Path $instPath))
{
    Write-Host "Determining download URL ..."
    $web = New-Object System.Net.WebClient
    $page = $web.DownloadString("http://www.7-zip.org/download.html")

    $64bit = ''

    if ($env:PROCESSOR_ARCHITECTURE -match '64')
    {
        $64bit = 'x64'
    }

    $pattern = "(http://.*?${64bit}\.msi)"
    $url = $page | Select-String -Pattern $pattern | Select-Object -ExpandProperty Matches -First 1 | foreach { $_.Value }

    $file = "$env:TEMP\7z.msi"
    if (Test-Path $file)
    {    
        rm $file | Out-Null
    }
    
    Write-Host "Downloading $url -> $file"

    $web.DownloadFile($url, $file)

    Write-Host "Installing..."
    Write-Host "(Note: please approve the User Account Control (UAC) popup if necessary...)"

    $cmd = "$file /passive"

    Invoke-Expression $cmd | Out-Null

    while (!(Test-Path $instPath))
    {
        Start-Sleep -Seconds 10
    }

    Write-Host "Done!"
}
else
{
    Write-Host "7-Zip already installed."
}