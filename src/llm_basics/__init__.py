import os

# import time
from dotenv import load_dotenv
from openai import OpenAI

DIM = "\033[2m"      # 变暗（思考区开）
RESET = "\033[0m"    # 恢复默认（思考区关）

def main() -> None:
    load_dotenv()  # ① 读 .env

    api_key = os.getenv("DEEPSEEK_API_KEY")  # ② 从环境变量取 key
    if not api_key:
        raise SystemExit("没找到 DEEPSEEK_API_KEY，检查 .env 文件")

    client = OpenAI(  # ③ 建客户端
        api_key=api_key,
        base_url="https://api.deepseek.com",  # 指向 DeepSeek
    )

    stream = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": "你是一个学习助手，用简洁的中文回答。"},
            {"role": "user", "content": "用一句话介绍你自己，15字以内"},
        ],
        stream=True,  # ← 和之前唯一的区别
    )
    thinking_started = False       # 判断思考标题是否打印
    answer_started = False         # 判断回答标题是否打印
    reason_count = 0               # 计数器
    content_count = 0
    for chunk in stream:
        if not chunk.choices:  # 防御性写法：万一有的块没 choices
            continue
        delta = chunk.choices[0].delta
        rc=getattr(delta,"reasoning_content",None)
        if rc:
            reason_count+=1
            if not thinking_started:
                print(f"{DIM}思考中……\n")
                thinking_started=True
            print(rc, end="", flush=True)
        elif delta.content:
            content_count+=1
            if not answer_started:
                print(f"{RESET}\n\n回答：\n")
                answer_started=True
            print(delta.content, end="", flush=True)

    print(f"{RESET}")
    print(f"思考块数：{reason_count}，回答块数：{content_count}")  
"""
piece = chunk.choices[0].delta.content
if piece:  # None 和空串都跳过
    print(piece, end="", flush=True)
for chunk in stream:
    if not chunk.choices:
        continue
    piece = chunk.choices[0].delta.content
    if piece:
        print(piece, end="", flush=True)
        time.sleep(0.03)        # ← 人工慢放：每块睡 30 毫秒（实验完删掉这行）
"""

  


if __name__ == "__main__":
    main()
