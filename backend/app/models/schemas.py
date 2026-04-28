from pydantic import BaseModel

class TargetCreate(BaseModel):
    domains: list[str]

class ScanResultResponse(BaseModel):
    domain: str
    status: str | None
    status_code: int | None
    title: str | None
    ip: str | None
    server: str | None
    content_type: str | None
    tech: str | None
    redirected: bool | None
    final_url: str | None
    ports: str | None

    class Config:
        from_attributes = True
