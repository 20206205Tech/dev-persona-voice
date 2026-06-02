import os

from environs import Env
from loguru import logger

env = Env()
logger.info("Loading environment variables...")


ENVIRONMENT = env.str("ENVIRONMENT", "production")
RELOAD = True if ENVIRONMENT == "development" else False


SERVICE_NAME = "code-chatbot-service"
PORT = env.int("SERVICE_PORT", 52001)
HOST = "0.0.0.0"


DATA_PIPELINE_VBPLNEW_DATABASE_URL = env.str("DATA_PIPELINE_VBPLNEW_DATABASE_URL")
MICROSERVICE_CHAT_HISTORY_DATABASE_URL = env.str(
    "MICROSERVICE_CHAT_HISTORY_DATABASE_URL"
)
MICROSERVICE_CHATBOT_SERVICE_DATABASE_URL = env.str(
    "MICROSERVICE_CHATBOT_SERVICE_DATABASE_URL"
)
DATABASE_URL = MICROSERVICE_CHATBOT_SERVICE_DATABASE_URL


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


PATH_FILE_ENV = os.path.abspath(__file__)
PATH_FOLDER_PROJECT = os.path.dirname(PATH_FILE_ENV)
PATH_FOLDER_DATA = os.path.join(PATH_FOLDER_PROJECT, "data")
PATH_FOLDER_DOCS = os.path.join(PATH_FOLDER_PROJECT, "docs")


if not os.path.exists(PATH_FOLDER_DATA):
    os.makedirs(PATH_FOLDER_DATA)

if not os.path.exists(PATH_FOLDER_DOCS):
    os.makedirs(PATH_FOLDER_DOCS)


os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "project-chatbot-by-terraform"
# os.environ["LANGCHAIN_TRACING_V2"] = "false"
# os.environ["LANGSMITH_TRACING"] = "false"


NVIDIA_API_KEY = env.str("NVIDIA_API_KEY")


PINECONE_API_KEY = env.str("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "dev-vbplnew" if ENVIRONMENT == "development" else "prod-vbplnew"

if ENVIRONMENT == "development":
    PINECONE_INDEX_NAME = "prod-vbplnew"


QDRANT_URL = env.str("QDRANT_URL")
QDRANT_API_KEY = env.str("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = (
    "dev_phap_dien_vectors"
    if ENVIRONMENT == "development"
    else "prod_phap_dien_vectors"
)


if ENVIRONMENT == "development":
    QDRANT_COLLECTION_NAME = "prod_phap_dien_vectors"


MILVUS_URI = env.str("MILVUS_URI")
MILVUS_TOKEN = env.str("MILVUS_TOKEN")
USER_DOCUMENTS_COLLECTION_NAME = (
    "dev_user_documents" if ENVIRONMENT == "development" else "prod_user_documents"
)


THRESHOLD_RETRIEVE = 0.5
THRESHOLD_RETRIEVE = 0.4

MAX_REWRITE_COUNT = 2
MAX_MESSAGES_BEFORE_SUMMARY = 5


JINA_API_KEY = env.str("JINA_API_KEY")


TAVILY_API_KEY = env.str("TAVILY_API_KEY")


LIVEKIT_URL = env.str("LIVEKIT_URL")
LIVEKIT_API_KEY = env.str("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = env.str("LIVEKIT_API_SECRET")
os.environ["LIVEKIT_AGENT_TELEMETRY"] = "false"

GROQ_API_KEY = env.str("GROQ_API_KEY")


RABBITMQ_URL = (
    "amqp://admin:secret123@rabbitmq-queue:5672"
    if ENVIRONMENT == "production"
    else "amqp://admin:secret123@localhost:5672"
)


CLOUDFLARE_ACCOUNT_ID = env.str("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = env.str("CLOUDFLARE_API_TOKEN")


R2_ACCESS_KEY_ID = env.str("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = env.str("R2_SECRET_ACCESS_KEY")
R2_ACCOUNT_ID = CLOUDFLARE_ACCOUNT_ID
R2_ENDPOINT_URL = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
R2_BUCKET_NAME = "dev-share" if ENVIRONMENT == "development" else "prod-share"
R2_PUBLIC_DOMAIN = (
    "https://dev-share.20206205.tech"
    if ENVIRONMENT == "development"
    else "https://prod-share.20206205.tech"
)


HONEYCOMB_API_KEY = env.str("HONEYCOMB_API_KEY")


OLLAMA_URL = "http://localhost:11434"


# REDIS_URL = env.str("REDIS_URL")


PERSONA_URL = (
    "http://localhost:52003"
    if ENVIRONMENT == "development"
    else "http://code-persona-service:80"
)
PERSONA_API_KEY = env.str("PERSONA_API_KEY")


TTS_BASE_URL = f"{PERSONA_URL}/code-persona-service/audio/v1"
TTS_API_KEY = PERSONA_API_KEY


TTS_MODEL = env.str("TTS_MODEL", "tts-1")


FIRST_MESSAGE = "Bạn đợi một chút nhé, tôi đang tìm kiếm thông tin tài liệu"


WELCOME_MESSAGE = "Xin chào, tôi là trợ lý pháp luật. Bạn có cần tôi giúp đỡ gì không?"
REJOIN_MESSAGE = "Chào mừng bạn đã quay trở lại. Bạn có cần tôi giúp đỡ gì không?"


OLLAMA_API_KEY = env.str("OLLAMA_API_KEY")

# OPENROUTER_API_KEY = env.str("OPENROUTER_API_KEY")
# QWEN_API_KEY = env.str("QWEN_API_KEY")


TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN")
TELEGRAM_GROUP_CHAT_ID = env.str("TELEGRAM_GROUP_CHAT_ID", "-5156220357")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


DEEPGRAM_API_KEY = env.str("DEEPGRAM_API_KEY")
