from winreg import *
from traceback import print_exc as printexception


WindowsUpdate = r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate"
AU = WindowsUpdate + r"\AU"

NoAutoUpdate = 'NoAutoUpdate'
AUOptions = 'AUOptions'
ScheduledInstallDay = 'ScheduledInstallDay'
ScheduledInstallTime = 'ScheduledInstallTime'


def check_setting():
    try:
        with OpenKeyEx(HKEY_LOCAL_MACHINE, AU, 0, KEY_READ) as key:
            try:
                noautoupdate = QueryValueEx(key, NoAutoUpdate)[0]
            except FileNotFoundError:
                noautoupdate = False

            if noautoupdate:
                print('Your machine is on setting "1"')
            else:
                auoption = QueryValueEx(key, AUOptions)[0]
                if 2 <= auoption <= 4:
                    print('Your machine is on setting "%i"' % auoption)
                else:
                    print('Your machine is on an unrecognized setting')

    except FileNotFoundError:  # If either the key or AUOptions doesn't exist
        print('Your machine is on the default setting ("0")')

    print()


def set_setting(s):
    try:
        try: DeleteKeyEx(HKEY_LOCAL_MACHINE, AU, KEY_ALL_ACCESS, 0)
        except FileNotFoundError: pass
        try: DeleteKeyEx(HKEY_LOCAL_MACHINE, WindowsUpdate, KEY_ALL_ACCESS, 0)
        except FileNotFoundError: pass

        CreateKeyEx(HKEY_LOCAL_MACHINE, WindowsUpdate, 0, KEY_ALL_ACCESS)
        CreateKeyEx(HKEY_LOCAL_MACHINE, AU, 0, KEY_ALL_ACCESS)

        with OpenKey(HKEY_LOCAL_MACHINE, AU, 0, KEY_ALL_ACCESS) as key:
            if s == 1:
                SetValueEx(key, 'NoAutoUpdate', 0, REG_DWORD, 1)
            elif s != 0:
                SetValueEx(key, 'NoAutoUpdate', 0, REG_DWORD, 0)
                SetValueEx(key, 'AUOptions', 0, REG_DWORD, s)
                SetValueEx(key, 'ScheduledInstallDay', 0, REG_DWORD, 6)
                SetValueEx(key, 'ScheduledInstallTime', 0, REG_DWORD, 3)

    except PermissionError:
        print('\nPermission denied. Please run this program as Administrator.')
    else:
        print('\nWindows Update settings changed successfully.')


def main():
    print('Windows Update configuration (Windows 10 Pro and up)\n')
    print('0 -> As guided by the Windows Update app (default)')
    print('1 -> Never check for updates')
    print('2 -> Notify before download and install')
    print('3 -> Auto download and notify for install')
    print('4 -> Auto download and schedule the install')
    print('check -> See which configuration is selected on your machine.\n')

    while True:
        choice = input('Enter your choice: ')
        if choice == 'check':
            check_setting()
        else:
            try:
                choice = int(choice)
                assert 0 <= choice <= 4
            except (ValueError, AssertionError):
                continue

            try:
                set_setting(choice)
            except Exception:
                print('\nSorry. The process failed through the following unhandled exception:')
                printexception()
            break

    input('Press any key to exit...')


if __name__ == '__main__':
    main()