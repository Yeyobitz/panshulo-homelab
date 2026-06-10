# Panshulo Homelab

[![Linux](https://img.shields.io/badge/OS-Ubuntu_24.04-orange?logo=ubuntu)](https://ubuntu.com)
[![Docker](https://img.shields.io/badge/Docker-20%2B-2496ed?logo=docker)](https://docker.com)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

Self-hosted server running at home. No cloud. Everything under my control.

---

## Current stack

| Category | Services | What it does |
|----------|----------|--------------|
| Streaming | Plex, Jellyfin, Tautulli, Overseerr | Movies, shows, play tracking |
| Automation | Sonarr, Radarr, Bazarr, Prowlarr, qBittorrent | Auto-download and organize media |
| Monitoring | Homarr, Netdata, Flask dashboard | Real-time server stats |
| Development | Gitea, Hermes Agent | Self-hosted Git, AI assistant |
| Finance | Cashflow MVP | Personal finance tracking |
| Access | Tailscale, Cloudflare Tunnel, UFW | VPN, tunnels, firewall |

---

## Architecture

```
Internet
    |
    +-- Cloudflare Tunnel -> Caddy (:8080) -> Web services
    |
    +-- Tailscale VPN -> Server (direct access)
                            |
                    +-------+-------+
                    |               |
              Docker Host      UFW Firewall
            (15+ services)   (default deny)
                    |
            +-------+-------+
            |               |
        NVMe SSD       USB HDD
    (OS + apps 476GB)  (media 931GB)
```

**Hardware:** Lenovo ThinkPad - Intel i7-7600U, 7GB RAM

---

## What I learned

**Linux admin.** Ubuntu Server, systemd, cron, bash scripting. No GUI, all terminal.

**Docker.** 15+ containers with Docker Compose. Networks, volumes, restart policies, port mapping.

**Networking.** UFW with default deny. Tailscale mesh VPN. Cloudflare Tunnel for public services. DNS and routing basics.

**Monitoring.** Custom Flask dashboard using psutil. Netdata for granular metrics. Health checks and alerts via cron and systemd timers.

**Security.** Zero-trust firewall. SSL tunnels everywhere. Nothing hits the internet without going through Cloudflare or Tailscale first.

**Storage.** SSD for OS and apps. USB HDD for media. Partitioning, auto-mount, mixed pool.

**Git.** Gitea self-hosted plus GitHub.

---

## How it started

I had an old notebook lying around and wanted to run my own services without paying monthly fees. Now it's my 24/7 server. Streaming, code repos, metrics, media automation, and a lab to break and fix things.

The name "Panshulo" started as a joke and stuck.

---

## Screenshots

(coming soon - Flask dashboard and service status pages)

---

## Tech stack

OS: Ubuntu Server 24.04 LTS
Containers: Docker + Docker Compose
Firewall: UFW (default deny incoming)
VPN: Tailscale (mesh)
Proxy/Tunnels: Cloudflare Tunnel + Caddy
Monitoring: Netdata + Flask dashboard (Python/psutil)
Git: Gitea

---

## How to use

1. Clone the repo
2. Copy `.env.example` to `.env` and fill in your variables
3. `docker compose -f stack/compose.yml up -d`
4. Configure each service through its web UI

Real values (IPs, tokens, domains) have been replaced with placeholders. No credentials in this repo.

---

## Contact

[LinkedIn](https://linkedin.com/in/yeyobitz) - [GitHub](https://github.com/Yeyobitz) - diegoqm96@hotmail.com
