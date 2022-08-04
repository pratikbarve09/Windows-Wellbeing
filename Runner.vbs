'Set Shell = CreateObject("WScript.Shell")
'put your exe file location here, mine is created in output folder inside project directory, with name WindowsWellbeing.exe
'Shell.Run """output\WindowsWellbeing.exe""", 0, False

Dim Shell
Const strComputer = "." 
  Dim objWMIService, colProcessList
  Set objWMIService = GetObject("winmgmts:" & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")
  Set colProcessList =  objWMIService.ExecQuery("SELECT * FROM Win32_Process WHERE Name = 'Wellbeing.exe'")
  For Each objProcess in colProcessList 
    objProcess.Terminate() 
  Next  
Set Shell = WScript.CreateObject("WScript.Shell")
Shell.Run """dist\Wellbeing.exe""", 0, False
Set Shell = Nothing