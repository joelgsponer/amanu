# Scheduler templates

P8 (and any background extension: `watch-inbox`, `scheduled-maintenance`,
`compile-memory`, `encrypted-backup`) fills one of these instead of hand-writing
scheduler config — the single biggest source of "worked in the session, dead after
reboot." Pick by the OS found in the preflight (§B), replace every `{{...}}`, and
**register idempotently** (unregister-then-register) so a re-run never double-loads.

Placeholders: `{{LABEL}}` (reverse-DNS-ish, e.g. `amanu.watch-inbox`), `{{CMD}}`
(absolute path to the script/interpreter), `{{ARGS}}`, `{{WORKDIR}}`, `{{LOG}}`
(absolute log path), `{{STATE}}` (heartbeat file, e.g. `<WORKDIR>/tools/<name>.state`),
`{{CALENDAR}}` (systemd `OnCalendar`, e.g. `daily`), `{{CRON}}` (5-field cron).

**Every scheduled job must write a heartbeat** — append/refresh `{{STATE}}` with a
`last_ok` timestamp on each successful run, so `/healthcheck` and start-of-session
checks detect a silently-dead job even between sessions.

## macOS — launchd  (`launchd.plist`)
Install to `~/Library/LaunchAgents/{{LABEL}}.plist`, then **modern** load:
```sh
launchctl bootout  gui/$(id -u)/{{LABEL}} 2>/dev/null   # idempotent: remove if present
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/{{LABEL}}.plist
launchctl kickstart -k gui/$(id -u)/{{LABEL}}           # start now
launchctl print     gui/$(id -u)/{{LABEL}}              # status (boot-persistent via RunAtLoad)
```
A watcher may need **Full Disk Access / Automation** permission (System Settings →
Privacy & Security) — flag this in the preflight.

## Linux — systemd user units  (`systemd.service` + `systemd.timer`)
Install to `~/.config/systemd/user/{{LABEL}}.{service,timer}`, then:
```sh
systemctl --user daemon-reload
systemctl --user enable --now {{LABEL}}.timer    # enable = boot-persistent
systemctl --user status {{LABEL}}.timer          # status
loginctl enable-linger "$USER"                    # so user timers run without an active login
```

## Anywhere — cron  (`crontab.txt`)
Idempotent install (no duplicate lines), marked by `{{LABEL}}`:
```sh
( crontab -l 2>/dev/null | grep -v "# amanu:{{LABEL}}" ; cat crontab.txt ) | crontab -
crontab -l | grep "# amanu:{{LABEL}}"             # status (cron @reboot persistence is best-effort)
```
Note `cron` runs with a minimal `PATH`/env — use absolute paths in `{{CMD}}`.
