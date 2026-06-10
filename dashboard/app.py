#!/usr/bin/env python3
"""
Panshulo Dashboard
Flask app — server metrics dashboard with real-time monitoring.
Runs on localhost only for security.
"""
import os
import subprocess
from functools import lru_cache

import psutil
import requests
from flask import Flask, jsonify, render_template, request

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
HOST = "127.0.0.1"
PORT = 5057
REFRESH_SECONDS = 10

# Services monitored — format: (name, URL, icon, port)
SERVICES = [
    ("Plex",         "http://127.0.0.1:32400/web",       "🎬", 32400),
    ("Jellyfin",     "http://127.0.0.1:8096",            "📺", 8096),
    ("Sonarr",       "http://127.0.0.1:8989",            "📡", 8989),
    ("Radarr",       "http://127.0.0.1:7878",            "🎯", 7878),
    ("qBittorrent",  "http://127.0.0.1:8085",            "⚡", 8085),
    ("Prowlarr",     "http://127.0.0.1:9696",            "🔍", 9696),
    ("Overseerr",    "http://127.0.0.1:5055",            "🍿", 5055),
    ("Bazarr",       "http://127.0.0.1:6767",            "💬", 6767),
    ("Tautulli",     "http://127.0.0.1:8181",            "📊", 8181),
    ("Homarr",       "http://127.0.0.1:7575",            "🏠", 7575),
]

# Port info for the modals
PORTS_INFO = {
    22: {
        "name": "SSH",
        "icon": "🔐",
        "desc": "Secure remote access to the server.",
        "usage": "Server administration from any computer.",
        "access": "ssh user@<server-ip>",
        "category": "administration",
    },
    3000: {
        "name": "Gitea",
        "icon": "🐊",
        "desc": "Self-hosted Git service.",
        "usage": "Private code repositories, issue tracking, CI.",
        "access": "https://git.<your-domain>.cl",
        "category": "development",
    },
    32400: {
        "name": "Plex",
        "icon": "🎬",
        "desc": "Media streaming server.",
        "usage": "Stream movies and series to any device.",
        "access": "http://<server-ip>:32400/web",
        "category": "media",
    },
    5050: {
        "name": "Cashflow MVP",
        "icon": "💰",
        "desc": "Personal finance management.",
        "usage": "Track income, expenses, and financial goals.",
        "access": "http://<server-ip>:5050",
        "category": "apps",
    },
    5055: {
        "name": "Overseerr",
        "icon": "🍿",
        "desc": "Media request management.",
        "usage": "Request movies and series to be added to the library.",
        "access": "http://<server-ip>:5055",
        "category": "media",
    },
    5057: {
        "name": "Panshulo Dashboard",
        "icon": "📊",
        "desc": "This dashboard — server health monitoring.",
        "usage": "Real-time metrics: CPU, RAM, disk, Docker status.",
        "access": "http://<server-ip>:5057",
        "category": "monitoring",
    },
    6767: {
        "name": "Bazarr",
        "icon": "💬",
        "desc": "Subtitle management.",
        "usage": "Automatically downloads subtitles for your media.",
        "access": "http://<server-ip>:6767",
        "category": "media",
    },
    7575: {
        "name": "Homarr",
        "icon": "🏠",
        "desc": "Unified dashboard for all services.",
        "usage": "Centralized access point for all self-hosted services.",
        "access": "http://<server-ip>:7575",
        "category": "monitoring",
    },
    7878: {
        "name": "Radarr",
        "icon": "🎯",
        "desc": "Movie automation.",
        "usage": "Automatically downloads and organizes movies.",
        "access": "http://<server-ip>:7878",
        "category": "media",
    },
    8080: {
        "name": "Caddy",
        "icon": "🔒",
        "desc": "Reverse proxy with automatic SSL.",
        "usage": "Routes external traffic to internal services with TLS.",
        "access": "https://<your-domain>.cl",
        "category": "infrastructure",
    },
    8085: {
        "name": "qBittorrent",
        "icon": "⚡",
        "desc": "Torrent client.",
        "usage": "Downloads media files via BitTorrent protocol.",
        "access": "http://<server-ip>:8085",
        "category": "media",
    },
    8096: {
        "name": "Jellyfin",
        "icon": "📺",
        "desc": "Open source media system.",
        "usage": "Stream media to any device (open source alternative to Plex).",
        "access": "http://<server-ip>:8096",
        "category": "media",
    },
    8989: {
        "name": "Sonarr",
        "icon": "📡",
        "desc": "Series automation.",
        "usage": "Automatically downloads and organizes TV series.",
        "access": "http://<server-ip>:8989",
        "category": "media",
    },
    9696: {
        "name": "Prowlarr",
        "icon": "🔍",
        "desc": "Indexer manager.",
        "usage": "Centralized search index management for the *arr stack.",
        "access": "http://<server-ip>:9696",
        "category": "media",
    },
}

# Docker containers to display
DOCKER_CONTAINERS = [
    "plex", "jellyfin", "sonarr", "radarr", "bazarr",
    "prowlarr", "qbittorrent", "homarr", "overseerr",
    "tautulli", "gitea", "netdata",
]

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = Flask(__name__)


def get_system_info():
    """Gather system metrics."""
    cpu = psutil.cpu_percent(interval=0.1)
    cpu_freq = psutil.cpu_freq()
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage("/")
    uptime_seconds = int(psutil.boot_time())
    temp = _get_cpu_temp()

    return {
        "cpu": cpu,
        "cpu_freq": round(cpu_freq.current, 0) if cpu_freq else 0,
        "ram_percent": ram.percent,
        "ram_used": ram.used,
        "ram_total": ram.total,
        "swap_percent": swap.percent,
        "disk_percent": disk.percent,
        "disk_used": disk.used,
        "disk_total": disk.total,
        "uptime": uptime_seconds,
        "temp": temp,
    }


def _get_cpu_temp():
    """Attempt to read CPU temperature."""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return round(int(f.read().strip()) / 1000, 1)
    except (FileNotFoundError, ValueError, OSError):
        return None


def check_port(port, timeout=2):
    """Check if a local port is listening."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex(("127.0.0.1", port))
        sock.close()
        return result == 0
    except:
        return False


def check_docker_container(name):
    """Check if a Docker container is running."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", f"name={name}", "--format", "{{.Names}}"],
            capture_output=True, text=True, timeout=5
        )
        return name in result.stdout.strip()
    except:
        return False


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html", refresh=REFRESH_SECONDS)


@app.route("/api/metrics")
def api_metrics():
    system = get_system_info()

    services_status = {}
    for name, url, icon, port in SERVICES:
        services_status[name] = {
            "icon": icon,
            "url": url,
            "online": check_port(port),
        }

    docker_status = {}
    for container in DOCKER_CONTAINERS:
        docker_status[container] = check_docker_container(container)

    return jsonify({
        "system": system,
        "services": services_status,
        "docker": docker_status,
        "ports_info": PORTS_INFO,
    })


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=False)
