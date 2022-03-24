from abc import ABC, abstractmethod


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Abstract Products ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class panel(ABC):
    @abstractmethod
    def testPanel(self):
        pass


class button(ABC):
    @abstractmethod
    def testButton(self):
        pass


class textBox(ABC):
    @abstractmethod
    def testTextBox(self):
        pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Concrete products: Panels ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class panel90(panel):
    @staticmethod
    def testPanel():
        print("Panel Word90")


class panel00(panel):
    @staticmethod
    def testPanel():
        print("Panel Word00")


class panel10(panel):
    @staticmethod
    def testPanel():
        print("Panel Word10")


class panel22(panel):
    @staticmethod
    def testPanel():
        print("Panel Word22")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Concrete products: Buttons ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class button90(button):
    @staticmethod
    def testButton():
        print("Button Word90")


class button00(button):
    @staticmethod
    def testButton():
        print("Button Word00")


class button10(button):
    @staticmethod
    def testButton():
        print("Button Word10")


class button22(button):
    @staticmethod
    def testButton():
        print("Button Word22")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Concrete products: Textbox ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class textBox90(textBox):
    @staticmethod
    def testTextBox():
        print("TextBox Word90\n")


class textBox00(textBox):
    @staticmethod
    def testTextBox():
        print("TextBox Word00\n")


class textBox10(textBox):
    @staticmethod
    def testTextBox():
        print("TextBox Word10\n")


class textBox22(textBox):
    @staticmethod
    def testTextBox():
        print("TextBox Word22\n")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Abstract Factory ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class wordProcessor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def createPanel(self):
        pass

    @abstractmethod
    def createButton(self):
        pass

    @abstractmethod
    def createTextBox(self):
        pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Concrete Factory classes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class word90(wordProcessor):
    # Insert Singleton here
    instanceCount = 0

    def __init__(self):
        word90.instanceCount += 1
        if word90.instanceCount > 2:
            raise Exception("There are already two instances of the Word 90 word processors")

    @staticmethod
    def createPanel():
        return panel90()

    @staticmethod
    def createButton():
        return button90()

    @staticmethod
    def createTextBox():
        return textBox90()


class word00(wordProcessor):
    instanceCount = 0

    if instanceCount < 2:
        def __init__(self):
            word00.instanceCount += 1
            # if word00.instanceCount > 2:
                # Raises exception if more than two instances of the class
                # raise Exception("There are already two instances of the Word 00 word processors")

    @staticmethod
    def createPanel():
        return panel00()

    @staticmethod
    def createButton():
        return button00()

    @staticmethod
    def createTextBox():
        return textBox00()


class word10(wordProcessor):
    instanceCount = 0

    def __init__(self):
        word10.instanceCount += 1
        if word10.instanceCount > 2:
            raise Exception("There are already two instances of the Word 10 word processors")

    @staticmethod
    def createPanel():
        return panel10()

    @staticmethod
    def createButton():
        return button10()

    @staticmethod
    def createTextBox():
        return textBox10()


class word22(wordProcessor):
    instanceCount = 0

    def __init__(self):
        word22.instanceCount += 1
        if word22.instanceCount > 2:
            raise Exception("There are already two instances of the Word 22 word processors")

    @staticmethod
    def createPanel():
        return panel22()

    @staticmethod
    def createButton():
        return button22()

    @staticmethod
    def createTextBox():
        return textBox22()


class client:
    Panel = panel
    Button = button
    TextBox = textBox
    classInstances = 0

    def __init__(self, wp: wordProcessor):
        client.classInstances = wp.instanceCount
        if client.classInstances > 2:
            print("Class already has two instances")
        else:
            client.Panel = wp.createPanel()
            client.Button = wp.createButton()
            client.TextBox = wp.createTextBox()

    @staticmethod
    def run():
        if client.classInstances > 2:
            return
        else:
            client.Panel.testPanel()
            client.Button.testButton()
            client.TextBox.testTextBox()


# Getting inputs from configuration text file
processorList =[]
with open('abstract_factory_config.txt') as config:
    for line in config:
        processorList.append(line.strip())


for processor in processorList:
    if processor == 'Word90':
        wordPcr = word90()
    elif processor == 'Word00':
        wordPcr = word00()
    elif processor == 'Word10':
        wordPcr = word10
    elif processor == 'Word22':
        wordPcr = word22
    else:
        print("Invalid input\n")

    c1 = client(wordPcr)
    c1.run()
