from pydantic import BaseModel

class CheckRequest(BaseModel):
    tenant_id: str
    api_key: str
    resource: str
    