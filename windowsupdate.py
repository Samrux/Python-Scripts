import traceback
from winreg import *

WindowsUpdate = r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate"
AU = WindowsUpdate + r"\AU"


print('Windows Update configuration (Windows 10 Pro and up)\n')
print('0 -> Change setting in Windows Update app (default)')
print('1 -> Never check for updates')
print('2 -> Notify before download and install')
print('3 -> Auto download and notify for install')
print('4 -> Auto download and schedule the install')

while True:
    try:
        choice = int(input('Enter your choice: '))
        assert 0 <= choice <= 4
    except (ValueError, AssertionError):
        continue
    else:
        break

try:
    try: DeleteKeyEx(HKEY_LOCAL_MACHINE, AU, KEY_ALL_ACCESS, 0)
    except FileNotFoundError: pass
    try: DeleteKeyEx(HKEY_LOCAL_MACHINE, WindowsUpdate, KEY_ALL_ACCESS, 0)
    except FileNotFoundError: pass

except (PermissionError, WindowsError):
    input('\nPermission denied. Please run this program as Administrator.')

else:
    try:
        CreateKeyEx(HKEY_LOCAL_MACHINE, WindowsUpdate, 0, KEY_ALL_ACCESS)
        CreateKeyEx(HKEY_LOCAL_MACHINE, AU, 0, KEY_ALL_ACCESS)

        with OpenKey(HKEY_LOCAL_MACHINE, AU, 0, KEY_ALL_ACCESS) as key:
            if choice == 1:
                SetValueEx(key, 'NoAutoUpdate', 0, REG_DWORD, 1)
            elif choice != 0:
                SetValueEx(key, 'NoAutoUpdate', 0, REG_DWORD, 0)
                SetValueEx(key, 'AUOptions', 0, REG_DWORD, choice)
                SetValueEx(key, 'ScheduledInstallDay', 0, REG_DWORD, 6)
                SetValueEx(key, 'ScheduledInstallTime', 0, REG_DWORD, 3)

    except Exception:
        print('\nProcess failed through the following unhandled exception:')
        traceback.print_exc()
        input('Sorry about that.')
    else:
        input('\nWindows Update settings changed successfully.')
