# Getdata.io SSL Recovery Plan

**Status:** Active — Gary executing via Telegram thread 9177
**Created:** 2026-07-18
**Owner:** Gary Teh / Sophia Truesight

## Goal
Replace the expired/broken Comodo SSL cert on `getdata.io` with an Amazon-issued ACM cert (auto-renewing, free).

## Units

### Unit 1 ✅ — Request ACM cert + DNS validation
- [x] Request Amazon-issued ACM cert in **Nelanco** (us-east-1) for `getdata.io` + `*.getdata.io`
- [x] Add DNS validation CNAME record to `getdata.io` hosted zone in **Explorya** Route53
- [ ] Wait for ACM to validate → status flips to ISSUED

### Unit 2 — Associate cert with NLB/ALB
- [ ] Identify which load balancer serves `getdata.io` (krake Nginx? NLB?)
- [ ] Associate the ACM cert with the HTTPS listener
- [ ] Verify TLS handshake on `https://getdata.io`

### Unit 3 — Cleanup
- [ ] Remove old Comodo cert from Nginx (if still referenced)
- [ ] Remove old DNS validation CNAMEs for Comodo (`_9e7da9668b015f3183da1358e51c06f9.getdata.io`, `_bd012ac3889dac7feea4c25e00ed644a.getdata.io`, `5ae60df7af05d72938731edf21c03a8d.getdata.io`)

## Key details

| Item | Value |
|------|-------|
| ACM Cert ARN | `arn:aws:acm:us-east-1:767697632458:certificate/8e76c9ff-f1a8-491a-8d86-f2dc2caabdd7` |
| DNS zone | Explorya `/hostedzone/Z1WSQ5L32FCMCC` |
| Validation CNAME | `_9ef609a13ec8920f051efb34e52d6ba2.getdata.io` → `_db5aed0bc044849b5a2ca95da807354f.jkddzztszm.acm-validations.aws.` |
| NLB (krake) | `krake-ror-1-1141435618.us-east-1.elb.amazonaws.com` |
