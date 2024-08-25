# ADB-based-GUI-tool

Some specific objectives and requirements like enhancing efficiency and accuracy were considered for designing the automated testing tool. The primary goals of the tool were to automate the execution of test cases and provide a user-friendly interface to ensure comprehensive logging for analysis and debugging. The tool was designed to meet the needs of the testers of the company by simplifying the testing process and providing adequate support for various testing scenarios.

The design of the tool was focused on solving key problems identified during the manual smoke testing phase. The design also aimed to create an intuitive interface that would be easy for testers to use. This is essential for minimizing learning effort and maximizing productivity. The GUI worked as an interface to employees while the back end accomplished runs of ADB commands and logged results.


Device type: Samsung Device


Android version: 13 & 14 are supported


The device must be enrolled with Real life user profile in EASE05 server

The PC must have python (including PIP) installed


# Components of the ADBbasedGUItool:

User initiates a test through the GUI Component in the beginning. Then GUI Component sends the selected command to the Command Processor. Then Command Processor creates the corresponding ADB command and the ADB Interface sends the command to the Android Device. Android Device executes the command successfully and returns the result. Then ADB Interface relays the result back to the Command Processor and Command Processor updates the GUI Component with the result. Finally, the results are sent to the Logger, and it records the successful execution for later analysis.


![Component Diagram of the designed prototype](https://github.com/user-attachments/assets/5891976d-e6c3-45a6-a5a7-197c52b6a9ba)


# Example of a specific case (sequence diagram)
Sequence diagram of the designed prototype for a specific test case. 

![Specific case Sequence diagram](https://github.com/user-attachments/assets/6c868a13-89eb-4793-a373-fa9024537b94)



At first, the user selects "Samsung Galaxy S22" from the "Select Device" dropdown in the GUI Component. Then he or she selects "Run Specific Test" from the "Select ADB Command" dropdown. After that, the user selects HubTest from the "Select Test Suite" dropdown and testSendReceive from the "Select Additional Test" dropdown. Then he or she clicks the "Execute Command" button and the GUI Component sends a final command to the Command Processor to execute the testSendReceive test on HubTest. The Command Processor constructs the ADB command to execute the testSendReceive test on the HubTest suite. The command might look something like: adb shell am instrument -w -e class com.blackberry.spl.functionaltest.test.specific.HubTest#testSendReceive com.blackberry.spl.functionaltest.test/androidx.test.runner.AndroidJUnitRunner. The Command Processor sends the generated ADB command to the ADB Interface. The ADB Interface connects to the " Samsung Galaxy S22" device and sends the command to execute the testSendReceive test. The Android Device runs the testSendReceive test as part of the HubTest suite. The test executes successfully and the Android device returns the result: "OK (1 test)" indicating success. The ADB Interface receives the success result and sends it back to the Command Processor. The Command Processor updates the GUI Component to show the successful execution of the testSendReceive test. The Command Processor sends detailed logs of the test execution to the Logger. The Logger records the success of the testSendReceive test for future reference and analysis.

# How to execute test:

Step 1: Enable the USB debugging of the testing device (Android, Samsung device)

Step 2: Install the functional test, Functional test debug and Test supporter in the testing device.

Step 3: Connect the device with PC with wire or wirelessly with Wifi.

Step 4: Run the script and check the device availability

Step 5: This UI window should appear after running the script

<img width="513" alt="1" src="https://github.com/user-attachments/assets/148ff32f-f6a9-4490-8184-bb4e0d477353">


Step 6: Now, we can select which test we want to execute.

<img width="513" alt="4" src="https://github.com/user-attachments/assets/29a98253-4f77-4c08-8936-9336f448f424">



