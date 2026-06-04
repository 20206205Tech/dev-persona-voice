import os

from environs import Env
from loguru import logger

env = Env()
logger.info("Loading environment variables...")


ENVIRONMENT = env.str("ENVIRONMENT", "production")
RELOAD = True if ENVIRONMENT == "development" else False


SERVICE_NAME = "code-persona-service"
PORT = env.int("SERVICE_PORT", 52003)
HOST = "0.0.0.0"


MICROSERVICE_PERSONA_SERVICE_DATABASE_URL = env.str(
    "MICROSERVICE_PERSONA_SERVICE_DATABASE_URL"
)
DATABASE_URL = MICROSERVICE_PERSONA_SERVICE_DATABASE_URL


SUPABASE_PROJECT_ID = env.str("SUPABASE_PROJECT_ID")
SUPABASE_URL = f"https://{SUPABASE_PROJECT_ID}.supabase.co"
JWKS_URL = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"
ISSUER = f"{SUPABASE_URL}/auth/v1"
AUDIENCE = "authenticated"


DESCRIPTION = f"""
# Chào mừng đến với {SERVICE_NAME} ({ENVIRONMENT})

* [Đăng nhập Google](https://{SUPABASE_PROJECT_ID}.supabase.co/auth/v1/authorize?provider=google&redirect_to=https://20206205tech.github.io/auth-callback)
* [Database](https://console.neon.tech/app/org-still-feather-82034197/projects?q={SERVICE_NAME})
* [Local](http://localhost:{PORT})
* [Dev](https://dev-{SERVICE_NAME}.20206205.tech)
* [docs](http://localhost:{PORT}/{SERVICE_NAME}/docs)
* [redoc](http://localhost:{PORT}/{SERVICE_NAME}/redoc)
* [voyager](http://localhost:{PORT}/{SERVICE_NAME}/voyager)
* [scalar](http://localhost:{PORT}/{SERVICE_NAME}/scalar)

""".strip()


logger.success(f"DESCRIPTION: \n{DESCRIPTION}")


HONEYCOMB_API_KEY = env.str("HONEYCOMB_API_KEY")


PERSONA_API_KEY = env.str("PERSONA_API_KEY")


SUPABASE_SERVICE_ROLE_KEY = env.str("SUPABASE_SERVICE_ROLE_KEY")


PERSONA_AVATARS_BUCKET = "persona_avatars"
ALLOWED_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]


PERSONA_AUDIOS_BUCKET = "persona_audios"
ALLOWED_AUDIO_EXTENSIONS = ["mp3", "wav", "ogg"]


REDIS_URL = env.str("REDIS_URL")


if ENVIRONMENT == "production":
    REDIS_URL = "redis://:secret123@redis-persona:6379"

CACHE_EXPIRE = 60 * 60 * 24  # 60 giây * 60 phút * 24 giờ
CACHE_KEY = f"persona:dev" if ENVIRONMENT == "development" else "persona:prod"


PATH_FILE_ENV = os.path.abspath(__file__)
PATH_FOLDER_PROJECT = os.path.dirname(PATH_FILE_ENV)
PATH_FOLDER_DATA = os.path.join(PATH_FOLDER_PROJECT, "data")
PATH_FOLDER_DOCS = os.path.join(PATH_FOLDER_PROJECT, "docs")
PATH_FOLDER_AVATAR = os.path.join(PATH_FOLDER_DATA, "avatar")
PATH_FOLDER_AUDIO_CACHE = os.path.join(PATH_FOLDER_DATA, "storage", "audio_cache")
PATH_FOLDER_DISKCACHE = os.path.join(PATH_FOLDER_DATA, "storage", "diskcache")
DISKCACHE_SIZE_LIMIT = env.int("DISKCACHE_SIZE_LIMIT", 1 * 1024 * 1024 * 1024)


if not os.path.exists(PATH_FOLDER_DATA):
    os.makedirs(PATH_FOLDER_DATA)

if not os.path.exists(PATH_FOLDER_DOCS):
    os.makedirs(PATH_FOLDER_DOCS)

if not os.path.exists(PATH_FOLDER_AVATAR):
    os.makedirs(PATH_FOLDER_AVATAR)

if not os.path.exists(PATH_FOLDER_AUDIO_CACHE):
    os.makedirs(PATH_FOLDER_AUDIO_CACHE)

if not os.path.exists(PATH_FOLDER_DISKCACHE):
    os.makedirs(PATH_FOLDER_DISKCACHE)


CLOUDFLARE_ACCOUNT_ID = env.str("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = env.str("CLOUDFLARE_API_TOKEN")


R2_ACCESS_KEY_ID = env.str("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = env.str("R2_SECRET_ACCESS_KEY")
R2_ACCOUNT_ID = CLOUDFLARE_ACCOUNT_ID
R2_ENDPOINT_URL = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
R2_BUCKET_NAME = "dev-share" if ENVIRONMENT == "development" else "prod-share"
R2_PUBLIC_DOMAIN = (
    "https://dev-persona.20206205.tech"
    if ENVIRONMENT == "development"
    else "https://prod-persona.20206205.tech"
)


ELEVENLABS_API_KEY = env.str("ELEVENLABS_API_KEY")
