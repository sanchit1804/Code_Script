import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import streamlit as st
import time
import os

# ---------------- Streamlit Page Config ----------------
st.set_page_config(page_title="📧 Bulk Email Pro+ Dashboard", page_icon="📨", layout="centered")
st.title("📨 Bulk Email Sender — Pro+ Edition")
st.caption("Send personalized bulk emails with live logs, attachments, and custom names")

st.markdown("---")

# ---------------- Email Login Section ----------------
with st.expander("🔑 Gmail Login Details"):
    sender_name = st.text_input("Sender Name (appears in inbox)", placeholder="Your Name")
    sender_email = st.text_input("Your Gmail Address", placeholder="youremail@gmail.com")
    sender_password = st.text_input("App Password", type="password", placeholder="16-character Gmail App Password")

# ---------------- CSV Upload ----------------
uploaded_file = st.file_uploader("📂 Upload CSV (columns: Name, Email)", type=["csv"])

st.markdown("""
**Example CSV format:**
| Name | Email |
|------|--------------------|
| Rahul Pandey | rahul@example.com |
| Riya Sharma | riya@example.com |
""")

# ---------------- Manual Email Entry ----------------
with st.expander("✏️ Add Optional Emails Manually"):
    manual_emails = st.text_area(
        "Enter additional emails manually (format: Name:Email, separated by commas)",
        placeholder="Rahul Pandey:rahul@gmail.com, Riya Sharma:riya@gmail.com"
    )

# ---------------- Email Content ----------------
subject = st.text_input("✉️ Email Subject", placeholder="Hello {Name}, here’s your update!")
message_template = st.text_area(
    "📝 Email Body (you can use placeholders like {Name})",
    height=150,
    placeholder="Dear {Name},\n\nHope you're doing well!\n\nBest regards,\nYour Name"
)

# ---------------- File Attachment ----------------
attachment = st.file_uploader("📎 Optional: Attach a file (PDF, Image, or DOCX)", type=["pdf", "jpg", "jpeg", "png", "docx"])

# ---------------- Email Preview ----------------
if st.button("👁️ Preview Email"):
    if uploaded_file:
        df_preview = pd.read_csv(uploaded_file)
        if "Name" in df_preview.columns and len(df_preview) > 0:
            name_sample = df_preview["Name"][0]
            st.markdown("### 🧾 Preview for first recipient:")
            st.info(f"**Subject:** {subject.format(Name=name_sample)}\n\n{message_template.format(Name=name_sample)}")
        else:
            st.warning("CSV must have a 'Name' column with at least one entry.")
    else:
        st.warning("Please upload a CSV first.")

# ---------------- Send Button ----------------
if st.button("🚀 Send Emails"):
    if not sender_email or not sender_password:
        st.error("Please enter your Gmail and App Password.")
    elif uploaded_file is None and not manual_emails:
        st.error("Please upload a CSV file or enter emails manually.")
    else:
        try:
            recipients = []

            # Load from CSV if available
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                if "Email" not in df.columns or "Name" not in df.columns:
                    st.error("CSV must contain columns 'Name' and 'Email'.")
                    st.stop()
                for _, row in df.iterrows():
                    recipients.append({"Name": row["Name"], "Email": row["Email"]})

            # Add manual emails (support Name:Email or just Email)
            if manual_emails:
                for entry in [e.strip() for e in manual_emails.split(",") if e.strip()]:
                    if ":" in entry:
                        name, email = entry.split(":", 1)
                        recipients.append({"Name": name.strip(), "Email": email.strip()})
                    else:
                        recipients.append({"Name": "Friend", "Email": entry.strip()})

            # Connect to Gmail
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            st.success("✅ Logged in successfully!")

            # UI Setup: progress bar + live logs
            progress = st.progress(0)
            status = st.empty()
            log_box = st.container()
            total = len(recipients)
            success_count = 0

            # ---------------- Sending Loop ----------------
            for i, recipient in enumerate(recipients):
                recipient_email = recipient["Email"]
                recipient_name = recipient["Name"]

                msg = MIMEMultipart()
                msg["From"] = f"{sender_name} <{sender_email}>"
                msg["To"] = recipient_email
                msg["Subject"] = subject.format(Name=recipient_name)

                # Message body
                body = message_template.format(Name=recipient_name)
                msg.attach(MIMEText(body, "plain"))

                # Add attachment if uploaded
                if attachment is not None:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.getvalue())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={attachment.name}"
                    )
                    msg.attach(part)

                # Send email and log live
                try:
                    server.send_message(msg)
                    success_count += 1
                    with log_box:
                        st.markdown(f"✅ **Sent to {recipient_name}** ({recipient_email})")
                except Exception as e:
                    with log_box:
                        st.markdown(f"⚠️ **Failed to send to {recipient_email}:** {e}")

                # Update progress bar
                progress.progress((i + 1) / total)
                status.text(f"📨 Sending email {i+1}/{total}...")

                time.sleep(0.5)

            server.quit()
            st.success(f"✅ Successfully sent {success_count}/{total} emails!")
            st.balloons()

        except Exception as e:
            st.error(f"❌ Error: {e}")
