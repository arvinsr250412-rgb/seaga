import streamlit as st
import json
import requests
import base64

# --- 1. 基础配置 (请确保 secrets.toml 中已配置 GITHUB_TOKEN) ---
REPO_OWNER = "arvinsr250412-rgb"
REPO_NAME = "seaga"
FILE_PATH = "keys.json"
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")

def _update_github(new_data, sha):
    """私有辅助函数：将更新后的数据写回 GitHub"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 将字典转为格式化的 JSON 字符串并进行 Base64 编码
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
    """
    密钥验证门禁函数
    :param test_id: 测试项目的唯一标识符 (如 "SoulCity")
    :return: 验证成功返回 True，否则返回 False 或拦截运行
    """
    # 如果该项目在本次会话中已解锁，直接放行
    if st.session_state.get(f"unlocked_{test_id}", False):
        return True

    # --- 侧边栏紧凑型验证 UI ---
    st.markdown("---")
    # 使用无 Label 模式让界面更干净
    u_key = st.text_input(
        "输入激活码", 
        key=f"input_field_{test_id}", 
        placeholder="输入8位密钥...", 
        label_visibility="collapsed"
    )
    
    # 按钮使用 use_container_width 填满侧边栏宽度
    if st.button("立即解锁项目 💥", key=f"verify_btn_{test_id}", use_container_width=True):
        if not u_key:
            st.warning("请先输入密钥哦~")
            st.stop()
            
        # 1. 从 GitHub 获取当前密钥库
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                data = res.json()
                # 解码 GitHub 上的 Base64 内容
                db = json.loads(base64.b64decode(data['content']).decode('utf-8'))
                sha = data['sha']
                
                # 2. 验证密钥是否存在且额度充足
                target = u_key.upper().strip()
                if target in db and db[target] > 0:
                    # 3. 扣除额度并同步到云端
                    db[target] -= 1
                    if _update_github(db, sha):
                        # 4. 记录解锁状态到 Session State
                        st.session_state[f"unlocked_{test_id}"] = True
                        st.success("激活成功！正在进入...")
                        st.rerun() # 重新运行以刷新主界面
                    else:
                        st.error("云端同步失败，请检查网络")
                else:
                    st.error("密钥无效或已失效 🔒")
            else:
                st.error(f"无法连接密钥中心 (Code: {res.status_code})")
        except Exception as e:
            st.error(f"系统错误: {str(e)}")
    
    # 只有点击按钮验证成功后才会执行 rerun，否则会在此处截断，不让主程序往下走
    st.stop()
