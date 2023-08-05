from environs import Env

env = Env()
env.read_env()

TG_TOKEN = env.str('TELEGRAM_TOKEN')
DB_ENDPOINT = env.str('DB_ENDPOINT')
DB_PASSWORD = env.str('DB_PASSWORD')
VK_GROUP_TOKEN = env.str('VK_GROUP_TOKEN')
VK_GROUP_ID = env.int('VK_GROUP_ID')
