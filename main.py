import tkinter as tk
from tkinter import messagebox, ttk
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
import time
import logging
import os

# Setup logging
logging.basicConfig(
    filename="telegram_member_transfer.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

# Functionality
class TelegramMemberTransfer:
    def __init__(self, api_id, api_hash, phone, source_group, target_group, log_text):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.source_group = source_group
        self.target_group = target_group
        self.client = None
        self.log_text = log_text

    def update_log(self, message, level="info"):
        """Update log in both the GUI and the log file."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        if level == "info":
            logging.info(message)
        elif level == "error":
            logging.error(message)
        elif level == "warning":
            logging.warning(message)
        else:
            logging.debug(message)

    def authenticate(self):
        """Authenticate Telegram Client"""
        try:
            self.update_log("Authenticating Telegram client...")
            self.client = TelegramClient("session", self.api_id, self.api_hash)
            self.client.connect()
            if not self.client.is_user_authorized():
                self.client.send_code_request(self.phone)
                code = simple_input("Enter the code sent to your phone:")
                self.client.sign_in(self.phone, code)
            self.update_log("Successfully authenticated!")
        except Exception as e:
            self.update_log(f"Authentication error: {e}", "error")
            messagebox.showerror("Error", f"Authentication failed: {e}")

    def fetch_members(self):
        """Fetch Members from Source Group"""
        try:
            self.update_log(f"Fetching members from the group: {self.source_group}")
            source_entity = self.client.get_entity(self.source_group)
            members = self.client.get_participants(source_entity)
            self.update_log(f"Fetched {len(members)} members from {self.source_group}")
            return members
        except Exception as e:
            self.update_log(f"Error fetching members: {e}", "error")
            messagebox.showerror("Error", f"Could not fetch members: {e}")
            return []

    def add_members(self, members):
        """Add Members to Target Group"""
        added_count = 0
        try:
            self.update_log(f"Starting to add members to the group: {self.target_group}")
            target_entity = self.client.get_entity(self.target_group)
            for member in members:
                try:
                    if not member.username:
                        continue  # Skip users without usernames
                    self.client(InviteToChannelRequest(target_entity, [member]))
                    self.update_log(f"Added: {member.username}")
                    time.sleep(30)  # Avoid rate limits
                    added_count += 1
                except PeerFloodError:
                    self.update_log("Rate limit reached. Stopping further additions.", "warning")
                    messagebox.showwarning("Rate Limit", "Telegram rate limit reached. Try again later.")
                    break
                except UserPrivacyRestrictedError:
                    self.update_log(f"User privacy settings prevented adding {member.username}", "warning")
                    continue
            self.update_log(f"Finished adding members. Total added: {added_count}")
            messagebox.showinfo("Complete", f"Added {added_count} members successfully!")
        except Exception as e:
            self.update_log(f"Error adding members: {e}", "error")
            messagebox.showerror("Error", f"Could not add members: {e}")

    def run(self):
        """Run the Member Transfer Process"""
        self.authenticate()
        members = self.fetch_members()
        if members:
            self.add_members(members)
        self.client.disconnect()

# GUI Setup
def run_tool():
    api_id = api_id_entry.get()
    api_hash = api_hash_entry.get()
    phone = phone_entry.get()
    source_group = source_group_entry.get()
    target_group = target_group_entry.get()

    if not all([api_id, api_hash, phone, source_group, target_group]):
        messagebox.showerror("Input Error", "All fields are required!")
        return

    tool = TelegramMemberTransfer(api_id, api_hash, phone, source_group, target_group, log_text)
    tool.run()

# Simple input for authentication codes
def simple_input(prompt):
    return messagebox.askstring("Code Required", prompt)

# GUI Interface
root = tk.Tk()
root.title("Simple transfer Members GUI")
root.geometry("500x600")
root.configure(bg="#282C34")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#282C34", foreground="#FFFFFF", font=("Arial", 12))
style.configure("TButton", background="#61AFEF", foreground="#FFFFFF", font=("Arial", 12), padding=6)
style.map("TButton", background=[("active", "#56B6C2")])

# Title
title_label = tk.Label(root, text="Telegram Member Transfer Tool", font=("Helvetica", 16, "bold"), bg="#282C34", fg="#61AFEF")
title_label.pack(pady=10)

# Input Fields
tk.Label(root, text="Telegram API ID:", bg="#282C34", fg="#FFFFFF").pack(anchor="w", padx=20)
api_id_entry = ttk.Entry(root)
api_id_entry.pack(fill="x", padx=20, pady=5)

tk.Label(root, text="Telegram API Hash:", bg="#282C34", fg="#FFFFFF").pack(anchor="w", padx=20)
api_hash_entry = ttk.Entry(root)
api_hash_entry.pack(fill="x", padx=20, pady=5)

tk.Label(root, text="Phone Number:", bg="#282C34", fg="#FFFFFF").pack(anchor="w", padx=20)
phone_entry = ttk.Entry(root)
phone_entry.pack(fill="x", padx=20, pady=5)

tk.Label(root, text="Source Group Username (without @):", bg="#282C34", fg="#FFFFFF").pack(anchor="w", padx=20)
source_group_entry = ttk.Entry(root)
source_group_entry.pack(fill="x", padx=20, pady=5)

tk.Label(root, text="Target Group Username (without @):", bg="#282C34", fg="#FFFFFF").pack(anchor="w", padx=20)
target_group_entry = ttk.Entry(root)
target_group_entry.pack(fill="x", padx=20, pady=5)

# Log Output
log_label = tk.Label(root, text="Log Output:", bg="#282C34", fg="#FFFFFF")
log_label.pack(anchor="w", padx=20, pady=(10, 0))
log_text = tk.Text(root, height=10, bg="#1E2127", fg="#ABB2BF", font=("Consolas", 10))
log_text.pack(fill="both", padx=20, pady=5, expand=True)

# Run Button
run_button = ttk.Button(root, text="Start Transfer", command=run_tool)
run_button.pack(pady=20)

# Main Loop
root.mainloop()
