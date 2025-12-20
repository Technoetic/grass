# Git 자동 설치 스크립트
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Git 설치 스크립트" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Git 설치 프로그램 다운로드 URL
$gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
$installerPath = "$env:TEMP\GitInstaller.exe"

Write-Host "📥 Git 설치 프로그램 다운로드 중..." -ForegroundColor Yellow
Write-Host "URL: $gitUrl" -ForegroundColor Gray

try {
    # 다운로드
    Invoke-WebRequest -Uri $gitUrl -OutFile $installerPath -UseBasicParsing
    Write-Host "✅ 다운로드 완료!" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "🔧 Git 설치 중..." -ForegroundColor Yellow
    Write-Host "설치 창이 열립니다. 기본 설정으로 'Next'를 클릭하세요." -ForegroundColor Cyan
    Write-Host ""
    
    # 자동 설치 실행 (조용한 모드)
    $arguments = "/VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS=icons,ext\shellhere,assoc,assoc_sh"
    Start-Process -FilePath $installerPath -ArgumentList $arguments -Wait
    
    Write-Host ""
    Write-Host "✅ Git 설치 완료!" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  중요: 터미널을 다시 시작해야 Git을 사용할 수 있습니다." -ForegroundColor Yellow
    Write-Host "   Cursor를 재시작하거나 새 터미널을 열어주세요." -ForegroundColor Yellow
    Write-Host ""
    
    # 임시 파일 삭제
    Remove-Item $installerPath -ErrorAction SilentlyContinue
    
} catch {
    Write-Host "❌ 오류 발생: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "수동 설치 방법:" -ForegroundColor Yellow
    Write-Host "1. https://git-scm.com/download/win 방문" -ForegroundColor Cyan
    Write-Host "2. 다운로드한 설치 프로그램 실행" -ForegroundColor Cyan
    Write-Host "3. 기본 설정으로 설치 진행" -ForegroundColor Cyan
    exit 1
}

