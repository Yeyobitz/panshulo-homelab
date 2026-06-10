# Panshulo Homelab - Network Architecture

## Network diagram

```mermaid
graph TB
    subgraph Internet
        CF[Cloudflare]
        USER[User/Phone]
    end

    subgraph "Tailscale Mesh VPN"
        TS[100.x.x.x/10]
    end

    subgraph "LAN 192.168.1.0/24"
        ROUTER[Router]
    end

    subgraph "Server"
        direction TB
        FW[UFW Firewall<br/>default deny inbound]
        CT[Cloudflare Tunnel<br/>cloudflared]
        CADDY[Caddy :8080<br/>reverse proxy]

        subgraph "Docker Host"
            PLEX[Plex :32400]
            JELLY[Jellyfin :8096]
            SONARR[Sonarr :8989]
            RADARR[Radarr :7878]
            BAZARR[Bazarr :6767]
            PROWLARR[Prowlarr :9696]
            QBIT[qBittorrent :8085]
            OVERSEER[Overseerr :5055]
            TAUTULLI[Tautulli :8181]
            HOMARR[Homarr :7575]
            GITEA[Gitea :3000]
            CASHFLOW[Cashflow MVP :5050]
            HERMES[Hermes Agent :8642/9119]
            DASHBOARD[Dashboard Flask :5057]
            NETDATA[Netdata :19999]
        end

        subgraph "Storage"
            NVME[NVMe 476GB<br/>OS + Apps]
            HDD[USB HDD 931GB<br/>Media: movies/series/music]
        end
    end

    USER -->|Cloudflare Tunnel| CT
    USER -->|Tailscale| TS
    CF -->|SSL/TLS| CT
    CT --> CADDY
    CADDY --> PLEX
    CADDY --> JELLY
    CADDY --> OVERSEER
    CADDY --> GITEA

    ROUTER -->|LAN ports| FW
    TS -->|Encrypted| FW
    FW --> DASHBOARD
    FW --> SONARR
    FW --> RADARR
    FW --> HOMARR
    FW --> CASHFLOW
    FW --> GITEA
    FW --> HERMES

    PLEX --> HDD
    JELLY --> HDD
    SONARR --> HDD
    RADARR --> HDD
```

## Ports exposed on LAN

| Port | Service | Access |
|------|---------|--------|
| 22/tcp | SSH | LAN + Tailscale only |
| 3000/tcp | Gitea | LAN + Cloudflare Tunnel |
| 32400/tcp | Plex | LAN |
| 5050/tcp | Cashflow MVP | LAN |
| 5051/tcp | Student Directory | LAN |
| 5055/tcp | Overseerr | LAN |
| 5057/tcp | Dashboard | LAN |
| 6767/tcp | Bazarr | LAN |
| 7575/tcp | Homarr | LAN |
| 7878/tcp | Radarr | LAN |
| 8080/tcp | Caddy | LAN + Cloudflare Tunnel |
| 8085/tcp | qBittorrent | LAN |
| 8096/tcp | Jellyfin | LAN |
| 8181/tcp | Tautulli | LAN |
| 8642/tcp | Hermes Agent | LAN |
| 8989/tcp | Sonarr | LAN |
| 9119/tcp | Hermes Agent WS | LAN |
| 9696/tcp | Prowlarr | LAN |
| 19999/tcp | Netdata | LAN |

## Security

- UFW: default deny inbound, allowlist only
- Tailscale mesh VPN for remote access (no ports exposed to internet)
- Cloudflare Tunnel for public web services (no open ports on router)
- Caddy reverse proxy with automatic SSL
- IPv6 fully blocked (including Docker forwarded traffic)

## Remote access flow

```
Phone/Laptop
    |
    +-- Cloudflare Tunnel (no open ports)
    |   +-- Gitea, Overseerr
    |
    +-- Tailscale (mesh VPN)
        +-- All services as if on LAN
```
