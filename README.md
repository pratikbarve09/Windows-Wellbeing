# Windows Wellbeing
Windows-Wellbeing is simple application which can be used to track of apps and softwares that we use daily. It is similar to Digital Wellbeing but made for Windows. 
For storing data, json file is used. Script generates json file named `tracker.json` where it stores its all data.
`tracker.json` file will get created in dist folder from from project's root directory.

## How script works:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;After running script, it checks if `tracker.json` file is present. If not, then it creates new file. If file is present, but it's empty or has some issue with file, then it rewrites that file with template present in code. 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Afterwards loop is executed in which script collects currently focused app and then adds sleep timer of 60 seconds. Afterwards, again current focused app name is collected. If previous and current name matches, then it adds that app to foreground category, else adds to background apps category. Script will also auto-delete old stats with condition days>10
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
* #### To compile project into executable files:
    1.  To create script executable:
        ``` 
        pyinstaller --onefile script.py --name Wellbeing
        ```
    2. To create main ui executable:
        ```
        pyinstaller app.spec
        ```
    
    
    Cheers!! :clinking_glasses:
    Now double-click `Runner.vbs` file from file explorer and it will start `WindowsWellbeing.exe` file without opening command prompt.<br/>
    :pushpin:After starting `Wellbeing.exe` through `Runner.vbs`, `tracker.json` file will get created in the same directory as that of `Wellbeing.exe`.<br/>
    Now You can see task manager shows that `Wellbeing.exe` is running in background. After this you can continue with your work and script will note your timing with each app untill it gets interrupted.
    ###### In order to view your usage, open `tracker.json` present in `dist` directory. (Opening with VS code shows live changes happening to file)

* #### To run this process automatically at startup:
    In order to run this process in background at startup instead of manually starting `Runner.vbs` everytime you log on to computer, we need to use `Windows Task Scheduler`.

    ##### Steps to follow:
    - Open `Windows Task Scheduler`.
    - Right-click `Task Scheduler Library` and add New folder(if you want to search this schedule task quicker) and give proper name to that folder.
    - Double-click on that folder and then go to `Action->Create Task`.
    - Create Task dialogue box will open
    - In `General` section, give any name and description
    - In security options, click on `Run only when user is logged on`
    - Under `Configure for` section, choose Windows 10
    - Inside `Triggers` section, click new.
    - In `Begin the task` choose `On workstation unlock` and tick for `any user`.In settings, click last option `Enabled`.
    - In `Actions` tab, click new and then make sure `Start a program` is selected under `Action`. In program/script, add `Runner.vbs` file full-path. Leave  `add arguments` empty and inside `Start in (optional)` add directory path of your `Runner.vbs` file with "\\" at end.
    - In `Conditions` tab, inside `Power` section, untick both `stop if computer switches to battery power` and `start the task only if computer is on AC power`. Also tick `Wake the computer to run this task`. Now hit `Ok`.

##### After compilation dist folder will contain 2 files: 
* compiled gui file named `app.exe`
* compiled background script file named `Wellbeing.exe`
* `tracker.json` file
    
 Congrats!!You scheduled this task to run automatically everytime computer boots up. :tada:
 But if you want to run task manually if its not started,then open task in task scheduler and right-click on taskname and choose `Run`. 
 If you want to stop this task which is running in background, Open `Task manager` and inside `Background Process`, find your task and right-click on it and choose `End task` and remove all instances of it.
