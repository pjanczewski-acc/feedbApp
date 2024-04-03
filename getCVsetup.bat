@ECHO OFF
start iexplore.exe https://ts.accenture.com/sites/Warsaw-Analytics/SitePages/Home.aspx 
echo 'Sync' Warsaw Analytics using the button over the folder list in the IE window
msg "%username%" 'Sync' Warsaw Analytics using the button over the folder list in the IE window, then return to the cmd window
Pause
C:\Users\%USERNAME%\Anaconda3\Scripts\activate.bat
if %errorlevel% neq 0 (
start iexplore.exe https://www.anaconda.com/products/distribution
msg "%username%" Anaconda run failed, please ensure you have it installed and it is in C:\Users\%USERNAME\Anaconda3\. If you don't have it all - please install it. If you have it - use Notepad to adjust Anaconda paths in both getCV bat files, since cmd might be unable to locate it automatically.
) else (
C:\Users\%USERNAME%\Anaconda3\Scripts\activate.bat & pip install pip==21.2.4 & C:\Users\%USERNAME%\Anaconda3\python.exe "C:\Users\%USERNAME%\Accenture\Warsaw Analytics - Documents\01_CVs\CVapp\CVapp_setup.py")
Pause
