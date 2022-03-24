from abc import ABC, abstractmethod


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PRODUCT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Page(ABC):
    @abstractmethod
    def getPageName(self):
        pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONCRETE PRODUCTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class educationPage(Page):
    @staticmethod
    def getPageName():
        print("Education Page")


class experiencePage(Page):
    @staticmethod
    def getPageName():
        print("Experience Page")


class resultsPage(Page):
    @staticmethod
    def getPageName():
        print("Results Page")


class conclusionPage(Page):
    @staticmethod
    def getPageName():
        print("Conclusion Page")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CREATOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Document(ABC):
    Pages = []

    @abstractmethod
    def createPages(self):
        pass

    @abstractmethod
    def getDocName(self):
        pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONCRETE CREATORS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Resume(Document):
    @staticmethod
    def createPages():
        Document.Pages.append(educationPage)
        Document.Pages.append(experiencePage)

    @staticmethod
    def getDocName():
        print("Resume")


class Report(Document):
    @staticmethod
    def createPages():
        Document.Pages.append(resultsPage)
        Document.Pages.append(conclusionPage)

    @staticmethod
    def getDocName():
        print("Report")


doc = []
doc.append(Resume())
doc[0].createPages()
doc[0].getDocName()
for page in doc[0].Pages:
    page.getPageName()