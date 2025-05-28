import streamlit as st
import json
import os
from datetime import datetime

# Constants
CANDIDATE_FILE = "candidates.json"
VOTE_FILE = "votes.json"
USER_FILE = "voted_users.json"

MIN_CHOICE = 1
MAX_CHOICE = 3

# ----------------------- Data Initialization ----------------------- #
def init_files():
    if not os.path.exists(CANDIDATE_FILE):
        candidates = [
            {"id": 1, "name": "Nguyen Van A", "birth_year": 1980, "position": "Truong phong"},
            {"id": 2, "name": "Tran Thi B", "birth_year": 1985, "position": "Pho phong"},
            {"id": 3, "name": "Pham Van C", "birth_year": 1990, "position": "Nhan vien"},
            {"id": 4, "name": "Le Thi D", "birth_year": 1982, "position": "Nhan vien"}
        ]
        with open(CANDIDATE_FILE, "w", encoding="utf-8") as f:
            json.dump(candidates, f, indent=2)

    if not os.path.exists(VOTE_FILE):
        with open(CANDIDATE_FILE, encoding="utf-8") as f:
            candidates = json.load(f)
        votes = [{"id": c["id"], "name": c["name"], "votes": 0} for c in candidates]
        with open(VOTE_FILE, "w", encoding="utf-8") as f:
            json.dump(votes, f, indent=2)

    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)

# ----------------------- Voting Logic ----------------------- #
def load_candidates():
    with open(CANDIDATE_FILE, encoding="utf-8") as f:
        return json.load(f)

def load_votes():
    with open(VOTE_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_votes(votes):
    with open(VOTE_FILE, "w", encoding="utf-8") as f:
        json.dump(votes, f, indent=2)

def load_users():
    with open(USER_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

def record_vote(user_id, selection):
    votes = load_votes()
    for sel in selection:
        for v in votes:
            if v["name"] == sel:
                v["votes"] += 1
    save_votes(votes)
    users = load_users()
    users[user_id] = {"voted": True, "time": str(datetime.now())}
    save_users(users)

# ----------------------- Main App ----------------------- #
def main():
    st.set_page_config(page_title="Ứng dụng Bầu cử", layout="centered")
    st.title("🗳️ Hệ thống Bầu cử Online")
    init_files()

    user_id = st.text_input("🔐 Nhập mã bầu cử của bạn:")

    if user_id:
        users = load_users()
        if user_id in users and users[user_id]["voted"]:
            st.warning("⚠️ Bạn đã gửi phiếu bầu. Mỗi người chỉ được bầu 1 lần.")
        else:
            candidates = load_candidates()

            st.markdown("### Danh sách Ứng viên")
            for c in candidates:
                st.markdown(f"- **{c['name']}** (Sinh năm: {c['birth_year']}, Chức vụ: {c['position']})")

            names = [c["name"] for c in candidates]
            selection = st.multiselect(
                f"✅ Chọn từ {MIN_CHOICE} đến {MAX_CHOICE} ứng viên:",
                options=names
            )

            if st.button("📝 Gửi phiếu"):
                if len(selection) < MIN_CHOICE:
                    st.error(f"Bạn phải chọn ít nhất {MIN_CHOICE} ứng viên.")
                elif len(selection) > MAX_CHOICE:
                    st.error(f"Chỉ được chọn tối đa {MAX_CHOICE} ứng viên.")
                else:
                    record_vote(user_id, selection)
                    st.success("✅ Phiếu bầu của bạn đã được ghi nhận. Xin cảm ơn!")

    # ----------------------- Admin Section ----------------------- #
    st.markdown("---")
    with st.expander("📊 Xem kết quả thống kê (Admin)"):
        password = st.text_input("Mật khẩu quản trị:", type="password")
        if password == "admin123":
            votes = load_votes()
            total_votes = sum([v["votes"] for v in votes])
            st.subheader("Kết quả Bầu cử")
            for v in votes:
                percent = (v["votes"] / total_votes * 100) if total_votes > 0 else 0
                st.write(f"- {v['name']}: {v['votes']} phiếu ({percent:.2f}%)")
        elif password:
            st.error("Sai mật khẩu quản trị.")

    # ----------------------- Hướng dẫn ----------------------- #
    with st.expander("🚀 Hướng dẫn triển khai trên GitHub & Streamlit Cloud"):
        st.markdown("""
        1. Đảm bảo 3 file: `candidates.json`, `votes.json`, `voted_users.json` có trong thư mục gốc.
        2. Push toàn bộ lên GitHub.
        3. Deploy qua [Streamlit Cloud](https://share.streamlit.io).
        4. Mỗi người chỉ được vote 1 lần, kiểm soát qua mã người dùng.
        5. Xem thống kê bằng mật khẩu quản trị: `admin123`
        """)

if __name__ == "__main__":
    main()