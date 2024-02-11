import tkinter as tk
from tkinter import messagebox, simpledialog
from twilio.rest import Client
import subprocess

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("300x150")

        # Twilio credentials
        self.twilio_account_sid = "AC0bda0c677d12e29647e2f8754cbb7eaa"
        self.twilio_auth_token = "f56d52ddf1dd52e09d423a50edce6c61"
        self.twilio_phone_number = "+1 6592448997"

        self.initialize_login()

    def initialize_login(self):
        label_username = tk.Label(self.master, text="Username:")
        label_username.pack(pady=5)

        self.entry_username = tk.Entry(self.master)
        self.entry_username.pack(pady=5)

        label_password = tk.Label(self.master, text="Password:")
        label_password.pack(pady=5)

        self.entry_password = tk.Entry(self.master, show="*")
        self.entry_password.pack(pady=5)

        login_button = tk.Button(self.master, text="Login", command=self.send_sms, height=2, width=15)
        login_button.pack(pady=15)

    def send_sms(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Replace with your actual username and password
        correct_username = "Charan Raavi"
        correct_password = "charanisthebest"

        if username == correct_username and password == correct_password:
            self.send_verification_sms()
        else:
            messagebox.showwarning("Access Denied", "Incorrect username or password. Please try again.")

    def send_verification_sms(self):
        # Generate a random verification code
        verification_code = simpledialog.askstring("Verification Code", "Enter the code sent to your phone(BOT VERIFICATION):")

        # Replace with your Twilio account SID, auth token, and Twilio phone number
        client = Client(self.twilio_account_sid, self.twilio_auth_token)

        # Replace with the phone number where you want to receive the SMS
        to_phone_number = "+91 9697592592"

        message = client.messages.create(
            to=to_phone_number,
            from_=self.twilio_phone_number,
            body=f"Your verification code is: {verification_code}"
        )

        entered_code = simpledialog.askstring("Verification Code", "Enter the code sent to your phone(DOUBLE STEP VERIFICATION):")

        if entered_code == verification_code:
            self.run_main_script()
        else:
            messagebox.showwarning("Access Denied", "Incorrect verification code. Please try again.")

    def run_main_script(self):
        subprocess.Popen(["python", "main.py"])
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()
