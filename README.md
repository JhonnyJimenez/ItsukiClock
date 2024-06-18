Digital clock with a YuYuYu Itsuki image-shaped window as Rainmeter skin alternative (Because I used Rainmeter only for this).

Requires python, pywin32 and PyQt6.7.0

I am pretty sure that it is cross-platform, but I can't guarantee it will stay on screen for any os other than Windows 10. For avoid minimize, this clock uses ctype, win32gui and win32com. That makes this clock doesn't work if Clock.pyw is not executed with Admin Privileges.

For any customization, edit Clock.pyw. I put options for that at top of code.

**IMPORTANT**: Before running clock, modify the image path (if you want use Itsuki image, you just need to delete 'YuYuYu/' from path in code, or make directory and put image in). This will prevent the clock from running without an image. This clock only can be closed by Alt + F4 or ending the process in the task manager because **it does not have a window with buttons, taskbar icon or tray icon**.

![Captura de pantalla (18)](https://github.com/JhonnyJimenez/ItsukiClock/assets/118622515/266ee42d-af05-4313-8648-68c954f7e6e9)
