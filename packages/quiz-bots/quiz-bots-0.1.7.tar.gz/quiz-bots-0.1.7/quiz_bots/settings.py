from environs import Env

env = Env()
env.read_env()

tg_token = env.str('TELEGRAM_TOKEN')
db_endpoint = env.str('DB_ENDPOINT')
db_password = env.str('DB_PASSWORD')
vk_group_token = env.str('VK_GROUP_TOKEN')
