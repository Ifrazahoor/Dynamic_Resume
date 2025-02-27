import streamlit as st
from fpdf import FPDF
from datetime import date

# Sidebar Theme Toggle
theme = st.sidebar.radio("Select Theme", ["Light", "Dark"])

# Apply Theme
if theme == "Dark":
    st.markdown(
        """
        <style>
            body { background-color: #1e1e1e; color: white; }
            .stTextInput, .stNumberInput, .stFileUploader, .stTextArea, .stSelectbox, .stDateInput {
                background-color: #333; color: white; border: 1px solid #555; border-radius: 10px; padding: 8px;
            }
            .stButton button { background-color: #007bff; color: white; border-radius: 8px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Resume Form
st.title("📄 Resume Generator")

with st.form("resume_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    dob = st.date_input("Date of Birth", min_value=date(1950, 1, 1), max_value=date.today())
    
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    st.write(f"🎂 **Age:** {age} years")

    address = st.text_area("Address")
    experience = st.number_input("Experience (Years)", 0, 40, 1)
    skills = st.text_area("Skills (comma-separated)")
    education = st.text_input("Highest Qualification")
    about = st.text_area("Short Bio")

    profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "png"])
    
    submitted = st.form_submit_button("Generate Resume")

# PDF Generation
def generate_pdf(name, email, phone, dob, age, address, experience, skills, education, about):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, name, ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"📧 Email: {email}", ln=True, align='C')
    pdf.cell(200, 10, f"📞 Phone: {phone}", ln=True, align='C')
    pdf.cell(200, 10, f"🎂 Age: {age} years", ln=True, align='C')
    pdf.cell(200, 10, f"🏠 Address: {address}", ln=True, align='C')

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Professional Details", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"📊 Experience: {experience} years", ln=True)
    pdf.cell(200, 10, f"🎓 Education: {education}", ln=True)
    pdf.cell(200, 10, f"🛠 Skills: {skills}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "About Me", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, about)

    return pdf

# Display Resume & Download Button
if submitted:
    if name and email and phone and skills and education:
        st.success(f"🎉 Resume Generated for {name} (Age: {age} years)")

        pdf = generate_pdf(name, email, phone, dob, age, address, experience, skills, education, about)

        pdf_file_path = "resume.pdf"
        pdf.output(pdf_file_path)

        with open(pdf_file_path, "rb") as pdf_file:
            st.download_button("📄 Download Resume", pdf_file, file_name=f"{name}_Resume.pdf", mime="application/pdf")
    else:
        st.warning("⚠ Please fill in all required fields!")