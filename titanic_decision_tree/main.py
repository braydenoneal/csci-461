from appJar import gui
import csv

from decision_tree import DecisionTree

column_names = ['pclass', 'survived', 'name', 'sex', 'age', 'sibsp', 'parch', 'ticket', 'fare', 'cabin', 'embarked',
                'boat', 'body', 'home.dest']
train_file = 'input/titanic_train.csv'
test_file = 'input/titanic_test.csv'


class MainGui:
    def __init__(self):
        self.appGui = gui()
        self.dt = DecisionTree()
        self.attributes: dict.keys = []
        self.training_set: list[dict] = []
        self.test_set: list[dict] = []

    def configure(self):
        self.appGui.addButtons(['Build Decision Tree', 'Test Decision Tree'], self.button_press)

    def start(self):
        self.configure()
        self.appGui.go()

    def button_press(self, button):
        if button == 'Build Decision Tree':
            with open(train_file) as csvfile:
                reader = csv.DictReader(csvfile, column_names)

                first_row: dict = next(reader)
                self.attributes = first_row.keys()

                for row in reader:
                    self.training_set.append(row)

            self.dt.train(self.training_set, self.attributes)
            print(self.dt.root.child_nodes)

        elif button == 'Test Decision Tree':
            with open(test_file) as csvfile:
                reader = csv.DictReader(csvfile, column_names)

                first_row: dict = next(reader)
                self.attributes = first_row.keys()

                for row in reader:
                    self.test_set.append(row)

            self.dt.test(self.test_set)


if __name__ == '__main__':
    app = MainGui()
    app.start()
