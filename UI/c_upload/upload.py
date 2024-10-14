import streamlit as st
import os

# Set the upload directory
UPLOAD_FOLDER = "c_data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.title("📁 File Upload")
st.write("Welcome to the File Upload System! Please upload your CSV or XLSX files.")

uploaded_files = st.file_uploader("Choose files to upload", 
                                    type=["csv", "xlsx"], 
                                    accept_multiple_files=True, 
                                    label_visibility="collapsed")

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ File '{uploaded_file.name}' has been successfully uploaded to `{file_path}`")
else:
    st.warning('Note: No files are being uploaded right now.', icon="⚠️")

#---寡版
# import streamlit as st
# import os

# # 设置上传文件的目录
# UPLOAD_FOLDER = "data"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# uploaded_files = st.file_uploader("Upload files", 
# type=["csv", "xlsx"], accept_multiple_files=True)

# if uploaded_files is not None:
#     # 遍历每个上传的文件并保存
#     for uploaded_file in uploaded_files:
#         file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())
#         st.success(f"Document '{uploaded_file.name}' has been uploaded to {file_path}")
# else:
#     st.error('Upload failed, please try again!', icon="⚠️")

# 如果有文件上传，将它们存储在会话状态中
# if uploaded_files:
#     st.session_state.uploaded_files = uploaded_files
#     st.success("Files uploaded successfully!")
# else:
    # st.session_state.uploaded_files = None  # 没有文件时设置为 None

# for uploaded_file in uploaded_files:
#     bytes_data = uploaded_file.read()
#     st.write("filename:", uploaded_file.name)
#     st.write(bytes_data)