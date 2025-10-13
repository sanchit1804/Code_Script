# 📨 Bulk Email Sender 

A modern **Streamlit web application** that allows users to send **personalized bulk emails** with optional attachments, Gmail App Password authentication, and live progress tracking.

---

## 🚀 Overview

This application simplifies email marketing and bulk communication by letting you send personalized emails to multiple recipients directly from a simple web interface.  
Built with **Python** and **Streamlit**, it supports both **CSV-based** and **manual** recipient entry.

---

## ✨ Key Features

- 📋 **CSV Upload Support** — Upload recipient lists in `.csv` format (`Name`, `Email`)
- ✏️ **Manual Email Entry** — Add extra emails manually in “Name:Email” format
- 🪄 **Personalized Messages** — Use placeholders like `{Name}` in your subject and message
- 📎 **File Attachments** — Attach PDFs, images, or DOCX files to your emails
- 👁️ **Email Preview** — Preview subject and message before sending
- 📊 **Progress Bar + Logs** — Live progress tracker with real-time status updates
- 🔐 **Secure Gmail Login** — Uses **App Passwords** (never your actual Gmail password)
- 🎈 **Clean UI with Streamlit** — User-friendly interface with status updates and balloons on completion

---

## 📂 Example CSV Format

Make sure your CSV has the following structure:

| Name | Email |
|------|--------------------|
| Rahul Pandey | rahul@example.com |
| Riya Sharma | riya@example.com |

---

## 🔧 Gmail App Password Setup

To use your Gmail securely, follow these steps:

1. Go to your [Google Account Security Settings](https://myaccount.google.com/security)
2. Enable **2-Step Verification**
3. Go to **App Passwords**
4. Choose:
   - **App:** Mail  
   - **Device:** Windows (or any)
5. Copy the generated **16-character password**
6. Use it in this app instead of your regular Gmail password

> ⚠️ *Without enabling 2-Step Verification, you cannot use Gmail App Password.
