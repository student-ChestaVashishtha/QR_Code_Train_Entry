import streamlit as st
import qrcode
import uuid
import cv2
import tempfile
import json
import os
from datetime import datetime

TICKET_FILE = "tickets.json"

# --- Ensure ticket file exists ---
if not os.path.exists(TICKET_FILE):
    with open(TICKET_FILE, "w") as f:
        json.dump([], f)

# --- QR Code Generator ---
def generate_qr(data_dict):
    qr = qrcode.make(json.dumps(data_dict))
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    qr.save(temp_file.name)
    return temp_file.name

# --- Ticket Store ---
def save_ticket(ticket):
    with open(TICKET_FILE, "r+") as file:
        tickets = json.load(file)
        tickets.append(ticket)
        file.seek(0)
        json.dump(tickets, file, indent=2)

def load_ticket_ids():
    with open(TICKET_FILE, "r") as file:
        tickets = json.load(file)
        return [ticket["ticket_id"] for ticket in tickets]

# --- QR Scanner ---
def scan_qr_from_webcam():
    with open(TICKET_FILE, "r") as file:
        tickets = json.load(file)

    valid_ids = [t["ticket_id"] for t in tickets]

    st.info("Press 'Q' to quit the camera feed.")
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    result = "No QR scanned"

    while True:
        success, frame = cap.read()
        if not success:
            st.error("Failed to access webcam.")
            break

        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            try:
                qr_dict = json.loads(data)
                ticket_id = qr_dict.get("ticket_id")

                if ticket_id in valid_ids:
                    result = f"✅ Access Granted (Ticket ID: {ticket_id})"
                else:
                    result = "❌ Access Denied: Ticket not found"

                cap.release()
                cv2.destroyAllWindows()
                return result
            except:
                result = "❌ Invalid QR Code (bad format)"
                cap.release()
                cv2.destroyAllWindows()
                return result

        cv2.imshow("Scan QR Code", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return result

# --- Custom CSS ---
st.markdown("""
    <style>
        .main {
            background-color: #f0f8ff;
        }
        .block-container {
            padding: 2rem 2rem;
        }
        .stTextInput, .stSelectbox, .stDateInput, .stButton {
            border-radius: 8px;
        }
        h1 {
            color: #2c3e50;
        }
        .title {
            font-size: 2.2em;
            font-weight: bold;
            color: #1abc9c;
        }
    </style>
""", unsafe_allow_html=True)

# --- Streamlit UI ---
st.markdown("<h1 class='title'>🚆 QR-Based Train Entry System</h1>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("📋 Menu", ["Book Ticket (Generate QR)", "Scan QR to Enter"])

if menu == "Book Ticket (Generate QR)":
    st.markdown("### 🎟️ Book Ticket and Generate QR")
    name = st.text_input("👤 Passenger Name")
    from_city = st.text_input("🌆 Departure City", placeholder="From")
    to_city = st.text_input("🌆 Arrival City", placeholder="To")
    train_no = st.text_input("🚄 Train Number", placeholder="e.g. 12045")
    travel_date = st.date_input("📅 Travel Date", value=datetime.now().date())
    
    st.markdown("### 💰 Ticket Payment")
    if "payment_done" not in st.session_state:
        st.session_state.payment_done = False

    if not st.session_state.payment_done:
        if st.button("💳 Pay Now"):
            if not name or not train_no or not from_city or not to_city :
                    st.warning("⚠️ Please fill in all required fields.")
            else:
                    st.session_state.payment_done = True
                    st.success("✅ Payment Successful!")
    else:
         st.button("✅ Paid", disabled=True)

    if st.button("🎫 Generate Ticket & QR"):
        if not st.session_state.payment_done :
            st.warning("⚠️ Payment Failed .")
        else:
            ticket_id = str(uuid.uuid4())[:8]
            ticket = {
                "ticket_id": ticket_id,
                "name": name,
                "from_city": from_city,
                "to_city": to_city,
                "train_no": train_no,
                "date": str(travel_date)
            }
            save_ticket(ticket)
            qr_path = generate_qr(ticket)
            st.success(f"✅ Ticket Booked!\n\n🆔 Ticket ID: `{ticket_id}`")
            st.image(qr_path, caption="📷 Scan this QR at Entry", use_container_width=True)


elif menu == "Scan QR to Enter":
    st.session_state.payment_done = False
    st.markdown("### 🧾 Scan QR Code for Entry")
    if st.button("📷 Start Camera and Scan QR"):
        result = scan_qr_from_webcam()
        st.success(result if result.startswith("✅") else result)


