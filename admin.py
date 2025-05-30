import streamlit as st
import pandas as pd
import json
import os
import io
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

VOTE_FILE = "votes.json"

# ------------------ Utility Functions ------------------ #

def load_votes():
    if os.path.exists(VOTE_FILE):
        with open(VOTE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def export_excel(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Ket Qua")
    buffer.seek(0)
    return buffer

def export_pdf(df):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawString(180, height - 40, "KẾT QUẢ BẦU CỬ")

    c.setFont("Helvetica", 12)
    y = height - 80
    for idx, row in df.iterrows():
        line = f"{row['name']}: {row['votes']} phiếu"
        c.drawString(80, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50
    c.save()
    buffer.seek(0)
    return buffer

# ------------------ Streamlit App ------------------ #

def main():
    st.set_page_config(page_title="Trang quản trị", layout="centered")
    st.title("🔐 Trang Quản Trị Kết Quả Bầu Cử")

    password = st.text_input("Nhập mật khẩu quản trị:", type="password")
    if password != "admin123":
        if password:
            st.error("❌ Sai mật khẩu!")
        return

    st.success("✅ Đăng nhập thành công!")

    votes = load_votes()
    if not votes:
        st.warning("Chưa có dữ liệu phiếu bầu.")
        return

    df = pd.DataFrame(votes)
    total_votes = df["votes"].sum()

    st.subheader("📊 Kết quả bầu cử")
    for _, row in df.iterrows():
        percent = (row["votes"] / total_votes * 100) if total_votes > 0 else 0
        st.write(f"- {row['name']}: {row['votes']} phiếu ({percent:.2f}%)")

    st.bar_chart(df.set_index("name")["votes"])

    st.markdown("### 📤 Tải kết quả")
    st.download_button(
        "📥 Tải CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name=f"ket_qua_{datetime.now():%Y%m%d_%H%M%S}.csv",
        mime="text/csv"
    )

    excel_file = export_excel(df)
    st.download_button(
        "📊 Tải Excel",
        data=excel_file,
        file_name=f"ket_qua_{datetime.now():%Y%m%d_%H%M%S}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    pdf_file = export_pdf(df)
    st.download_button(
        "🧾 Xuất PDF",
        data=pdf_file,
        file_name=f"ket_qua_{datetime.now():%Y%m%d_%H%M%S}.pdf",
        mime="application/pdf"
    )

if __name__ == "__main__":
    main()
