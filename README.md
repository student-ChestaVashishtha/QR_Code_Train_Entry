# 🚉 QR Code Train Entry System

This project is a simple but effective **Train Entry System** using **QR Codes**. Every passenger is issued a unique QR code token that acts as their digital entry pass. Only passengers with valid QR tokens can be granted access to the train platform.

---

## 🔧 Key Features

- ✅ Generate a **secure unique ticket id** for each passenger
- ✅ Create a **QR code** containing only the token (no personal info exposed)
- ✅ Scan the QR to retrieve and verify the token
- ✅ Validate entry based on token existence
- ✅ City-to-city travel selection with live display
- ✅ Built using **Streamlit** and **qrcode** for fast deployment

---

## 🧰 Tech Stack

- **Python**
- **Streamlit** – Web interface
- **qrcode** – QR image generation
- **OpenCV** – For webcam-based QR code scanning

---

## 🚀 How It Works

1. **Passenger selects** their departure (`From`) and destination (`To`) city.
2. A **ticket id** is generated.
3. A **QR code** is created from that user details and shown/downloaded.
4. At the train gate, a QR scanner reads the ticket id.
5. If the toket id is valid (found in the database), entry is allowed.

---

## 📦 Installation

```bash
pip install streamlit qrcode[pil] opencv-python

---

##### This project I made in hackerthon is still in working #####

