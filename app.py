import streamlit as st
import time

st.set_page_config(layout="wide")

if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Admin", "Clerk"]

def login():

    st.title("Xsell")

    username = st.text_input(" Username")
    password = st.text_input(" Password", type="password")

    if st.button("Log In"):
        if username == "admin" and password == "123456":
            st.session_state.role = "Admin"
            st.success("Admin Login successful!", icon="🎉")
            time.sleep(2)
            st.rerun()
        elif username == "clerk" and password == "123456":
            st.session_state.role = "Clerk"
            st.success("Clerk login successful!", icon="🎉")
            time.sleep(2)
            st.rerun()
        else:
            st.session_state.role = None
            st.error('The user name or password is wrong, please try again.', icon="⚠️")
            time.sleep(2)
            st.rerun()

def logout():
    st.session_state.role = None
    st.rerun()

role = st.session_state.role

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
a_show = st.Page(
    "UI/a_upload/show.py",
    title="View Files",
    icon=":material/task:",
)
a_delete = st.Page(
    "UI/a_upload/delete.py",
    title="Delete Files",
    icon=":material/scan_delete:",
)
c_upload = st.Page(
    "UI/c_upload/upload.py",
    title="Upload Files",
    icon=":material/upload_file:",
)
c_show = st.Page(
    "UI/c_upload/show.py",
    title="View Files",
    icon=":material/task:",
)
c_delete = st.Page(
    "UI/c_upload/delete.py",
    title="Delete Files",
    icon=":material/scan_delete:",
)
svip = st.Page(
    "UI/consumer_insight/svip.py",
    title="SVIP Recommendation",
    icon=":material/stars:",
    default=(role == "Clerk")
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

account_pages = [logout_page, settings]
a_upload_pages = [a_upload, a_show, a_delete]
c_upload_pages = [c_upload, c_show, c_delete]
allmember_pages = [member_overview, member_analysis]
insight_pages = [svip]
brand_pages = [inventory]

# st.title("XSell")
st.logo("UI/images/horizontal_blue.png", icon_image="UI/images/icon_blue.png")

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

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

# 启动应用
pg.run()