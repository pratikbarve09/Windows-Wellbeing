# Windows Wellbeing
Windows-Wellbeing is simple commandline based application which can be used to track of apps and softwares that we use daily. It is similar to digital wellbeing but made for Windows. 
For storing data, json file is used. Script generates json file named `tracker.json` where it stores its all data.
`tracker.json` file will get created in same folder from where script is running in terminal.

## How script works:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;After running script, it checks if `tracker.json` file is present. If not, then it creates new file. If file is present, but it's empty or has some issue with file, then it rewrites that file with template present in code. 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Afterwards loop is executed in which script collects currently focused app and then adds sleep timer of 60 seconds. Afterwards, again current focused app name is collected. If previous and current name matches, then it adds that app to foreground category, else adds to background apps category.
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Now to get list of apps running in background (which are not in focus or lost focus within 1 minute sleep time) script uses powershell command and lists all apps running(foreground and background). Then script tries to find app (if it was having focus in 1 minute period) and because it has incremented timer for that app in foreground apps category, script tries to find similar app with same name like focused app and that app is removed from list. 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Afterwards all the apps present in that list are added and incremented in background apps category.  

### Get started:
* #### To clone repository:
    ```
    git clone https://github.com/pratik0903/Windows-Wellbeing.git
    ```

* #### To setup project with all dependencies:
    ```
    pip install -r requirements.txt
    ```
* #### To compile into Executable file:
    I used `auto-py-to-exe` python package for compiling this file.<br/>
    <img src="images/auto-py-to-exe.png" alt="auto-py-to-exe settings screenshot" width="500"/><br/>
    you will see Complete status in the end.

* #### To run newly created exe file without opening terminal window
    In project directory, inside `Runner.vbs`, add your executable file path inside `Shell.Run` command.

    ```VBScript
        Shell.Run """{YOUR-ExecutableFile-PATH}""", 0, False
    ```
    
    Cheers!! :clinking_glasses:
    Now double-click `Runner.vbs` file from file explorer and it will start `WindowsWellbeing.exe` file without opening command prompt.<br/>
    :pushpin::pushpin::pushpin:
    After starting `WindowsWellbeing.exe` through `Runner.vbs`, `tracker.json` file will get created in the same directory as that of `Runner.vbs`.<br/>
    As you can see task manager shows that `WindowsWellbeing.exe` is running in background.<br/>
    <img src="images/taskmanagerScreenShot.png" alt="Task Manager screenshot" width="500"/><br/>
    Now you can continue with your work and script will note your timing with each app.
    
    

