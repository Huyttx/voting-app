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
    try:
        if os.path.exists(VOTE_FILE):
            with open(VOTE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except json.JSONDecodeError:
        st.error("⚠️ Lỗi định dạng trong file votes.json")
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
