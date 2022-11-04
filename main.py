"""
# Prerequisites:
pip3 install pywin32 pyinstaller

# Build:
pyinstaller.exe --onefile --runtime-tmpdir=. --hidden-import win32timezone myservice.py

# With Administrator privilges
# Install:
dist\myservice.exe install

# Start:
dist\myservice.exe start

# Install with autostart:
dist\myservice.exe --startup delayed install

# Debug:
dist\myservice.exe debug

# Stop:
dist\myservice.exe stop

# Uninstall:
dist\myservice.exe remove


"""

import time
import sys
import logging


import win32serviceutil  # ServiceFramework and commandline helper
import win32service  # Events
import servicemanager  # Simple setup and logging

logging.basicConfig(level=logging.INFO, filename=${logPath}, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class MyService:
    """Silly little application stub"""
    def stop(self):
        """Stop the service"""
        self.running = False

    def run(self):
        """Main service loop. This is where work is done!"""
        self.running = True
        i = 0
        while self.running:
            time.sleep(10)  # Important work
            logging.info('Add log')
            i += 1
            if i == 10:
                self.running = False


class MyServiceFramework(win32serviceutil.ServiceFramework):

    _svc_name_ = 'MyService'
    _svc_display_name_ = 'My Service display name'

    def SvcStop(self):
        """Stop the service"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.service_impl.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        """Start the service; does not return until stopped"""
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.service_impl = MyService()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        # Run the service
        self.service_impl.run()


def init():
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyServiceFramework)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyServiceFramework)


if __name__ == '__main__':
    init()