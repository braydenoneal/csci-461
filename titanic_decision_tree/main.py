from appJar import gui
import csv

from decision_tree import DecisionTree


class MainGui:
    def __init__(self):
        self.appGui = gui()
        self.dt = DecisionTree()
        self.data: list[dict] = []
        self.attributes: dict.keys = []

    # add & configure widgets
    def configure(self):
        self.appGui.addLabelFileEntry("CSV File")
        self.appGui.addButtons(["Read File", "Build Decision Tree", "Test Decision Tree"], self.button_press)

    # configure window and start
    def start(self):
        self.configure()
        self.appGui.go()

    # event handler for button presses
    def button_press(self, button):
        if button == "Read File":
            self.read_file(self.appGui.getEntry("CSV File"))
            self.attributes = self.data[0].keys()

        # TODO: handle the other events
        elif button == "Build Decision Tree":
            print("Building decision tree")

        elif button == "Test Decision Tree":
            print("Testing decision tree")

    # read the comma-separated data file and store the contents
    def read_file(self, file_name):
        with open(file_name) as csvfile:
            reader = csv.DictReader(csvfile, ["pclass", "survived", "name", "sex", "age", "sibsp", "parch",
                                              "ticket", "fare", "cabin", "embarked", "boat", "body", "home.dest"])

            for row in reader:
                self.data.append(row)

        print(self.data)


# Start the GUI if this is the main script
if __name__ == '__main__':
    app = MainGui()
    app.start()
