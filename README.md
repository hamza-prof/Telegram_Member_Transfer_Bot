### Telegram Channel Members Transfer Tool

**Instructions to Run:**

1. **Extract the ZIP file** to your computer.
2. **Generate the `main.exe` file**:
   - Open a terminal/command prompt in the folder where `main.py` is located.
   - Run the following command to generate the `main.exe` file:
     ```bash
     pyinstaller --onefile --noconsole main.py
     ```
   - This will create the `main.exe` file in the `dist` folder within the same directory.
3. **Double-click the `main.exe` file** in the `dist` folder to launch the application.
4. Follow the prompts in the graphical interface:
   - Enter your Telegram API ID, API Hash, and phone number.
   - Input the source group username (without @) to copy members from.
   - Input the target group username (without @) to add members to.

**Requirements:**

- Ensure your **Telegram account** is active and logged in on your phone.
- Have **admin rights** for the target group.
- **Python** and **PyInstaller** installed on your machine to generate the `main.exe` file.
  - Install PyInstaller using:
    ```bash
    pip install pyinstaller
    ```

**Log File:**

- All actions and errors are logged in the `telegram_member_transfer.log` file for troubleshooting.

**Note:**

- To avoid bans, the tool respects **Telegram's rate limits** and includes delays between member additions.

Enjoy using the tool! Contact me for support or future updates.
