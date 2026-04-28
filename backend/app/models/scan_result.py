from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base

class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String)
    status = Column(String)
    status_code = Column(Integer)
    title = Column(String)
    ip = Column(String)
    server = Column(String)
    content_type = Column(String)
    tech = Column(String)
    redirected = Column(Boolean)
    final_url = Column(String)

    # 🔥 ESTA ES LA CLAVE
    ports = Column(String)
