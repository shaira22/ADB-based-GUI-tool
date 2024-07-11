import subprocess
import threading
import tkinter as tk
from tkinter import ttk
from queue import Queue
from datetime import datetime

class ADBUI:
    VERSION_CODE = "v1.0"

    def __init__(self, root):
        self.root = root
        self.root.title(f"ADB Command UI {self.VERSION_CODE}")
        self.root.geometry("1024x786")  # Set your preferred width and height

        # Label to display the executed ADB command
        self.executed_command_label = tk.Label(root, text="", font=("Arial", 11), wraplength=1000)
        self.executed_command_label.pack()

        self.devices_label = tk.Label(root, text="Select Device:")
        self.devices_label.pack()

        self.device_combobox = ttk.Combobox(root, values=self.get_device_list())
        self.device_combobox.pack()

        self.command_label = tk.Label(root, text="Select ADB Command:")
        self.command_label.pack()

        self.command_combobox = ttk.Combobox(root, values=[
            "Run Sanity Suite",
            "Run Specific Test Suite",
            "Run Specific Test",
            "Run Hub AutoMailer Suite",
            "Run Battery Suite"
        ])
        self.command_combobox.pack()

        self.additional_params_frame = tk.Frame(root)
        self.additional_params_frame.pack()

        self.update_additional_params()

        # Queue to communicate between threads
        self.queue = Queue()

        self.execute_button = tk.Button(root, text="Execute Command", command=self.execute_adb_command)
        self.execute_button.pack()

        self.cancel_button = tk.Button(root, text="Cancel", command=self.cancel_adb_command, state="disabled")
        self.cancel_button.pack()

        # Binding the event to update specific tests when the test suite changes
        self.command_combobox.bind("<<ComboboxSelected>>", self.update_additional_params)

        self.status_label = tk.Label(root, text="", font=("Arial", 14))  # Set the font size to 14
        self.status_label.pack()

        # Variable to indicate whether a command is currently running
        self.command_running = False
        # Variable to hold the subprocess object
        self.subprocess_obj = None

        # Store the last position in stdout and stderr
        self.stdout_position = 0
        self.stderr_position = 0

        self.adb_command_text = tk.Text(root, height=4, wrap="none")
        self.adb_command_text.pack()

        # Button to refresh the list of connected devices
        self.refresh_button = tk.Button(root, text="Refresh Devices", command=self.refresh_device_list)
        self.refresh_button.pack()

        # Set up a timer to refresh devices every 30 seconds (adjust as needed)
        self.root.after(30000, self.refresh_device_list)

    def refresh_device_list(self):
        # Update the values in the device combobox
        self.device_combobox['values'] = self.get_device_list()
        self.root.after(30000, self.refresh_device_list)  # Schedule the next refresh

    def get_device_list(self):
        # Use adb devices to get the list of connected devices
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        devices = [line.split('\t')[0] for line in result.stdout.splitlines()[1:] if line.strip()]
        return devices

    def update_additional_params(self, event=None):
        # Clear existing widgets in the frame
        for widget in self.additional_params_frame.winfo_children():
            widget.destroy()

        selected_command = self.command_combobox.get()

        if selected_command in ["Run Sanity Suite", "Run Smoke Suite"]:
            # Provide options for suite.SanitySuite, suite.SmokeSuite, and suite.BatterySuite
            self.test_suite_label = tk.Label(self.additional_params_frame, text="Select Test Suite:")
            self.test_suite_label.pack()

            self.test_suite_combobox = ttk.Combobox(self.additional_params_frame, values=[
                "SanitySuite",
                "SmokeSuite"
            ])
            self.test_suite_combobox.pack()

        elif selected_command in ["Run Specific Test Suite", "Run Specific Test"]:
            # Provide options for specific tests based on the selected suite
            self.test_suite_label = tk.Label(self.additional_params_frame, text="Select Test Suite:")
            self.test_suite_label.pack()

            self.test_suite_combobox = ttk.Combobox(self.additional_params_frame, values=[
                "AcrobatReaderTest",
                "BWMessengerTest",
                "HubTest",
                "CalendarTest",
                "CameraTest",
                "CitrixWorkspaceTest",
                "SelfTest",
                "HubOpenAttachmentTest",
                "TasksTest",
                "NotesTest",
                "BbciTest",
                "ClipboardTest",
                "SecuFoxTest",
                "VerseTest",
                "VerseOpenAttachmentTest",
                "WPSOfficeTest",
                "TurtleImageViewerTest",
                "FileManagerTest",
                "GalleryTest",
                "SecuStoreTest",
                "SecuServiceTest",
                "SecuConnecTest",
                "SecuVoiceTest",
                "FoxitPdfTest",
                "EsriExplorerTest",
                "EsriFieldMapsTest",
                "Isec7MedTest",
                "Isec7MedOpenAttachmentTest",
                "WireTest",
                "SENetzTest",
                "JabberTest",
                "SecuOfficeTest",
                "KeePassTest",
                "WebexTest",
                "HorizonTest",
                "NextcloudTest",
                "ConversationsTest",
                "BWMessengerTest"
            ])
            self.test_suite_combobox.pack()

            if selected_command == "Run Specific Test":
                # Add additional specific tests for Run Specific Test
                self.additional_tests_label = tk.Label(self.additional_params_frame, text="Select Additional Test:")
                self.additional_tests_label.pack()

                self.additional_tests_combobox = ttk.Combobox(self.additional_params_frame, values=[
                    "testSendReceive",
                    "testSendReceive_duration",
                    "testSendReceiveWithAttachment",
                    "testCallLogs"
                ])
                self.additional_tests_combobox.pack()

        elif selected_command == "Run Hub AutoMailer Suite":
            # Provide entry fields for options
            self.runtime_label = tk.Label(self.additional_params_frame, text="Runtime:")
            self.runtime_label.pack()

            self.runtime_entry = tk.Entry(self.additional_params_frame)
            self.runtime_entry.pack()

            self.daytimer_label = tk.Label(self.additional_params_frame, text="Daytimer:")
            self.daytimer_label.pack()

            self.daytimer_entry = tk.Entry(self.additional_params_frame)
            self.daytimer_entry.pack()

            self.nighttime_label = tk.Label(self.additional_params_frame, text="Nighttime:")
            self.nighttime_label.pack()

            self.nighttime_entry = tk.Entry(self.additional_params_frame)
            self.nighttime_entry.pack()

            self.email1_label = tk.Label(self.additional_params_frame, text="Email1:")
            self.email1_label.pack()

            self.email1_entry = tk.Entry(self.additional_params_frame)
            self.email1_entry.pack()

            self.email2_label = tk.Label(self.additional_params_frame, text="Email2:")
            self.email2_label.pack()

            self.email2_entry = tk.Entry(self.additional_params_frame)
            self.email2_entry.pack()

            self.device_password_label = tk.Label(self.additional_params_frame, text="Enter Device Password:")
            self.device_password_label.pack()

            self.device_password_entry = tk.Entry(self.additional_params_frame, show="*")
            self.device_password_entry.pack()

        if selected_command == "Run Battery Suite":
            # Provide entry field for password
            self.device_password_label = tk.Label(self.additional_params_frame, text="Enter Device Password:")
            self.device_password_label.pack()

            self.device_password_entry = tk.Entry(self.additional_params_frame, show="*")
            self.device_password_entry.pack()

    def execute_adb_command(self):
        if self.command_running:
            self.status_label.config(text="Command is already running", fg="orange")
            return

        try:
            self.update_ui_before_execution()

            selected_device = self.device_combobox.get()
            selected_command = self.command_combobox.get()
            additional_params = self.get_additional_params(selected_command)

            if selected_command == "Run Specific Test Suite" or selected_command == "Run Specific Test":
                test_suite = self.test_suite_combobox.get()
                test_name = f"{test_suite}_{self.additional_tests_combobox.get()}" if selected_command == "Run Specific Test" else test_suite
            else:
                test_name = self.test_suite_combobox.get()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file_name = f"adb_output_{timestamp}_{selected_device}_{test_name}.txt"

            if selected_command == "Run Specific Test Suite" or selected_command == "Run Specific Test":
                adb_command = f"adb -s {selected_device} shell am instrument -w -r -e class {additional_params} com.blackberry.spl.functionaltest.test/android.support.test.runner.AndroidJUnitRunner > {output_file_name}"
            else:
                adb_command = f"adb -s {selected_device} shell am instrument -w -r -e class com.blackberry.spl.functionaltest.suite.{additional_params} com.blackberry.spl.functionaltest.test/android.support.test.runner.AndroidJUnitRunner > {output_file_name}"

            self.adb_command_text.delete(1.0, tk.END)  # Clear previous content
            self.adb_command_text.insert(tk.END, adb_command)

            threading.Thread(target=self.execute_adb_subprocess, args=(adb_command,), daemon=True).start()

        except Exception as e:
            self.handle_execution_error(e)

    def execute_adb_subprocess(self, adb_command):
        try:
            self.command_running = True
            self.subprocess_obj = subprocess.Popen(
                adb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1,
                universal_newlines=True  # Enable text mode for real-time output
            )

            self.root.after(100, self.check_for_updates)

        except Exception as e:
            self.handle_execution_error(e)
            self.finalize_execution()

    def check_for_updates(self):
        return_code = self.subprocess_obj.poll()
        if return_code is None:
            stdout = self.subprocess_obj.stdout.read()
            stderr = self.subprocess_obj.stderr.read()

            self.queue_output(stdout, 'stdout')
            self.queue_output(stderr, 'stderr')

            self.root.after(100, self.check_for_updates)
        else:
            self.queue_output('', 'done')
            self.finalize_execution()


    def queue_output(self, line, stream_type):
        self.queue.put((stream_type, line))
        print(f"[{stream_type.upper()}]: {line.strip()}")  # Print to console for debugging

    def get_additional_params(self, selected_command):
        try:
            if selected_command in ["Run Sanity Suite", "Run Smoke Suite"]:
                return f"{self.test_suite_combobox.get()}"

            elif selected_command in ["Run Specific Test Suite", "Run Specific Test"]:
                test_suite = self.test_suite_combobox.get()
                additional_params = f"com.blackberry.spl.functionaltest.test.specific.{test_suite}"

                if selected_command == "Run Specific Test":
                    additional_test = self.additional_tests_combobox.get()
                    additional_params += f"#{additional_test}"

                return additional_params

            elif selected_command == "Run Hub AutoMailer Suite":
                runtime = self.runtime_entry.get()
                daytimer = self.daytimer_entry.get()
                nighttime = self.nighttime_entry.get()
                email1 = self.email1_entry.get()
                email2 = self.email2_entry.get()
                device_password = self.device_password_entry.get()

                return (
                    f"com.blackberry.spl.functionaltest.suite.HubAutoMailerSuite "
                    f"-e config.AutoMailerTest.suiteDuration {runtime} "
                    f"-e config.AutoMailerTest.interval {daytimer} "
                    f"-e config.AutoMailerTest.intervalNight {nighttime} "
                    f"-e config.email1 {email1},{email2} "
                    f"-e config.devicePassword {device_password}"
                )

            if selected_command == "Run Battery Suite":
                #runtime = self.runtime_entry.get()
                #daytimer = self.daytimer_entry.get()
                #nighttime = self.nighttime_entry.get()
                #email1 = self.email1_entry.get()
                #email2 = self.email2_entry.get()
                device_password = self.device_password_entry.get()

                return (
                    f"BatterySuite "
                    #f"-e config.BatteryTest.suiteDuration {runtime} "
                    #f"-e config.BatteryTest.interval {daytimer} "
                    #f"-e config.BatteryTest.intervalNight {nighttime} "
                    #f"-e config.email1 {email1},{email2} "
                    f"-e config.devicePassword {device_password}"
                )

        except Exception as e:
            self.handle_execution_error(e)
            return None  # Return None on error

    def update_ui_before_execution(self):
        self.execute_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.status_label.config(text="Executing command...", fg="blue")

        # Clear previous content in the Text widget
        self.adb_command_text.delete(1.0, tk.END)

        # Display the executed ADB command in the Text widget
        self.adb_command_text.insert(tk.END, "Command will be displayed here after execution...\n")

        # Clear the queue
        self.queue.queue.clear()

        # Start a new thread to continuously update the Text widget
        threading.Thread(target=self.update_output_text, daemon=True).start()



    def finalize_execution(self):
        self.command_running = False
        self.execute_button.config(state="normal")
        self.cancel_button.config(state="disabled")
        self.status_label.config(text="Command execution finished", fg="green")

    # ... (other methods)

    def update_output_text(self):
        while self.command_running:
            try:
                stream_type, line = self.queue.get_nowait()
                if stream_type == 'stdout':
                    self.adb_command_text.insert(tk.END, f"[STDOUT]: {line}")
                elif stream_type == 'stderr':
                    self.adb_command_text.insert(tk.END, f"[STDERR]: {line}")
                elif stream_type == 'done':
                    self.adb_command_text.insert(tk.END, "Command execution finished.\n")
            except queue.Empty:
                pass

            # Scroll to the end of the Text widget
            self.adb_command_text.yview(tk.END)

            # Update the UI after a short delay
            self.root.after(100)

    # Add the cancel_adb_command method here
    def cancel_adb_command(self):
        if self.command_running:
            try:
                # Kill the adb process and update UI
                self.subprocess_obj.kill()
                self.subprocess_obj.wait()  # Wait for the process to finish
                self.status_label.config(text="Command canceled", fg="orange")
            except Exception as e:
                self.status_label.config(text=f"Error canceling command:\n{str(e)}", fg="red")
            finally:
                self.command_running = False
                self.execute_button.config(state="normal")
                self.cancel_button.config(state="disabled")
        else:
            self.status_label.config(text="No command is currently running", fg="orange")

    # ... (other methods)

if __name__ == "__main__":
    root = tk.Tk()
    adb_ui = ADBUI(root)
    root.mainloop()


