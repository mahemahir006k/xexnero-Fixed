# Xexnaro Daily Facebook Automation - cost-controlled
$ErrorActionPreference = "Stop"

$flowiseBaseUrl = "http://localhost:3000"
$flowId = "f4e00396-7d8b-497a-b6ff-d669cdbd2449"
$flowiseApiKey = ""
$logDirectory = "C:\AI Agent\logs"
$today = Get-Date -Format "yyyy-MM-dd"
$logFile = Join-Path $logDirectory "facebook-post-$today.log"

if (-not (Test-Path $logDirectory)) {
    New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
}

function Write-Log {
    param([string]$Message)
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - $Message"
    Add-Content -Path $logFile -Value $line
    Write-Output $line
}

try {
    Write-Log "Daily Facebook automation started."

    Invoke-WebRequest -Uri $flowiseBaseUrl -UseBasicParsing -TimeoutSec 15 | Out-Null

    $prompt = @"
Create ONE professional Facebook post for an AI technology page.

Choose one useful topic related to AI, automation, generative AI,
machine learning, digital transformation, AI productivity, or cloud AI.

Requirements:
- Professional caption
- Clear CTA
- Exactly 5 relevant hashtags
- Generate a premium square image only if the Flowise workflow has image generation enabled
- Publish to the configured Facebook Page
- Return only the final publishing result
"@

    $requestBody = @{
        question = $prompt
        streaming = $false
        overrideConfig = @{
            sessionId = "daily-facebook-$today"
        }
    } | ConvertTo-Json -Depth 10

    $headers = @{}
    if (-not [string]::IsNullOrWhiteSpace($flowiseApiKey)) {
        $headers["Authorization"] = "Bearer $flowiseApiKey"
    }

    $predictionUrl = "$flowiseBaseUrl/api/v1/prediction/$flowId"
    Write-Log "Calling Flowise once for today's post."

    $response = Invoke-RestMethod `
        -Method Post `
        -Uri $predictionUrl `
        -Headers $headers `
        -ContentType "application/json" `
        -Body $requestBody `
        -TimeoutSec 600

    $responseText = if ($null -ne $response.text) {
        [string]$response.text
    } else {
        ($response | ConvertTo-Json -Depth 10 -Compress)
    }

    # Do not write the full model/Facebook response to disk.
    Write-Log "Flowise returned $($responseText.Length) characters."

    try {
        $facebookResult = $responseText | ConvertFrom-Json

        if (
            -not [string]::IsNullOrWhiteSpace($facebookResult.post_id) -and
            -not [string]::IsNullOrWhiteSpace($facebookResult.id)
        ) {
            Write-Log "Facebook post published successfully. photo=$($facebookResult.id) post=$($facebookResult.post_id)"
            exit 0
        }
    } catch {
        Write-Log "Flowise output was not valid Facebook JSON."
    }

    Write-Log "Workflow completed but no Facebook post ID was detected."
    exit 1
}
catch {
    Write-Log "ERROR: $($_.Exception.Message)"
    exit 1
}
