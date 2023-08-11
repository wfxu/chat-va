import openai, os, logging
import tiktoken

def num_tokens_from_string(string: str, encoding_name='cl100k_base') -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

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
    max_tokens = 8192
    response = ''
    
    total_token = sum([len(message['content']) for message in messages_list])
    n = 0
    while total_token > max_tokens:
        if len(messages_list) == 0:
            break
        n += 1
        messages_list.pop(0)
        total_token = sum([len(message['content']) for message in messages_list])

    for i in range(max_retries):
        if len(messages_list) == 0:
            break
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=messages_list,
            )
            if response:
                break
        except openai.error.InvalidRequestError:
            n += 1
            messages_list.pop(0)
            logger.info(f"{n} delete conversation")
        except (openai.error.APIConnectionError, ConnectionAbortedError):
            print(i + 1, "connection error")
            logger.info(f"{i + 1} connection error")
            continue
        except:
            logger.info("unknown error")
            continue
    if not response:
        result = '没有返回结果'
    else:
        result = ('' if i <= 0 else f"<em>请求尝试了 {i+1} 次</em><br>") + ('' if n <= 0 else f"<em>删除了 {n} 个对话</em><br>") + response["choices"][0]["message"]["content"]
    
    return result