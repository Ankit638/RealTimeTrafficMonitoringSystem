from twilio.rest import Client
import pandas as pd
import os

# Load vehicle data
vehicle_data = pd.read_csv("vehicle_data.csv")

# Twilio config from .env or hardcode here if needed
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_FROM = os.getenv("TWILIO_FROM")  # Twilio phone number

def send_sms_alert(plate_number, message):
    try:
        # Normalize and match plate
        plate_number = plate_number.upper()
        match = vehicle_data[vehicle_data["plate_number"].str.upper() == plate_number]
        
        if match.empty:
            print(f"⚠️ No contact found for plate {plate_number}")
            return

        contact = match.iloc[0]["contact"]
        name = match.iloc[0]["name"]

        client = Client(TWILIO_SID, TWILIO_AUTH)
        sms = client.messages.create(
            body=f"🚨 Traffic Violation Alert 🚨\n\nDear {name},\n{message}",
            from_=TWILIO_FROM,
            to=f"+91{contact}"
        )

        print(f"📱 SMS sent to {contact} for {plate_number} [SID: {sms.sid}]")

    except Exception as e:
        print(f"❌ SMS sending failed: {e}")
