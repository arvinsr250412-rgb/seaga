import streamlit as st
import json
import requests
import base64

# --- 配置信息 ---
REPO_OWNER = "arvinsr250412-rgb"
REPO_NAME = "seaga"
FILE_PATH = "keys.json"
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")

def _update_github(new_data, sha):
    """内部函数：同步数据到 GitHub"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    encoded_content = base64.b64encode(json.dumps(new_data, indent=4).encode('utf-8')).decode('utf-8')
    payload = {"message": "Consume Key", "content": encoded_content, "sha": sha}
    r = requests.put(url, headers=headers, json=payload)
    return r.status_code in [200, 201]

def key_check_gate(test_id):
    """
    只需调用此函数即可开启门禁
    test_id: 每个测试唯一的名称，例如 'mbti_test'
    """
    # 1. 管理员免检
    if st.session_state.get('admin_logged_in', False):
        return True

    # 2. 检查当前测试是否已解锁
    state_key = f"unlocked_{test_id}"
    if st.session_state.get(state_key, False):
        return True

    # 3. 未解锁时显示的 UI 界面
    st.markdown(f"""
        <div style="padding: 10px; border-radius: 15px; background: white; border: 2px solid #FFE4E9; text-align: center;">
            <p style="color: #FF512F; font-weight: bold; margin-bottom: 5px;">请输入密钥</p>
        </div>
    """, unsafe_allow_html=True)
  

    # 输入框和按钮
    col1, col2 = st.columns([3, 1])
    with col1:
        u_key = st.text_input("请输入密钥", key=f"input_{test_id}", label_visibility="collapsed", placeholder="输入 8 位密钥...")
    with col2:
        if st.button("激活 💥", key=f"btn_{test_id}", use_container_width=True):
            if not u_key:
                st.warning("请填入密钥")
                return False
            
            # 执行校验逻辑
            url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
            headers = {"Authorization": f"token {GITHUB_TOKEN}"}
            res = requests.get(url, headers=headers)
            
            if res.status_code == 200:
                data = res.json()
                db = json.loads(base64.b64decode(data['content']).decode('utf-8'))
                sha = data['sha']
                
                target_key = u_key.upper().strip()
                if target_key in db and db[target_key] > 0:
                    db[target_key] -= 1
                    if _update_github(db, sha):
                        st.session_state[state_key] = True
                        st.success("激活成功！")
                        st.rerun()
                    else:
                        st.error("同步失败，请重试")
                else:
                    st.error("密钥无效或次数已用完")
            else:
                st.error("无法连接云端数据库")
    
    # 核心拦截：未通过验证则停止运行后续代码
    st.stop()
