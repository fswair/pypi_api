from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import user_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def retrieve_url(url: str, headers: dict = {}):
    """
    This function retrieves the content from the given URL.
    """
    import aiohttp
    async with aiohttp.ClientSession() as session:
        _headers = {
            "Host": "pypi.org",
            "Sec-Ch-Ua": "\"Not:A-Brand\";v=\"24\", \"Chromium\";v=\"134\"",
            "User-Agent": user_agent.generate_user_agent(),
            "Sec-Ch-Ua-Mobile": "?0",
            "Accept": "application/json",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://pypi.org",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=1, i"
        }
        
        headers = {**_headers, **(headers or {})}
        
        async with session.get(url, headers=headers, ssl=False) as response:
            if response.status != 200:
                raise Exception({"error": "Failed to retrieve content from the URL"})
            return await response.json()

@app.get("/get_package")
async def get_product(package: str, version: str = None):
    """
    This endpoint receives a product name and returns a response.
    """
    package = package if not version else f"{package}/{version}"
    package_url = f"https://pypi.org/pypi/{package}/json"
    return  {"url": package_url, "data":await retrieve_url(package_url)}

@app.get("/get_package_binaries")
async def get_package_binaries(package: str):
    """
    This endpoint receives a package name and returns a response.
    """
    url = f"https://pypi.org/simple/{package}/"

    return {"url": url, "data": await retrieve_url(url, {"Accept": "application/vnd.pypi.simple.v1+json"})}

@app.get("/get_pypi_stats")
async def get_pypi_stats():
    """
    This endpoint receives a package name and returns a response.
    """
    url = f"https://pypi.org/stats"
    return {"url": url, "data": await retrieve_url(url)}