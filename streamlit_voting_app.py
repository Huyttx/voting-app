import streamlit as st
import json
import os
from datetime import datetime

# ⚠️ set_page_config phải nằm ở đầu tiên
st.set_page_config(page_title="Bầu cử", layout="centered")

# ----------------------- Khai báo file ----------------------- #
CANDIDATE_FILE = "candidates.json"
VOTE_FILE = "votes.json"
USER_FILE = "voted_users.json"
ALLOWED_USERS_FILE = "allowed_users.json"
MIN_CHOICE = 1
MAX_CHOICE = 3

# ----------------------- Hàm tiện ích ----------------------- #
def load_json(file):
    with open(file, encoding="utf-8") as f:
        return json.load(f)

def save_json(data, file):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def init_files():
    if not os.path.exists(CANDIDATE_FILE):
        save_json([
            {"id": 1, "name": "Nguyen Van A", "birth_year": 1980, "position": "Truong phong"},
            {"id": 2, "name": "Tran Thi B", "birth_year": 1985, "position": "Pho phong"},
            {"id": 3, "name": "Pham Van C", "birth_year": 1990, "position": "Nhan vien"},
            {"id": 4, "name": "Le Thi D", "birth_year": 1982, "position": "Nhan vien"}
        ], CANDIDATE_FILE)

    if not os.path.exists(VOTE_FILE):
        votes = [{"id": c["id"], "name": c["name"], "votes": 0} for c in load_json(CANDIDATE_FILE)]
        save_json(votes, VOTE_FILE)

    if not os.path.exists(USER_FILE):
        save_json({}, USER_FILE)

    if not os.path.exists(ALLOWED_USERS_FILE):
        save_json(["user01", "user02", "user03"], ALLOWED_USERS_FILE)

# ----------------------- Ghi phiếu bầu ----------------------- #
def record_vote(user_id, selection):
    votes = load_json(VOTE_FILE)
    for sel in selection:
        for v in votes:
            if v["name"] == sel:
                v["votes"] += 1
    save_json(votes, VOTE_FILE)

    users = load_json(USER_FILE)
    users[user_id] = {
        "voted": True,
        "time": str(datetime.now()),
        "selection": selection
    }
    save_json(users, USER_FILE)

# ----------------------- Giao diện người dùng ----------------------- #
def main():
    st.title("\U0001F5F3️ Bầu chọn ứng viên")
    init_files()

    allowed_users = load_json(ALLOWED_USERS_FILE)
    user_id = st.text_input("\U0001F510 Nhập mã bầu cử:", key="user_id_input")

    if user_id:
        if user_id not in allowed_users:
            st.error("❌ Mã không hợp lệ.")
            return

        users = load_json(USER_FILE)
        if user_id in users and users[user_id]["voted"]:
            st.warning("⚠️ Bạn đã bầu.")
        else:
            candidates = load_json(CANDIDATE_FILE)
            st.markdown("### Danh sách Ứng viên")
            for c in candidates:
                st.markdown(f"- **{c['name']}** ({c['position']}, {c['birth_year']})")

            selection = st.multiselect("✅ Chọn ứng viên:", [c["name"] for c in candidates], key="candidate_select")
            if st.button("📝 Xác nhận", key="confirm_vote"):
                if len(selection) < MIN_CHOICE:
                    st.error("Chọn quá ít.")
                elif len(selection) > MAX_CHOICE:
                    st.error("Chọn quá nhiều.")
                else:
                    st.success(f"Đã chọn: {selection}")
                    if st.button("✅ Gửi phiếu", key="submit_vote"):
                        record_vote(user_id, selection)
                        st.success("Phiếu bầu đã được ghi nhận.")

# ----------------------- Hướng dẫn ----------------------- #
    with st.expander("\U0001F680 Hướng dẫn triển khai trên GitHub & Streamlit Cloud"):
        st.markdown("""
        1. Đảm bảo 4 file: `candidates.json`, `votes.json`, `voted_users.json`, `allowed_users.json` có trong thư mục gốc.
        2. Push toàn bộ lên GitHub.
        3. Deploy qua [Streamlit Cloud](https://share.streamlit.io).
        4. Mỗi người chỉ được vote 1 lần, kiểm soát qua mã người dùng.
        5. Xem thống kê bằng mật khẩu quản trị.
        """)

if __name__ == "__main__":
    main()
