import os
import random
from dotenv import find_dotenv, load_dotenv

env = load_dotenv(find_dotenv())


class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    MYSQL = dict(
        MYSQL_HOST=os.environ.get("MYSQL_HOST", "127.0.0.1"),
        MYSQL_PORT=int(os.environ.get("MYSQL_PORT", 3306)),
        MYSQL_USER=os.environ.get("MYSQL_USER", "root"),
        MYSQL_PASSWORD=os.environ.get("MYSQL_PASSWORD")
    )
    ls = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"]
    HEADERS = {
        "User-Agent": random.choice(ls)
    }



class DevelopmentConfig(Config):
    DEBUG = True
    TABLE = "so"


class TestingConfig:
    TESTING = True
    TABLE = "test"


config = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "default": DevelopmentConfig
}
