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
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    json_str = json.dumps(new_data, indent=4)
    encoded_content = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    payload = {
        "message": "🔑 Spectrum: 密钥额度自动扣减",
        "content": encoded_content,
        "sha": sha
    }
    r = requests.put(url, headers=headers, json=payload)
    return r.status_code in [200, 201]

def key_check_gate(test_id):
    # 已解锁直接放行
    # --- 新增：管理员特权通道 ---
    if st.session_state.get("admin_logged_in", False):
        return True  # 直接返回 True，视为验证通过，不渲染任何输入框

    st.markdown("---")
    u_key = st.text_input(
        "输入激活码", 
        key=f"input_field_{test_id}", 
        placeholder="输入8位密钥...", 
        label_visibility="collapsed"
    )
    
    if st.button("立即解锁项目 💥", key=f"verify_btn_{test_id}", use_container_width=True):
        if not u_key:
            st.warning("请先输入密钥哦~")
            return False # 替换了原来的 st.stop()
            
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                data = res.json()
                db = json.loads(base64.b64decode(data['content']).decode('utf-8'))
                sha = data['sha']
                
                target = u_key.upper().strip()
                if target in db and db[target] > 0:
                    db[target] -= 1
                    if _update_github(db, sha):
                        # --- 核心修复：直接在这里改变目标页面 ---
                        st.session_state[f"unlocked_{test_id}"] = True
                        st.session_state.target_page = test_id  # 自动跳转到测试页
                        st.session_state.needs_auth = None      # 关闭验证框
                        st.success("激活成功！正在进入...")
                        st.rerun()
                    else:
                        st.error("云端同步失败，请检查网络")
                else:
                    st.error("密钥无效或已失效 🔒")
            else:
                st.error(f"无法连接密钥中心 (Code: {res.status_code})")
        except Exception as e:
            st.error(f"系统错误: {str(e)}")
    
    return False # 替换了原来的 st.stop()，让主页保持显示
