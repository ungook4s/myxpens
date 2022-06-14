import configparser as parser
import sys

# ----------------------------------------------------------------------------------
# Input
# ----------------------------------------------------------------------------------
# mileage.csv
# seperator: tab
# File  Date          from    to      vehicle distance    comment
# Home.png  05/02/2022	Home	HKMC	Short	100
properties = parser.ConfigParser()
properties.read('./config.ini')

imgDir = properties['CONFIG']['image_dir']

# ----------------------------------------------------------------------------------
# functions
# ----------------------------------------------------------------------------------
def newExpense(tranDate, fromLoc, toLoc, vehicleId, distance, comment, filepath):
    waitXpath("Wait", "//span[@data-trans-id='Expense.addExpense']")
    time.sleep(1) # require break, otherwise error will happend which requires login again TT

    clickXpath("Add Expense", "//span[@data-trans-id='Expense.addExpense']")

    clickXpath("Personal Car Mileage", "//span[text()='Personal Car Mileage']")

    time.sleep(0.3)

    xpath = "//input[@name='transactionDate']"
    sendKeys("Send keys Ctrl+a", xpath, Keys.CONTROL + "a")
    sendKeys("Send keys DEL", xpath, Keys.DELETE)
    sendKeys("Send keys {tranDate}}", xpath, tranDate)

    sendKeys("Send keys {fromLoc}", "//input[@name='fromLocation']", fromLoc)

    sendKeys("Send keys {toLoc}", "//input[@name='toLocation']", toLoc)

    clickXpath("VehicleId Combo", "//div[@data-nuiexp='field-carKey']")

    clickXpath(f"VehicleId {vehicleId}", f"//li/span[text()='{vehicleId}']")

    xpath = "//input[@name='businessDistance']"
    sendKeys("Send keys Ctrl+a", xpath, Keys.CONTROL + "a")
    sendKeys("Send keys DEL", xpath, Keys.DELETE)
    sendKeys("Send keys distance", xpath, distance)
    sendKeys("Send keys comment", "//textarea[@name='comment']", comment)


    time.sleep(1)

    # Update image
    clickXpath("Show Reciept", "//button[@aria-controls='entry-receipts']")

    clickXpath("Upload Receipt Image", "//a[@data-nuiexp='attach-receipt-modal-button']")

    sleep(1)

    clickXpath("Upload Image", "(//a[@class='sapcnqr-card__button'])[2]")

    sleep(1)

    subprocess.check_call([r"fileopen.exe", filepath])

    sleep(3)

    waitXpath("Wait page is loaded after attaching image", "//div[@class='receipt-image-zoom-container']")
    waitXpath("Wait page is loaded: Deatch", "//span[@data-trans-id='receipt.detach']")

    sleep(2)

    clickXpath("Save Expense", "//span[@data-trans-id='expenseEntry.saveExpense']")

    time.sleep(2)


# ----------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------
exec(open('login.py').read())

with open('mileage.csv', 'r') as csvfile:
    f = csv.reader(csvfile, delimiter='\t', lineterminator="\r\n")
    lineno = 0;
    for values in f:
        lineno += 1
        comment = ""

        if (len(values) == 0) : continue

        if (len(values) == 1) : 
            if values[0].startswith("#") : continue

        if (len(values) < 6 or len(values) > 7) :
            print(f"Content of csv file is not proper. Line {lineno}: {values}" )
            print("Exmaple row is following" )
            print("File 05/02/2022	Home	HKMC	Short	100" )
            sys.exit()
        elif (len(values) == 7 ):
            filename, trDate, fromLoc, toLoc, vehicleId, distance, comment = values
        elif (len(values) == 6 ):
            filename, trDate, fromLoc, toLoc, vehicleId, distance = values

        distance = distance.strip()
        comment = comment.strip()

        filepath = f"{imgDir}\\{filename}"

        print(trDate, fromLoc, toLoc, vehicleId, distance, comment, filepath)
        newExpense(trDate, fromLoc, toLoc, vehicleId, distance, comment, filepath)
        
print("Job is complete")
