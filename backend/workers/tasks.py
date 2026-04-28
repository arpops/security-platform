from .celery_app import celery
import socket
import requests

from app.db.database import SessionLocal
from app.models.scan_result import ScanResult

# DNS
@celery.task
def dns_task(domain):
    try:
        ip = socket.gethostbyname(domain)
        return {"domain": domain, "ip": ip}
    except:
        return {"domain": domain, "ip": None}

# HTTP
@celery.task
def http_task(data):
    domain = data["domain"]

    try:
        response = requests.get(f"http://{domain}", timeout=5)

        title = None
        if "<title>" in response.text:
            title = response.text.split("<title>")[1].split("</title>")[0]

        data.update({
            "status": "up",
            "status_code": response.status_code,
            "title": title,
            "final_url": str(response.url),
            "redirected": len(response.history) > 0
        })

    except:
        data.update({
            "status": "down",
            "status_code": None
        })

    return data

# PORT SCAN
def scan_ports(domain):
    common_ports = [22, 80, 443, 3306, 8080]
    open_ports = []

    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)

            if sock.connect_ex((domain, port)) == 0:
                open_ports.append(port)

            sock.close()
        except:
            pass

    return ",".join(map(str, open_ports)) if open_ports else None

# HEADERS + SAVE
@celery.task
def header_task(data):
    domain = data["domain"]

    try:
        response = requests.get(f"http://{domain}", timeout=5)

        server = response.headers.get("Server")
        content_type = response.headers.get("Content-Type")

        tech = None
        if server:
            if "nginx" in server.lower():
                tech = "nginx"
            elif "apache" in server.lower():
                tech = "apache"
            else:
                tech = server

        ports = scan_ports(domain)

        data.update({
            "server": server,
            "content_type": content_type,
            "tech": tech,
            "ports": ports
        })

    except:
        pass

    # 🔥 GUARDAR EN DB
    db = SessionLocal()

    new_result = ScanResult(
        domain=data.get("domain"),
        status=data.get("status"),
        status_code=data.get("status_code"),
        title=data.get("title"),
        ip=data.get("ip"),
        server=data.get("server"),
        content_type=data.get("content_type"),
        tech=data.get("tech"),
        redirected=data.get("redirected"),
        final_url=data.get("final_url"),
        ports=data.get("ports")
    )

    db.add(new_result)
    db.commit()
    db.close()

    return data
