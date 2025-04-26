import smtplib
from email.message import EmailMessage
import streamlit as st


# Function to send email

# def send_otp(recipients, subject, body, sender, sender_password):
#     # Create email message
#     msg = EmailMessage()
#     msg["Subject"] = subject
#     msg["From"] = sender
#     msg["To"] = ", ".join(recipients)
#     msg.set_content(body)
#
#     # Connect to Gmail's SMTP server over SSL.
#     # Change the server settings if you're using a different email provider.
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#         smtp.login(sender, sender_password)
#         smtp.send_message(msg)
# send_otp()

def send_email(recipients, subject, body):
    # Create email message
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "segmentrends@gmail.com"
    msg["To"] = ", ".join(recipients)
    msg.set_content(body)

    # Connect to Gmail's SMTP server over SSL.
    # Change the server settings if you're using a different email provider.
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        #"qnca umak ngjz gave"
        PASSW = st.secrets["PASS"]
        smtp.login("segmentrends@gmail.com",PASSW)
        smtp.send_message(msg)


# # Streamlit app
# st.title("Bulk Email Sender")
#
# # Instructions
# st.write("Enter your sender email credentials and a comma-separated list of recipient emails.")
#
# # Input fields
# sender = "segmentrends@gmail.com"
# sender_password = "qnca umak ngjz gave"          # st.text_input("Sender Password", type="password")
# subject = st.text_input("Email Subject")
# body = st.text_area("Email Body")
# recipients_str = st.text_area("Recipient Emails (comma separated)")
#
# if st.button("Send Email"):
#     # Split recipient emails by comma and strip spaces
#     recipients = [email.strip() for email in recipients_str.split(",") if email.strip()]
#     if not recipients:
#         st.error("Please enter at least one recipient email.")
#     elif not sender or not sender_password:
#         st.error("Please enter your sender email and password.")
#     else:
#         try:
#             send_email(recipients, subject, body, sender, sender_password)
#             st.success("Email sent successfully!")
#         except Exception as e:
#             st.error(f"Error sending email: {e}")
