# Environment Variables Verification Script for Render Deployment
# Run this before deploying to ensure all variables are set correctly

Write-Host "================================" -ForegroundColor Cyan
Write-Host "TVET@2026 Environment Checker" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (Test-Path ".env") {
    Write-Host "✓ .env file found" -ForegroundColor Green
    
    # Load .env file
    $envContent = Get-Content ".env"
    
    # Check required variables
    $requiredVars = @(
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY",
        "SUPABASE_SERVICE_ROLE_KEY"
    )
    
    Write-Host "`nChecking required variables:" -ForegroundColor Yellow
    
    foreach ($var in $requiredVars) {
        $found = $envContent | Where-Object { $_ -match "^$var=" }
        if ($found) {
            $value = ($found -split "=", 2)[1]
            if ($value -and $value -ne "" -and $value -notmatch "your-|replace-with") {
                Write-Host "  ✓ $var is set" -ForegroundColor Green
            } else {
                Write-Host "  ✗ $var is empty or placeholder" -ForegroundColor Red
            }
        } else {
            Write-Host "  ✗ $var is missing" -ForegroundColor Red
        }
    }
} else {
    Write-Host "✗ .env file not found!" -ForegroundColor Red
    Write-Host "  Please create .env file with your Supabase credentials" -ForegroundColor Yellow
}

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "Git Repository Check" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Check if git initialized
if (Test-Path ".git") {
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
    
    # Check remote
    $remote = git remote get-url origin 2>$null
    if ($remote) {
        Write-Host "✓ Remote configured: $remote" -ForegroundColor Green
    } else {
        Write-Host "✗ No remote configured" -ForegroundColor Red
    }
    
    # Check if .env is in .gitignore
    if (Test-Path ".gitignore") {
        $gitignore = Get-Content ".gitignore"
        if ($gitignore -match "\.env") {
            Write-Host "✓ .env is in .gitignore" -ForegroundColor Green
        } else {
            Write-Host "✗ .env is NOT in .gitignore!" -ForegroundColor Red
        }
    }
} else {
    Write-Host "✗ Git not initialized" -ForegroundColor Red
}

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "Render Deployment Files" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

$deploymentFiles = @(
    "render.yaml",
    "backend/requirements.txt",
    "frontend/package.json"
)

foreach ($file in $deploymentFiles) {
    if (Test-Path $file) {
        Write-Host "✓ $file exists" -ForegroundColor Green
    } else {
        Write-Host "✗ $file missing" -ForegroundColor Red
    }
}

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "Supabase Configuration" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Before deploying, ensure you have:" -ForegroundColor Yellow
Write-Host "  1. Created a Supabase project" -ForegroundColor White
Write-Host "  2. Obtained the database connection string" -ForegroundColor White
Write-Host "  3. Set up authentication in Supabase dashboard" -ForegroundColor White
Write-Host "  4. Created necessary database tables" -ForegroundColor White

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "Next Steps" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Get Database URL from Supabase:" -ForegroundColor Yellow
Write-Host "   https://supabase.com/dashboard/project/psdxitqfusfmkutxsojc/settings/database" -ForegroundColor White
Write-Host ""
Write-Host "2. Deploy on Render:" -ForegroundColor Yellow
Write-Host "   https://dashboard.render.com" -ForegroundColor White
Write-Host "   → New + → Blueprint → Connect alexfreed254/tvet2026" -ForegroundColor White
Write-Host ""
Write-Host "3. See RENDER-QUICK-START.md for detailed steps" -ForegroundColor Yellow
Write-Host ""
