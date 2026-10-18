import psycopg
from config.settings import settings
def get_post_gres_connection():
    return psycopg.connect(
        host = settings.post_gres_host,
        port = settings.post_gres_port,
        dbname = settings.post_gres_dbname,
        user=settings.post_gres_user,
        password=settings.post_gres_password
    )
