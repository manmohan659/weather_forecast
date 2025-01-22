from supabase import create_client
from app.core.config import settings #import from config

SUPABASE_URL = settings.SUPABASE_URL # use settings.
SUPABASE_KEY = settings.SUPABASE_KEY # use settings.

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)