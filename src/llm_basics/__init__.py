import os

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    load_dotenv()                                  # ① 读 .env

    api_key = os.getenv("DEEPSEEK_API_KEY")        # ② 从环境变量取 key
    if not api_key:
        raise SystemExit("没找到 DEEPSEEK_API_KEY，检查 .env 文件")

    client = OpenAI(                               # ③ 建客户端
        api_key=api_key,
        base_url="https://api.deepseek.com",       # 指向 DeepSeek
    )

    resp = client.chat.completions.create(         # ④ 发请求
        model="deepseek-flash",
        messages=[
            {"role": "user", "content": "我叫小明"},
            {"role": "assistant", "content": "你好小明！有什么可以帮你的？"},
            {"role": "user", "content": "我叫什么名字？"},
        ],
    )

    print("=== 完整响应 ===")
    print(resp)
    print("=== 就这一行 ===")
    print(resp.choices[0].message.content)         # ⑤ 取回复


if __name__ == "__main__":
    main()