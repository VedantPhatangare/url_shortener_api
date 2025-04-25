from pydantic import BaseModel

class URLReq(BaseModel):
    long_url: str