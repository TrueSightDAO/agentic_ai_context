# Krake Sidekiq Consolidation Plan

**Goal:** Merge 4 separate `krake_sk*` EC2 instances into a single instance.
**Estimated savings:** ~$55/month (4 instances → 1).

---

## Current State

| Instance | Type | Memory | Config | Queues | Cost/mo |
|----------|------|--------|--------|--------|---------|
| krake_sk | t2.nano | 0.5 GB | `sidekiq.yml` | critical, high, medium, low, ec2_processes, default | ~$4 |
| krake_sk_webhook | t2.small | 2 GB | `sidekiq_webhook.yml` | webhook, webhook_emails | ~$17 |
| krake_sk_crawler | t2.small | 2 GB | `sidekiq_crawler.yml` | crawler_loading, pre_crawlers, crawlers | ~$17 |
| krake_sk_scaler | t2.micro | 1 GB | `sidekiq_scaler.yml` | scalers | ~$8 |
| **Total** | | **~5.5 GB** | | | **~$46** |

All 4 run:
- **Same codebase:** `KrakeIO/krake_ror.git` (branch: master)
- **Same Ruby:** 2.6.3 via RVM
- **Same Sidekiq:** 5.2.5
- **Same init:** Upstart (`/etc/init/krake_sk.conf`)
- **Same monit:** `/etc/monit/conf.d/krake_sk.conf`
- **All idle:** 0 of 2 busy (at time of inspection)

### Upstart Script Pattern

All 4 boxes have an identical `/etc/init/krake_sk.conf` except for the Sidekiq config argument:

```bash
sidekiq -e production -C config/sidekiq_<variant>.yml -P tmp/pids/sidekiq.pid
```

The upstart script also does `git pull origin master` and `bundle install` on every start.

### Sidekiq Config Files

All 4 config files exist on every box at `/home/ubuntu/krake_ror/config/`:
- `sidekiq.yml` — general queues
- `sidekiq_webhook.yml` — webhook, webhook_emails
- `sidekiq_crawler.yml` — crawler_loading, pre_crawlers, crawlers
- `sidekiq_scaler.yml` — scalers

---

## Proposed Target State

**Single instance:** `krake_sk_consolidated` — t3.small (2 GB RAM, 2 vCPUs)

### Upstart Scripts (4 separate services, 1 box)

| Service Name | Config File | Queues | Concurrency |
|-------------|-------------|--------|-------------|
| `krake_sk` | `sidekiq.yml` | critical(9), high(8), medium(7), low(9), ec2_processes(5), default(3) | 2 |
| `krake_sk_webhook` | `sidekiq_webhook.yml` | webhook(5), webhook_emails(3) | 2 |
| `krake_sk_crawler` | `sidekiq_crawler.yml` | crawler_loading(20), pre_crawlers(10), crawlers(8) | 2 |
| `krake_sk_scaler` | `sidekiq_scaler.yml` | scalers(8) | 2 |

Each gets its own PID file to avoid conflicts:
- `tmp/pids/sidekiq.pid`
- `tmp/pids/sidekiq_webhook.pid`
- `tmp/pids/sidekiq_crawler.pid`
- `tmp/pids/sidekiq_scaler.pid`

### Monit Config

Single `/etc/monit/conf.d/krake_sk.conf` monitoring all 4 processes.

---

## Migration Steps

### Phase 1: Prepare the target box

1. **Launch a new t3.small** from the existing `krake_sk` AMI (or fresh Ubuntu 18.04 + deploy)
   - Same security group as current krake_sk boxes
   - Same subnet (for Redis/DB access)
   - Key pair: `GETDATA_IO_PAIR_20201122`

2. **Verify the app is deployed**
   ```bash
   ssh ubuntu@<new-ip>
   cd /home/ubuntu/krake_ror
   git pull origin master
   bundle install
   ```

3. **Create 4 Upstart scripts**

   `/etc/init/krake_sk.conf`:
   ```bash
   description "Sidekiq - General Queues"
   setuid ubuntu
   setgid ubuntu
   env HOME=/home/ubuntu
   respawn
   respawn limit 3 30
   normal exit 0 TERM
   reload signal USR1
   kill timeout 15

   script
   exec /bin/bash <<'EOT'
     source /home/ubuntu/.profile
     cd /home/ubuntu/krake_ror/
     bundle exec sidekiq -e production -C config/sidekiq.yml -P tmp/pids/sidekiq.pid
   EOT
   end script
   ```

   Repeat for `krake_sk_webhook`, `krake_sk_crawler`, `krake_sk_scaler` with their respective config files and PID files.

4. **Update Monit**

   `/etc/monit/conf.d/krake_sk.conf`:
   ```
   check process krake_sk with pidfile /home/ubuntu/krake_ror/tmp/pids/sidekiq.pid
     start program = "/usr/sbin/service krake_sk start" with timeout 60 seconds
     stop program  = "/usr/sbin/service krake_sk stop"
     if memory usage > 65% then restart
     if does not exist then start

   check process krake_sk_webhook with pidfile /home/ubuntu/krake_ror/tmp/pids/sidekiq_webhook.pid
     start program = "/usr/sbin/service krake_sk_webhook start" with timeout 60 seconds
     stop program  = "/usr/sbin/service krake_sk_webhook stop"
     if memory usage > 65% then restart
     if does not exist then start

   # ... repeat for crawler and scaler
   ```

### Phase 2: Cut over

5. **Stop Sidekiq on old boxes** (one at a time, drain queues first)
   ```bash
   # On each old box:
   sudo service krake_sk stop
   ```

6. **Start all 4 services on the new box**
   ```bash
   sudo start krake_sk
   sudo start krake_sk_webhook
   sudo start krake_sk_crawler
   sudo start krake_sk_scaler
   ```

7. **Verify**
   ```bash
   ps aux | grep sidekiq | grep -v grep
   # Should show 4 sidekiq processes
   ```

### Phase 3: Cleanup

8. **Monitor for 48 hours** — check logs, verify queues are processing
9. **Stop old instances** (don't terminate for 1 week as rollback)
10. **Terminate old instances** after confirmation

---

## Rollback Plan

If something goes wrong:
1. Start the old boxes back up
2. Stop the new box's Sidekiq services
3. Investigate

The old boxes are stopped, not terminated, so this is a quick recovery.

---

## What Stays Separate

| Instance | Reason |
|----------|--------|
| **krake_ror** | Rails web server — different role |
| **krake_data** | PostgreSQL database — 50 GB data volume |
| **GETDATA_REDIS** | Redis — different service |
| **GETDATA_CACHE** | Different codebase (`krake_publisher`) — can't merge |

---

## Cost Analysis

| Item | Current | Proposed | Savings |
|------|---------|----------|---------|
| 4× krake_sk instances | ~$46/mo | ~$17/mo (t3.small) | **~$29/mo** |
| EIP | $0 (1st EIP free) | $0 | $0 |
| **Total** | **~$46/mo** | **~$17/mo** | **~$29/mo** |

*Note: Actual savings depend on reserved vs on-demand pricing.*

---

## Appendix: SSH Access

All krake boxes use `GETDATA_IO_PAIR_20201122.pem` key. From the autopilot:

```bash
ssh -o PubkeyAcceptedKeyTypes=+ssh-rsa -o HostKeyAlgorithms=+ssh-rsa \
  -i ~/.ssh/NELANCO_aws_20201122.pem ubuntu@<ip>
```
