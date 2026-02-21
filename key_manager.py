import streamlit as st
import json
import requests
import base64

# 从主程序 secrets 中获取配置（或者你也可以在这里定义）
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
REPO_OWNER = "arvinsr250412-rgb"
REPO_NAME = "seaga"
FILE_PATH = "keys.json"

def get_keys_from_github():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            content = r.json()
            return json.loads(base64.b64decode(content['content']).decode('utf-8')), content['sha']
    except Exception as e:
        print(f"Error fetching keys: {e}")
    return {}, None

def update_keys_to_github(new_data, sha=None):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    encoded_content = base64.b64encode(json.dumps(new_data, indent=4).encode('utf-8')).decode('utf-8')
    payload = {"message": "Update keys via System", "content": encoded_content}
    if sha: payload["sha"] = sha
    r = requests.put(url, headers=headers, json=payload)
    return r.status_code in [200, 201]

def verify_and_consume(input_key):
    """
    供测试页面调用的核心接口
    返回: (bool, message)
    """
    input_key = input_key.upper().strip()
    db, sha = get_keys_from_github()
    
    if input_key in db:
        if db[input_key] > 0:
            db[input_key] -= 1
            if update_keys_to_github(db, sha):
                return True, "密钥验证成功！"
            return False, "网络拥堵，请重试"
        return False, "密钥次数已耗尽"
    return False, "无效的密钥"
