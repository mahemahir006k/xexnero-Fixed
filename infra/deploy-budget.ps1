param(
    [Parameter(Mandatory=$true)]
    [string]$AlertEmail,

    [string]$BudgetLimitUSD = "25",
    [string]$Region = "ap-south-1"
)

$ErrorActionPreference = "Stop"

$stackName = "xexnaro-cost-guard"
$template = Join-Path $PSScriptRoot "aws-budget-alarms.yml"

Write-Host "Deploying Xexnaro AWS budget alarms..."
aws cloudformation deploy `
    --stack-name $stackName `
    --template-file $template `
    --region $Region `
    --parameter-overrides BudgetLimitUSD=$BudgetLimitUSD AlertEmail=$AlertEmail

Write-Host "Budget alarm stack deployed."
Write-Host "Confirm the budget email subscription when AWS sends it."
