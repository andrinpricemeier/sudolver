from fastapi import HTTPException, Depends, Request
from .auth import Authenticator
from .dependencies import authenticator_dependency


def perform_auth(
    req: Request, authenticator: Authenticator = Depends(authenticator_dependency)
) -> None:
    print("Received authentication request.")
    if "x-api-key" not in req.headers:
        print("Authentication failed. API token was missing.")
        raise HTTPException(status_code=401, detail="Authentication failed.")
    user_token: str = req.headers["x-api-key"]
    is_valid = authenticator.authenticate(user_token)
    if not is_valid:
        print("Authentication failed. Wrong API token given.")
        raise HTTPException(status_code=401, detail="Authentication failed.")
    print("Authenticated passed.")
