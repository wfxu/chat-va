import openai, os, logging
openai.api_key = os.getenv("OPENAI_API_KEY")

# 配置日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 创建一个控制台处理器，将日志信息输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 定义日志信息格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# 将处理器添加到记录器
logger.addHandler(console_handler)

def openai_chat(messages_list):
    max_retries = 10
    for i in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages_list,
            )
            if response:
                break
        except (openai.error.APIConnectionError, ConnectionAbortedError):
            print(i + 1, "connection error")
            logger.info(f"{i + 1} connection error")
            continue
    if not response:
        result = '没有返回结果'
    else:
        result = f"{i+1 if i > 0 else ''}" + response["choices"][0]["message"]["content"]
    
    return result