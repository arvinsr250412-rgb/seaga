import streamlit as st
import json
import requests
import base64

REPO_OWNER = "arvinsr250412-rgb"
REPO_NAME = "seaga"
FILE_PATH = "keys.json"
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")

def _update_github(new_data, sha):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    encoded_content = base64.b64encode(json.dumps(new_data, indent=4).encode('utf-8')).decode('utf-8')
    payload = {"message": "Consume Key", "content": encoded_content, "sha": sha}
    r = requests.put(url, headers=headers, json=payload)
    return r.status_code in [200, 201]

def key_check_gate(test_id):
    if st.session_state.get(f"unlocked_{test_id}", False):
        return True

    # 针对侧边栏设计的紧凑 UI
    u_key = st.text_input("Key", key=f"inp_{test_id}", placeholder="输入8位密钥...", label_visibility="collapsed")
    
    if st.button("立即激活 💥", key=f"btn_act_{test_id}", use_container_width=True):
        if not u_key:
            st.warning("请输入密钥")
            st.stop()
            
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        res = requests.get(url, headers=headers)
        
        if res.status_code == 200:
            data = res.json()
            db = json.loads(base64.b64decode(data['content']).decode('utf-8'))
            sha = data['sha']
            
            target = u_key.upper().strip()
            if target in db and db[target] > 0:
                db[target] -= 1
                if _update_github(db, sha):
                    st.session_state[f"unlocked_{test_id}"] = True
                    st.success("激活成功！")
                    st.rerun()
            else:
                st.error("密钥无效或额度不足")
        else:
            st.error("连接 Github 失败")
    
    st.stop() # 必须拦截，防止未输入密钥就运行测试代码
