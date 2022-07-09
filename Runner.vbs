'Set Shell = CreateObject("WScript.Shell")
'put your exe file location here, mine is created in output folder inside project directory, with name WindowsWellbeing.exe
'Shell.Run """output\WindowsWellbeing.exe""", 0, False

Dim Shell
Set Shell = WScript.CreateObject("WScript.Shell")
' Shell.CurrentDirectory = ".\dist"
Shell.Run """dist\script.exe""", 0, False
Set Shell = Nothing