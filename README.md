# Panshulo Homelab

[![Linux](https://img.shields.io/badge/OS-Ubuntu_24.04-orange?logo=ubuntu)](https://ubuntu.com)
[![Docker](https://img.shields.io/badge/Docker-20%2B-2496ed?logo=docker)](https://docker.com)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

Un servidor casero con servicios auto-hosteado. Nada de nube. Todo mio.

---

## Stack actual

| Categoria | Servicios | Para que |
|-----------|-----------|----------|
| Streaming | Plex, Jellyfin, Tautulli, Overseerr | Peliculas, series, tracking |
| Automatizacion | Sonarr, Radarr, Bazarr, Prowlarr, qBittorrent | Descarga y organizacion automatica |
| Monitoreo | Homarr, Netdata, Dashboard Flask | Estado del server en tiempo real |
| Desarrollo | Gitea, Hermes Agent | Git propio, agente AI |
| Finanzas | Cashflow MVP | Gestion de lucas |
| Acceso | Tailscale, Cloudflare Tunnel, UFW | VPN + tuneles + firewall |

---

## Arquitectura

```
Internet
    │
    ├── Cloudflare Tunnel -> Caddy (:8080) -> Servicios web
    │
    └── Tailscale VPN -> Servidor (acceso directo)
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

**Hardware:** Lenovo ThinkPad - Intel i7-7600U, 7GB RAM, 476GB NVMe + 931GB HDD

---

## Que aprendi

Linux SysAdmin: Ubuntu Server headless, systemd, cron, bash scripting, cero GUI.

Docker: 15+ contenedores con Docker Compose. Redes, volumenes, restart policies.

Redes: UFW con default deny, Tailscale VPN, Cloudflare Tunnel, DNS, routing basico.

Monitoreo: Dashboard en Flask con psutil + Netdata. Health checks y alertas via cron y systemd.

Seguridad: Firewall zero-trust, tuneles SSL, VPN mesh. Nada expuesto al mundo sin pasar por Cloudflare o Tailscale.

Almacenamiento: SSD para el SO y apps, HDD USB para media. Particionado, montaje automatico.

Git: Gitea auto-hosteado + GitHub.

---

## Como surgio

Empece con un notebook tirado y la idea de tener mis servicios sin pagarle a nadie. Hoy es mi servidor 24/7. Streaming, repos de codigo, metricas, automatizacion de medios, y un laboratorio para romper cosas y arreglarlas.

El nombre "Panshulo" empezo como talla y se quedo.

---

## Capturas

(proximamente - dashboard Flask y estado de servicios)

---

## Stack tecnico

OS: Ubuntu Server 24.04 LTS
Contenedores: Docker + Docker Compose
Firewall: UFW (default deny incoming)
VPN: Tailscale (mesh)
Proxy/Tuneles: Cloudflare Tunnel + Caddy
Monitoreo: Netdata + dashboard Flask (Python/psutil)
Git: Gitea

---

## Como usar

1. Clona el repo
2. Copia `.env.example` a `.env` y completa tus variables
3. `docker compose -f stack/compose.yml up -d`
4. Configura los servicios desde sus respectivas UIs

Los valores reales (IPs, tokens, dominios) estan reemplazados por placeholders. No subo credenciales a GitHub.

---

## Contacto

[LinkedIn](https://linkedin.com/in/) - diegoqm96@hotmail.com
