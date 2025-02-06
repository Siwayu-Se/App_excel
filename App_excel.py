import streamlit as st
import pandas as pd
from io import BytesIO

# กำหนด URL หรือเส้นทางของภาพพื้นหลัง
background_image_url = "https://images.unsplash.com/photo-1620570623737-efc0ec4ab486?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

# กำหนดสีที่ต้องการ
text_color = "#FFCC99"  # สีที่คุณต้องการ

# ใส่ CSS สำหรับพื้นหลังและสีตัวอักษร
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('{background_image_url}');
        background-size: cover;
        background-position: center;
        height: 100vh;
    }}
    h1, h2, h3, p, div {{
        color: {text_color} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# ส่วนอัปโหลดไฟล์ Excel
uploaded_file = st.file_uploader("อัปโหลดไฟล์ Excel", type="xlsx")

if uploaded_file is not None:
    # อ่านข้อมูลจากไฟล์ Excel
    df = pd.read_excel(uploaded_file)

    # แสดงตัวอย่างข้อมูล
    st.write("ตัวอย่างข้อมูล:", df.head())

    # ตรวจสอบว่าแถวไหนมีคอลัมน์ A หรือ B หายไป
    def compare_rows(row):
        if pd.isna(row['A']) and pd.isna(row['B']):
            return "Both columns are missing"
        elif pd.isna(row['A']):
            return "No have column A"
        elif pd.isna(row['B']):
            return "No have column B"
        elif row['A'] == row['B']:
            return "Result is Same"
        else:
            return "Result is not same"

    # สร้างคอลัมน์ใหม่เพื่อเก็บผลลัพธ์การเปรียบเทียบ
    df['Comparison'] = df.apply(compare_rows, axis=1)
    
    # แสดงผลลัพธ์การเปรียบเทียบ
    st.write("ผลการเปรียบเทียบ:", df[['A', 'B', 'Comparison']])

    # ฟังก์ชันสำหรับการดาวน์โหลดไฟล์
    def to_excel(df):
        # สร้างไฟล์ Excel จาก DataFrame
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Comparison Results')
        processed_data = output.getvalue()
        return processed_data

    # เพิ่มปุ่มให้ผู้ใช้ดาวน์โหลดไฟล์ที่เปรียบเทียบแล้ว
    excel_file = to_excel(df)
    st.download_button(
        label="ดาวน์โหลดไฟล์ Excel",
        data=excel_file,
        file_name="comparison_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
