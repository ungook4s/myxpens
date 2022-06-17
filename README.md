These are automation tool to help to update expense report.

# run_attendee.bat
Attach attendee on every "Business Meals (Staff Only)"<br>
Ensure that meal expenses are modified to "Business Meals (Staff Only)" before excuting the programs.

# run_mileage.bat 
Create Mileage Expense using csv file. (Map can be attached.). Below steps needs to be configured at first time.
1. Vehicle Id should be set "Long" and "Short"
2. Put the records in mileage.csv

# run_city.bat
Updates "City of Purchase" and "Business Purpose" if the expense misses the one of information.

# prerequisite
There are few stpes to be done before running programs
1. locate the right version of chromedriver.exe in https://chromedriver.chromium.org/downloads
    (refer link https://www.businessinsider.com/what-version-of-google-chrome-do-i-have in order to check the verion of chrome.) 
2. install python using https://docs.microsoft.com/ko-kr/windows/python/beginners
3. install python libraries <br>
3.1. Open command console <br>
3.2. type "pip install selenium" <br>
3.3. type "pip install pyautogui"
4. Update config.ini 
