# Panshulo Homelab 🖥️

[![Linux](https://img.shields.io/badge/OS-Ubuntu_24.04-orange?logo=ubuntu)](https://ubuntu.com)
[![Docker](https://img.shields.io/badge/Docker-20%2B-2496ed?logo=docker)](https://docker.com)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

> Homelab server — infraestructura completa de servicios auto-hosteada.
> El objetivo: automatizar todo lo repetitivo, aprender infraestructura real, y tener control total de mis datos.

---

## 📊 Stack actual

| Categoría | Servicios | Propósito |
|-----------|-----------|-----------|
| **🎬 Streaming** | Plex, Jellyfin, Tautulli, Overseerr | Películas, series, tracking de reproducción |
| **🤖 Automatización** | Sonarr, Radarr, Bazarr, Prowlarr, qBittorrent | Descarga y organización automática de medios |
| **📊 Monitoreo** | Homarr, Netdata, Dashboard propio (Flask) | Estado del servidor en tiempo real |
| **💻 Desarrollo** | Gitea, Hermes Agent | Git self-hosted, agente AI |
| **💰 Finanzas** | Cashflow MVP | Gestión de finanzas personales |
| **🔐 Acceso** | Tailscale, Cloudflare Tunnel, UFW | VPN + túneles + firewall zero-trust |

---

## 🏗️ Arquitectura

```
Internet
    │
    ├── Cloudflare Tunnel ──► Caddy (:8080) ──► Servicios web
    │
    └── Tailscale VPN ──► Servidor (acceso directo)
                            │
                    ┌───────┴───────┐
                    │               │
              Docker Host      UFW Firewall
            (15+ servicios)   (default deny)
                    │
            ┌───────┼───────┐
            │       │       │
        NVMe SSD   USB HDD 8GB RAM
        (SO + apps) (media) Intel i7-7600U
```

**Hardware:** Lenovo ThinkPad — Intel i7-7600U, 7GB RAM, 476GB NVMe + 931GB HDD

---

## 🛠️ Lo que aprendí (y demuestra)

| Skill | Lo que hice |
|-------|------------|
| **Linux SysAdmin** | Ubuntu Server headless, systemd, cron, bash scripting, sin GUI |
| **Docker** | 15+ contenedores con Docker Compose, redes, volúmenes, reinicio automático |
| **Redes** | UFW (default deny), Tailscale VPN, Cloudflare Tunnel, DNS, routing |
| **Monitoreo** | Dashboard Flask custom, Netdata, health checks, alertas |
| **Seguridad** | Firewall zero-trust, túneles SSL, VPN, puertos solo desde LAN |
| **Almacenamiento** | Particionamiento, montaje automático, SSD + HDD pool |
| **Git** | Gitea self-hosted + GitHub, CI básico |

---

## 🚀 Cómo surgió

Empecé con un notebook viejo y la idea de tener mis propios servicios sin depender de terceros. Hoy es mi servidor principal 24/7 que me da streaming, backup de código, métricas, automatización de medios, y un sandbox para aprender infraestructura real.

El nombre "Panshulo" empezó como talla y se quedó.

---

## 📸 Capturas

_(Próximamente — dashboard Flask personalizado y estado de servicios)_

---

## 🔧 Stack técnico

- **OS:** Ubuntu Server 24.04 LTS
- **Contenedores:** Docker + Docker Compose
- **Firewall:** UFW (default deny incoming)
- **VPN:** Tailscale (mesh VPN)
- **Proxy/Túneles:** Cloudflare Tunnel, Caddy
- **Monitoreo:** Netdata, dashboard Flask custom (Python/psutil)
- **Git:** Gitea

---

## ⚙️ Cómo usar

1. Clona el repo
2. Copia `.env.example` a `.env` y completa tus variables
3. `docker compose -f stack/compose.yml up -d`
4. Configura los servicios desde sus respectivas UIs

> **⚠️ Este repo es un portfolio.** Los valores reales (IPs, tokens, dominios) han sido reemplazados por placeholders por seguridad.

---

## 📬 Contacto

[LinkedIn](https://linkedin.com/in/) | [Email](mailto:diegoqm96@hotmail.com)

---

*Hecho con 💻 y café desde Chile — abierto a oportunidades remotas en Canada/USA.*
