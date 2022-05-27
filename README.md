These are python script to help expense report on Concur.
There are few stpes to be done before running it.
1. locate the right version of chromedriver.exe in https://chromedriver.chromium.org/downloads
    (refer link https://www.businessinsider.com/what-version-of-google-chrome-do-i-have in order to check the verion of chrome.) 
2. install python using https://docs.microsoft.com/ko-kr/windows/python/beginners
3. install selenium library <br>
3.1. Open command console <br>
3.2. type "pip install selenium"
4. Update config.ini 

Now, you're ready to run the following script. 
Ensure that meal expense are modified to "Business Meals (Staff Only)" before excuting the programs.

# attendee.py
Attach atendee on "Business Meals (Staff Only)"
# city.py
It updates "City of Purchase" and "Business Purpose" if the expense misses the one of information.
# mileage.py
1. Vehicle Id should be set "Long" and "Short"
2. put the record in mileage.csv
