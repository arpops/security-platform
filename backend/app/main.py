from fastapi import FastAPI, Depends, Body
from sqlalchemy.orm import Session
from celery import chain

from app.db.database import engine, Base, SessionLocal
from app.models import target, scan_result
from app.models.target import Target
from app.models.schemas import TargetCreate, ScanResultResponse

from workers.tasks import dns_task, http_task, header_task

app = FastAPI(
    title="Security Scanner API",
    description="""
API para analizar dominios de forma sencilla.

### Cómo usar:
1. Ve a **🔍 Analizar dominios**
2. Introduce dominios (ej: google.com)
3. Ejecuta
4. Ve a **📊 Ver resultados**

El sistema analiza:
- DNS
- HTTP/HTTPS
- Tecnologías
- Puertos abiertos
""",
    version="1.0"
)

Base.metadata.create_all(bind=engine)

# DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ROOT
@app.get(
    "/",
    summary="🟢 Estado de la API",
    description="Comprueba que la API está funcionando"
)
def root():
    return {"message": "Security Platform running"}

# 🔥 MULTI TARGET
@app.post(
    "/targets",
    summary="🔍 Analizar uno o varios dominios",
    description="Permite analizar múltiples dominios a la vez"
)
def create_targets(
    target: TargetCreate = Body(
        example={"domains": ["google.com", "github.com"]}
    ),
    db: Session = Depends(get_db)
):
    results = []

    for domain in target.domains:

        existing = db.query(Target).filter(Target.domain == domain).first()

        if existing:
            results.append({"domain": domain, "status": "exists"})
            continue

        new_target = Target(domain=domain)
        db.add(new_target)
        db.commit()
        db.refresh(new_target)

        # lanzar pipeline
        chain(
            dns_task.s(domain),
            http_task.s(),
            header_task.s()
        ).apply_async()

        results.append({"domain": domain, "status": "created"})

    return {"results": results}

# RESULTADOS
@app.get(
    "/results",
    response_model=list[ScanResultResponse],
    summary="📊 Ver resultados del análisis",
    description="Obtiene todos los resultados o filtra por dominio"
)
def get_results(domain: str = None, db: Session = Depends(get_db)):
    query = db.query(scan_result.ScanResult)

    if domain:
        query = query.filter(scan_result.ScanResult.domain == domain)

    return query.all()
