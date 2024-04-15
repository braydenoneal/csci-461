import torch
import torch.nn as nn
from skimage import io
import du.lib as dulib
import math
import os

image_size = 100

train_amount = 0.8
learning_rate = 0.001
momentum = 0.9
epochs = 64
batch_size = 32
centered = True
normalized = True

yss_dictionary = {}
yss_list = []
xss_list = []

for subdir, dirs, files in os.walk('images'):
    for file in files:
        if file[-4:] == '.png':
            yss_dictionary[subdir] = 0
            yss_list.append(list(yss_dictionary.keys()).index(subdir))
            xss_list.append(io.imread(os.path.join(subdir, file), as_gray=True))

yss = torch.LongTensor(len(yss_list))
xss = torch.FloatTensor(len(xss_list), image_size, image_size)

for i in range(len(yss_list)):
    yss[i] = yss_list[i]

for i in range(len(xss_list)):
    xss[i] = torch.FloatTensor(xss_list[i])

random_split = torch.randperm(xss.size(0))
train_split_amount = math.floor(xss.size(0) * train_amount)

xss_train = xss[random_split][:train_split_amount]
xss_test = xss[random_split][train_split_amount:]

if centered:
    xss_train, xss_train_means = dulib.center(xss_train)
    xss_test, _ = dulib.center(xss_test, xss_train_means)

if normalized:
    xss_train, xss_train_stds = dulib.normalize(xss_train)
    xss_test, _ = dulib.normalize(xss_test, xss_train_stds)

yss_train = yss[random_split][:train_split_amount]
yss_test = yss[random_split][train_split_amount:]

image_dimensions = image_size * image_size


class ConvolutionalModel(nn.Module):
    def __init__(self):
        super(ConvolutionalModel, self).__init__()
        self.meta_layer1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=16, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        )
        self.meta_layer2 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        )
        self.fc_layer1 = nn.Linear(image_dimensions * 2, image_dimensions)
        self.fc_layer2 = nn.Linear(image_dimensions, len(yss_list))

    def forward(self, forward_xss):
        forward_xss = torch.unsqueeze(forward_xss, dim=1)
        forward_xss = self.meta_layer1(forward_xss)
        forward_xss = self.meta_layer2(forward_xss)
        forward_xss = torch.reshape(forward_xss, (-1, image_dimensions * 2))
        forward_xss = self.fc_layer1(forward_xss)
        forward_xss = self.fc_layer2(forward_xss)
        return torch.log_softmax(forward_xss, dim=1)


model = ConvolutionalModel()
criterion = nn.NLLLoss()


def pct_correct(xss_test_, yss_test_):
    count = 0

    for x, y in zip(xss_test_, yss_test_):
        if torch.argmax(x).item() == y.item():
            count += 1

    return 100 * count / len(xss_test_)


model = dulib.train(
    model,
    crit=criterion,
    train_data=(xss_train, yss_train),
    valid_data=(xss_test, yss_test),
    learn_params={'lr': learning_rate, 'mo': momentum},
    epochs=epochs,
    bs=batch_size,
    valid_metric=pct_correct,
    graph=1,
    print_lines=(-1,)
)

pct_training = dulib.class_accuracy(model, (xss_train, yss_train), show_cm=False)

pct_testing = dulib.class_accuracy(model, (xss_test, yss_test), show_cm=False)

print(
    f'\n'
    f'Percentage correct on training data: {100 * pct_training:.2f}\n'
    f'Percentage correct on testing data: {100 * pct_testing:.2f}\n'
    f'\n'
    f'Learning Rate: {learning_rate}\n'
    f'Momentum: {momentum}\n'
    f'Epochs: {epochs}\n'
    f'Batch Size: {batch_size}'
)

"""
Percentage correct on training data: 100.00
Percentage correct on testing data: 100.00

Learning Rate: 0.001
Momentum: 0.9
Epochs: 64
Batch Size: 32
"""
