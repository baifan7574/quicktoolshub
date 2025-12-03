# Ghostscript Auto Install Script

Write-Host "Downloading Ghostscript..." -ForegroundColor Green

$url = "https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs1000/gs1000w64.exe"
$installer = "$PSScriptRoot\gs-installer.exe"

try {
    Invoke-WebRequest -Uri $url -OutFile $installer -UseBasicParsing
    Write-Host "Download completed: $installer" -ForegroundColor Green
    
    if (Test-Path $installer) {
        $fileSize = (Get-Item $installer).Length
        Write-Host "File size: $([math]::Round($fileSize/1MB, 2)) MB" -ForegroundColor Green
        
        Write-Host "`nInstalling Ghostscript (requires admin rights)..." -ForegroundColor Yellow
        Write-Host "Note: The installer may show a window. Please follow the prompts." -ForegroundColor Yellow
        
        $installArgs = "/S"
        Start-Process -FilePath $installer -ArgumentList $installArgs -Wait -Verb RunAs
        
        Write-Host "`nInstallation completed! Verifying..." -ForegroundColor Green
        
        Start-Sleep -Seconds 3
        
        $machinePath = [System.Environment]::GetEnvironmentVariable("Path","Machine")
        $userPath = [System.Environment]::GetEnvironmentVariable("Path","User")
        $env:Path = "$machinePath;$userPath"
        
        try {
            $version = & gs --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "`nSUCCESS! Ghostscript installed. Version: $version" -ForegroundColor Green
            } else {
                Write-Host "`nWARNING: Ghostscript may be installed but you may need to restart the terminal." -ForegroundColor Yellow
                Write-Host "Please run 'gs --version' to verify." -ForegroundColor Yellow
            }
        } catch {
            Write-Host "`nWARNING: Installation may be complete, but you need to restart the terminal." -ForegroundColor Yellow
            Write-Host "Please close and reopen the terminal, then run 'gs --version' to verify." -ForegroundColor Yellow
        }
        
        Write-Host "`nCleaning up installer..." -ForegroundColor Gray
        Remove-Item $installer -ErrorAction SilentlyContinue
        
    } else {
        Write-Host "ERROR: Downloaded file does not exist" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "`nERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "`nPlease manually download and install Ghostscript:" -ForegroundColor Yellow
    Write-Host "1. Visit: https://www.ghostscript.com/download/gsdnld.html" -ForegroundColor Yellow
    Write-Host "2. Download Windows 64-bit version" -ForegroundColor Yellow
    Write-Host "3. Run the installer" -ForegroundColor Yellow
    exit 1
}
