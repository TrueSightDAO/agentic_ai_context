# S3 Asset Convention — China Firewall Bypass

## Purpose

Direct download URLs to `assets.truesight.me` do not have a valid SSL certificate for that hostname, making HTTPS downloads via the custom domain unreliable in some environments. Use the raw S3 endpoint instead.

## Bucket

- **Account**: Nelanco (AWS)
- **Bucket**: `assets.truesight.me`
- **Region**: us-east-1
- **Access**: Objects uploaded with `--acl public-read`

## Raw S3 URL Format

```
https://s3.amazonaws.com/assets.truesight.me/{folder}/{filename}
```

Or region-specific:

```
https://s3.us-east-1.amazonaws.com/assets.truesight.me/{folder}/{filename}
```

## Convention

1. Upload all presentation files (PPTX, PDF) meant for Chinese partners to `s3://assets.truesight.me/cacao-deck/`
2. Use `--acl public-read` on upload
3. Share the **raw S3 endpoint** URL (not the custom domain), as `assets.truesight.me` has SSL hostname mismatch
4. Both URLs are functionally identical — use the shorter one:
   `https://s3.amazonaws.com/assets.truesight.me/cacao-deck/filename.pptx`

## Current Files (July 2026)

| File | Size | S3 URL |
|---|---|---|
| Cacao_Tea_China_Opportunity_EN.pptx | 22.2 MB | [Download](https://s3.amazonaws.com/assets.truesight.me/cacao-deck/Cacao_Tea_China_Opportunity_EN.pptx) |
| Cacao_Tea_China_Opportunity_CN.pptx | 22.2 MB | [Download](https://s3.amazonaws.com/assets.truesight.me/cacao-deck/Cacao_Tea_China_Opportunity_CN.pptx) |

## Temp Credentials

The autopilot box does not have permanent AWS credentials. Uploads require a fresh STS token from the `nelanco` account, obtained via `aws_query(account='nelanco', service='sts', operation='GetSessionToken')`. The token is valid for 1 hour.

Upload command:

```bash
/home/ubuntu/.local/bin/aws s3 cp <local_file> s3://assets.truesight.me/<path> --acl public-read
```
