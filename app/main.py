from fastapi import FastAPI,HTTPException
from fastapi.responses import RedirectResponse
from .Req_Res_Schemas import URLReq
from .sqlCrud import addShortUrl,get_url_by_short
app = FastAPI();

@app.post("/shorten")
def shorten_url(request:URLReq):
    if not request.long_url:
        raise HTTPException(status_code=404, detail="long_url required")
    short_url = addShortUrl(request.long_url)
    return {"shorten _url" : f"http://localhost:8000/{short_url}"}
    return {"message": "basic api"}


@app.get("/{short_code}")
def redirect_to_long_url(short_code:str):
    long_url = get_url_by_short(short_code)
    if long_url:
        return RedirectResponse(url=long_url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")
