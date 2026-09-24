# Xexnaro AWS Cost Optimization

This version applies six requested cost controls.

## 15. Duplicate cleanup
- Removed the nested `facebook-poster/facebook-poster/` duplicate project.
- Removed the old `facebook_publisher - backup.py`.
- Removed previously generated output media from the distribution ZIP.

## 16. Company-data caching
`topic_knowledge.py` now caches `company_text.txt` locally for 6 hours by default.

## 17. Topic/research caching
- News research is cached per topic/query for 6 hours.
- Repeated calls for the same topic use the cached RSS result.
- Topic JSON is cached in-process for 60 seconds.

## 18. Batch analytics
Events are recorded locally in SQLite and summarized by:
`GET /analytics/daily`

No AI call is made for each analytics event.

## 19. API-call limits
Persistent daily limits are enforced in SQLite:
- News fetch: 10/day
- LLM generation: 5/day
- LLM review: 5/day
- Image generation: 3/day
- Facebook publish: 2/day

Override in `.env` only when required.

## 20. AWS budget alarms
Deploy `infra/aws-budget-alarms.yml` with:
```powershell
.\infra\deploy-budget.ps1 -AlertEmail "you@example.com" -BudgetLimitUSD "25"
```

Alerts are sent at 50%, 80%, 100%, plus a forecasted 100% threshold.
The template does not automatically delete or stop resources.

## Additional safeguards
- Caption review retries reduced from 2 retries to 1 retry.
- Pollinations image retries reduced from 3 to 2.
- PowerShell automation no longer stores full Flowise responses in logs.
- Image generation can be disabled with `ENABLE_IMAGE_GENERATION=false`.

## Important
These changes reduce unnecessary application/API activity. They do not guarantee a specific AWS bill. If AWS credits are still being consumed quickly, check AWS Cost Explorer by service to identify whether EC2, EBS, NAT Gateway, CloudWatch, Bedrock, Lambda, or another service is the actual cost driver.
