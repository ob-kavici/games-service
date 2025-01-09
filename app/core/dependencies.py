from supabase import create_client, Client
from core.config import settings
from fastapi import HTTPException

def get_supabase_client(auth: dict = None) -> Client:
    """
    Instantiates a Supabase client and optionally sets the session 
    for authenticated requests.
    
    Args:
        auth (dict, optional): A dictionary containing 'jwt' and 'refresh_token'.

    Returns:
        Client: The Supabase client with or without an authenticated session.
    """
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    # Set the session if auth is provided
    if auth:
        jwt = auth.get("jwt")
        refresh_token = auth.get("refresh_token")

        if not jwt:
            raise HTTPException(status_code=400, detail="Missing JWT in authentication.")
        if not refresh_token:
            raise HTTPException(status_code=400, detail="Missing Refresh Token in authentication.")

        try:
            supabase.auth.set_session(jwt, refresh_token)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to set session: {e}")
    
    return supabase
