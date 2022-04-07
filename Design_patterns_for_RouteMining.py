import xlsxwriter
import pandas as pd
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
import urllib.request
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from tkinter import ttk


# This function returns the carrier route of an address that is input into it. It takes the street number, street name,
# apartment number if it exists, state and zipcode. It then sends an XML request to the USPS API and returns the carrier
# route
def getCarrierRoute(streetNo, streetName, apt, city, state, zipCode):
    cRoute = []

    requestXML = """
    <?xml version="1.0"?>
    <AddressValidateRequest USERID="XXXXXXXXXXXX">
        <Revision>1</Revision>
        <Address ID="0">
            <Address1>""" + streetNo + ' ' + streetName + """</Address1>
            <Address2>""" + apt + """</Address2>
            <City>""" + city + """</City>
            <State>""" + state + """</State>
            <Zip5>""" + zipCode + """</Zip5>
            <Zip4/>
        </Address>
    </AddressValidateRequest>
    """

    # print(requestXML)
    docString = requestXML
    docString = docString.replace('\n', '').replace('\t', '')
    docString = urllib.parse.quote_plus(docString)

    url = "http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=" + docString

    # If response code is not 200, then it's an error
    response = urllib.request.urlopen(url)
    if response.getcode() != 200:
        print("Error making HTTP call")
        print(response.info())
        exit()

    contents = response.read()

    root = ET.fromstring(contents)
    for address in root.findall('Address'):
        cRoute.append(address.find("CarrierRoute").text)

    return cRoute


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ADDRESS CLASS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Address class is a class implemented by the concrete decorators. Objects created from this class are meant to
# represent the addresses from the excel file
class AddressClass:
    def __init__(self):
        self.streetNumber = ''
        self.streetName = ''
        self.apartment = ''
        self.city = ''
        self.state = ''
        self.zipCode = ''

    def printAddress(self):
        return str(self.streetNumber) + ' ' + self.streetName + ' ' + str(self.apartment) + ', ' + self.city + ', ' + self.state + ' ' + str(self.zipCode)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DECORATOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This is an abstract class that is used to decorate the AddressClass with street number, street name, apartment, city
# and state values
class AddressDecorator(AddressClass):
    @abstractmethod
    def printAddress(self):
        pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONCRETE DECORATORS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This decorator decorates the address class with a specified street number
class StreetNumberDecorator(AddressDecorator):
    def __init__(self, addressObject, number):
        self.addressObject = addressObject
        self.streetNumber = number
        self.streetName = addressObject.streetName
        self.apartment = addressObject.apartment
        self.city = addressObject.city
        self.state = addressObject.state
        self.zipCode = addressObject.zipCode

    def printAddress(self):
        return str(self.streetNumber) + ' ' + self.streetName + ' ' + str(self.apartment) + ', ' + self.city + ', ' + self.state + ' ' + str(self.zipCode)


# This decorator decorates the address class with a specified street name
class StreetNameDecorator(AddressDecorator):
    def __init__(self, addressObject, name):
        self.addressObject = addressObject
        self.streetNumber = addressObject.streetNumber
        self.streetName = name
        self.apartment = addressObject.apartment
        self.city = addressObject.city
        self.state = addressObject.state
        self.zipCode = addressObject.zipCode

    def printAddress(self):
        return str(self.streetNumber) + ' ' + self.streetName + ' ' + str(self.apartment) + ', ' + self.city + ', ' + self.state + ' ' + str(self.zipCode)


# This decorator decorates the address class with a specified apartment number
class ApartmentDecorator(AddressDecorator):
    def __init__(self, addressObject, apartment):
        self.addressObject = addressObject
        self.streetNumber = addressObject.streetNumber
        self.streetName = addressObject.streetName
        self.apartment = apartment
        self.city = addressObject.city
        self.state = addressObject.state
        self.zipCode = addressObject.zipCode

    def printAddress(self):
        return str(self.streetNumber) + ' ' + self.streetName + ' ' + str(self.apartment) + ', ' + self.city + ', ' + self.state + ' ' + str(self.zipCode)


# This decorator decorates the address class with a specified city
class CityDecorator(AddressDecorator):
    def __init__(self, addressObject, city):
        self.addressObject = addressObject
        self.streetNumber = addressObject.streetNumber
        self.streetName = addressObject.streetName
        self.apartment = addressObject.apartment
        self.city = city
        self.state = addressObject.state
        self.zipCode = addressObject.zipCode

    def printAddress(self):
        return str(self.streetNumber) + ' ' + self.streetName + ' ' + str(self.apartment) + ', ' + self.city + ', ' + self.state + ' ' + str(self.zipCode)


# This decorator decorates the address class with a specified state
class StateDecorator(AddressDecorator):
    def __init__(self, addressObject, state):
        self.addressObject = addressObject
        self.streetNumber = addressObject.streetNumber
        self.streetName = addressObject.streetName
        self.apartment = addressObject.apartment
        self.city = addressObject.city
        self.state = state
        self.zipCode = addressObject.zipCode

    def printAddress(self):
        return str(self.streetNumber) + ' ' + self.streetName + ' ' + str(self.apartment) + ', ' + self.city + ', ' + self.state + ' ' + str(self.zipCode)


# This decorator decorates the address class with a specified zip code
class ZipDecorator(AddressDecorator):
    def __init__(self, addressObject, zipCode):
        self.addressObject = addressObject
        self.streetNumber = addressObject.streetNumber
        self.streetName = addressObject.streetName
        self.apartment = addressObject.apartment
        self.city = addressObject.city
        self.state = addressObject.state
        self.zipCode = zipCode

    def printAddress(self):
        return str(self.streetNumber) + ' ' + self.streetName + ' ' + str(self.apartment) + ', ' + self.city + ', ' + self.state + ' ' + str(self.zipCode)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ITERATOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This is an abstract class implemented by the AddressIterator class. Implementations of this class determine how the
# elements of a collection of addresses are be traversed
class Iterator(ABC):
    @abstractmethod
    def hasNext(self):
        pass

    @abstractmethod
    def next(self):
        pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONCRETE ITERATOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The address iterator is an implementation of the Iterator class that iterates over the collection of addresses
# sequentially. The collection in this case is a list and it goes over the list sequentially from start to finish
class AddressIterator(Iterator):
    i = -1

    # This method checks if the collection being iterated over has another element and returns True if it does.
    # Otherwise it returns False
    @staticmethod
    def hasNext():
        if AddressIterator.i < len(addrObjectList)-1:
            return True
        return False

    # This method applies the iteration technique (in this case, iterating sequentially over a list) to the next element
    # in the collection
    @staticmethod
    def next():
        if AddressIterator.hasNext():
            AddressIterator.i += 1
            return addrObjectList[AddressIterator.i]
        return None


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ITERABLE COLLECTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This abstract class is implemented by AddressRepository and is used to select the iterator that iterates over the
# collection of AddressClass objects
class Container(ABC):
    @abstractmethod
    def getIterator(self):
        pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONCRETE COLLECTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This implementation of the Container class uses the AdressIterator iterator as its iterator class
class AddressRepository(Container):
    @staticmethod
    def getIterator():
        return AddressIterator()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DIRECTOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The director is part of the builder design pattern and uses the builders' generateReport() methods to build and
# display the reports
class Director:
    @staticmethod
    def buildReport(concreteBuilder):
        concreteBuilder.generateReport()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BUILDER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This abstract class serves as the builder in the builder design pattern
class ReportBuilder(ABC):
    @abstractmethod
    def generateReport(self):
        pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONCRETE BUILDERS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# These concrete builders implement the builder abstract class. Report 1 generates a report using the Report 1 style,
# Report 2 generates a report using the report 2 style and Report 3 generatesa a bar chart report based on data shown in
# Report 2
class Report1(ReportBuilder):
    address_routeList = []
    # Create a repository instance of the AddressRepository class
    repository = AddressRepository()

    # This method generates Report 1
    @staticmethod
    def generateReport():
        # Get the iterator from repository instance
        iterator = Report1.repository.getIterator()

        # Initialize Tkinter GUI
        gui = tk.Tk()
        gui.title("Report 1")
        gui.geometry('500x500')
        frame = tk.Frame(gui, relief='sunken', height=450)
        frame.pack(padx=(50, 50), pady=(50, 50))
        frame2 = tk.Frame(gui, relief='sunken', bg="red", height=400)
        frame2.pack(padx=(50, 50), pady=(50, 50))
        report = ttk.Treeview(frame)
        report.pack()
        report['columns'] = ('address', 'carrier_route')
        report.column("#0", width=0, stretch='NO')
        report.column("address", anchor='center', width=300)
        report.column("carrier_route", anchor='center', width=80)
        report.heading("#0", text="", anchor='center')
        report.heading("address", text="Address", anchor='center')
        report.heading("carrier_route", text="Carrier Route", anchor='center')
        i = 0

        # while there is another element in repository's collection:
        while iterator.hasNext():
            # The address used for the rest of the loop is that next element
            currentAddress = iterator.next()

            # If there was no apartment specified in spreadsheet, make apartment spot blank, else, ensure apartment
            # number is a string
            if np.isnan(currentAddress.apartment): currentAddress.apartment = ''
            else: currentAddress.apartment = 'APT ' + str(int(currentAddress.apartment))

            # This try-except statement ensures that a carrier route is only found for valid addresses. If the address
            # is invalid, instead of producing an error, the address is ignored and the loop continues
            try:
                # Get the carrier route using getCarrierRoute() function and append it to the GUI
                cRoute = getCarrierRoute(str(currentAddress.streetNumber), currentAddress.streetName, currentAddress.apartment, currentAddress.city, currentAddress.state, str(currentAddress.zipCode))
                Report1.address_routeList.append([currentAddress.printAddress(), cRoute[0]])
                report.insert(parent='', index='end', iid=i, text='', values=(currentAddress.printAddress(), cRoute))
                i += 1
            except:
                continue

        # Add a button to the GUI that allows for exporting the report to an Excel spreadsheet using the export() method
        exportButton = tk.Button(frame2, text="Export to Excel", command=lambda: Report1.export())
        exportButton.pack()

        gui.mainloop()

    # This method is used to export the report data to Excel using the xlsxwriter library
    @staticmethod
    def export():
        workbook = xlsxwriter.Workbook('Report 1.xlsx')
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 0, 'Address')
        worksheet.write(0, 1, 'Carrier Route')
        row, col = 1, 0

        for address, croute in Report1.address_routeList:
            worksheet.write(row, col, address)
            worksheet.write(row, col + 1, croute)
            row += 1

        workbook.close()


class Report2(ReportBuilder):
    route_freqList = []
    # Create a repository instance of the AddressRepository class
    repository = AddressRepository()

    # This method generates Report 2
    @staticmethod
    def generateReport():
        iterator = Report2.repository.getIterator()
        reportDict = {}

        # Initialize Tkinter GUI
        gui = tk.Tk()
        gui.title("Report 2")
        gui.geometry('500x500')
        frame = tk.Frame(gui, relief='sunken', height=450)
        frame.pack(padx=(50, 50), pady=(50, 50))
        frame2 = tk.Frame(gui, relief='sunken', height=400)
        frame2.pack(padx=(50, 50), pady=(50, 50))
        report = ttk.Treeview(frame)
        report.pack()
        report['columns'] = ('carrier_route', 'no_of_addr')
        report.column("#0", width=0, stretch='NO')
        report.column("carrier_route", anchor='center', width=80)
        report.column("no_of_addr", anchor='center', width=150)
        report.heading("#0", text="", anchor='center')
        report.heading("carrier_route", text="Carrier Route", anchor='center')
        report.heading("no_of_addr", text="Number of Addresses", anchor='center')
        i = 0

        # while there is another element in repository's collection:
        while iterator.hasNext():
            # The address used for the rest of the loop is that next element
            currentAddress = iterator.next()

            # If there was no apartment specified in spreadsheet, make apartment spot blank, else, ensure apartment
            # number is a string
            if np.isnan(currentAddress.apartment): currentAddress.apartment = ''
            else: currentAddress.apartment = 'APT ' + str(int(currentAddress.apartment))

            # This try-except statement ensures that a carrier route is only found for valid addresses. If the address
            # is invalid, instead of producing an error, the address is ignored and the loop continues
            try:
                cRoute = getCarrierRoute(str(currentAddress.streetNumber), currentAddress.streetName, currentAddress.apartment, currentAddress.city, currentAddress.state, str(currentAddress.zipCode))

                # This try-except statement makes sure that the dictionary, which keeps count of the number of times
                # each carrier route is found, only increments the carrier route's value if the carrier route only
                # exists in the dictionary. If it doesn't exist, instead of raising a KeyError, it adds the carrier
                # route to the dictionary as a key
                try:
                    reportDict[cRoute[0]] += 1
                except:
                    reportDict[cRoute[0]] = 1
            except:
                continue

        # Append the carrier route and it's value (apperenace frequency) to the GUI
        for key in reportDict:
            Report2.route_freqList.append([key, reportDict[key]])
            report.insert(parent='', index='end', iid=i, text='', values=(key, reportDict[key]))
            i += 1

        # Add a button to the GUI that allows for exporting the report to an Excel spreadsheet using the export() method
        exportButton = tk.Button(frame2, text="Export to Excel", command=lambda: Report2.export())
        exportButton.pack()

        gui.mainloop()

    # This method is used to export the report data to Excel using the xlsxwriter library
    @staticmethod
    def export():
        print("Exporting")
        workbook = xlsxwriter.Workbook('Report 2.xlsx')
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 0, 'Carrier Route')
        worksheet.write(0, 1, 'Number of Addresses')
        row, col = 1, 0

        for croute, addr in Report2.route_freqList:
            worksheet.write(row, col, croute)
            worksheet.write(row, col + 1, addr)
            row += 1

        workbook.close()


class Report3(ReportBuilder):
    # Create a repository instance of the AddressRepository class
    repository = AddressRepository()

    # This method generates Report 3
    @staticmethod
    def generateReport():
        iterator = Report3.repository.getIterator()
        reportDict = {}

        while iterator.hasNext():
            currentAddress = iterator.next()

            if np.isnan(currentAddress.apartment): currentAddress.apartment = ''
            else: currentAddress.apartment = 'APT ' + str(int(currentAddress.apartment))

            # This try-except statement ensures that a carrier route is only found for valid addresses. If the address
            # is invalid, instead of producing an error, the address is ignored and the loop continues
            try:
                cRoute = getCarrierRoute(str(currentAddress.streetNumber), currentAddress.streetName, currentAddress.apartment, currentAddress.city, currentAddress.state, str(currentAddress.zipCode))

                # This try-except statement makes sure that the dictionary, which keeps count of the number of times
                # each carrier route is found, only increments the carrier route's value if the carrier route only
                # exists in the dictionary. If it doesn't exist, instead of raising a KeyError, it adds the carrier
                # route to the dictionary as a key
                try:
                    reportDict[cRoute[0]] += 1
                except:
                    reportDict[cRoute[0]] = 1
            except:
                continue

        # Create bar chart
        xAxis, yAxis = [], []
        for key in reportDict:
            xAxis.append(key)
            yAxis.append(reportDict[key])
        plt.bar(xAxis, yAxis)
        plt.title('Number of Addresses for each Carrier Route')
        plt.xlabel('Carrier Route')
        plt.ylabel('Number of Addresses')
        plt.show()


# Read the excel file where the addresses are stored called 'adresses.xlsx' to a pandas dataframe and convert dataframe
# to NumPy array
df = pd.read_excel(r'adresses.xlsx')
addressList = df.to_numpy()

# For each address in the excel file, create an instance of AddressClass with values from the address in the excel file,
# then append the object to the addrObjectList list
addrObjectList = []
for i in range(0, len(addressList)):
    addrObject = AddressClass()
    addrObject = StreetNumberDecorator(addrObject, addressList[i][0])
    addrObject = StreetNameDecorator(addrObject, addressList[i][1])
    addrObject = ApartmentDecorator(addrObject, addressList[i][2])
    addrObject = CityDecorator(addrObject, addressList[i][3])
    addrObject = StateDecorator(addrObject, addressList[i][4])
    addrObject = ZipDecorator(addrObject, addressList[i][5])
    addrObjectList.append(addrObject)

# Create director and instances of concrete builders (Builder design pattern)
myDirector = Director()
report1 = Report1()
report2 = Report2()
report3 = Report3()

# Ask user for what report they wish to see
reportStyle = input("Which report would you like to see? (Report 1, Report 2 or Report 3). Type 'exit' to end. ")

# Depending on what report is requested, build and display that report using the director. Or tell user that they selected an invalid report type
while True:
    if reportStyle == 'Report 1':
        myDirector.buildReport(report1)
        break
    elif reportStyle == 'Report 2':
        myDirector.buildReport(report2)
        break
    elif reportStyle == 'Report 3':
        myDirector.buildReport(report3)
        break
    elif reportStyle == 'exit':
        break
    else:
        print("Invalid Report Type")
        reportStyle = input("Which report would you like to see? (Report 1, Report 2 or Report 3) ")



