import streamlit as st
import time

# 使用 st.set_page_config() 来设置页面的宽度和其他布局选项。
st.set_page_config(layout="wide")

if "role" not in st.session_state:
    st.session_state.role = None

# 角色列表：定义用户的角色，包含 None 和不同的角色名。
# 不同的用户进入权限不同
# ROLES = [None, "Relog","Upload","Requester", "Responder", "Admin"]
ROLES = [None, "Admin", "Clerk"]

def login():

    st.header("Log in")
    # role = st.selectbox("Choose your role", ROLES)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log in"):
        if username == "123" and password == "123":
            st.session_state.role = "Admin"
            st.toast("Admin Login successful!")
            st.rerun()
        elif username == "456" and password == "456":
            st.session_state.role = "Clerk"
            st.toast("Clerk login successful!")
            st.rerun()
        else:
            st.session_state.role = None
            st.toast('The user name or password is wrong, please try again.', icon="⚠️")
            st.rerun()

def logout():
    st.session_state.role = None
    st.rerun()

role = st.session_state.role

# 使用 st.Page 创建多个页面，包括登出、设置、上传等，每个页面都有标题和图标。
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("UI/settings.py", title="Settings", icon=":material/settings:")

member_overview = st.Page(
    "UI/all_member/member_overview.py",
    title="Overview",
    icon=":material/database:", 
)
member_analysis = st.Page(
    "UI/all_member/member_analysis.py", 
    title="Analysis", 
    icon=":material/leaderboard:",
    default=(role == "Admin"),
)
a_upload = st.Page(
    "UI/a_upload/upload.py",
    title="Upload Files",
    icon=":material/upload_file:",
)
a_show_data = st.Page(
    "UI/a_upload/show_data.py",
    title="View Files",
    icon=":material/task:",
)
c_upload = st.Page(
    "UI/c_upload/upload.py",
    title="Upload Files",
    icon=":material/upload_file:",
    default=(role == "Clerk"),
)
c_show_data = st.Page(
    "UI/c_upload/show_data.py",
    title="View Files",
    icon=":material/task:",
)
svip = st.Page(
    "UI/consumer_insight/svip.py",
    title="SVIP Recommendation",
    icon=":material/stars:",
)
# lever_analysis = st.Page(
#     "consumer_insight/lever_analysis.py",
#     title="Level Analysis",
#     icon=":material/monitoring:",
# )
# product_recommendations = st.Page(
#     "consumer_insight/product_recommendations.py",
#     title="Product Recommendation",
#     icon=":material/monitoring:",
# )
inventory = st.Page(
    "UI/brand/inventory.py",
    title="Procurement Recommendation",
    icon=":material/inventory:",
)

# 根据角色构建页面字典：根据当前角色添加相应的页面到 page_dict，以便在侧边栏中显示。
account_pages = [logout_page, settings]
a_upload_pages = [a_upload, a_show_data]
c_upload_pages = [c_upload, c_show_data]
allmember_pages = [member_overview, member_analysis]
insight_pages = [svip]
brand_pages = [inventory]

# st.title("XSell")
st.logo("UI/images/horizontal_blue.png", icon_image="UI/images/icon_blue.png")

# 按照希望的顺序排列页面组
page_dict = {}
if st.session_state.role in ["Admin"]:
    page_dict["File Operations"] = a_upload_pages
if st.session_state.role in ["Clerk"]:
    page_dict["File Operations"] = c_upload_pages
if st.session_state.role == "Admin":
    page_dict["All Current Members"] = allmember_pages
if st.session_state.role in ["Clerk", "Admin"]:
    page_dict["Consumer Insight"] = insight_pages
    page_dict["Brand Insight"] = brand_pages

# 如果 page_dict 有页面，创建导航菜单；如果没有，则显示登录页面。
if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

# 启动应用
pg.run()