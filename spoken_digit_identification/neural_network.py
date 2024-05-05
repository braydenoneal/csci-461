import torch
import torch.nn as nn
from skimage import io
import du.lib as dulib
import math
import os

image_size = 100

train_amount = 0.75
learning_rate = 1e-3
momentum = 0.9
epochs = 64
batch_size = 64
centered = False
normalized = False

yss_dictionary = {}
yss_list = []
xss_list = []

print('Reading images')

for subdir, dirs, files in os.walk('images'):
    count = 0
    for file in files:
        if file[-4:] == '.png':
            if count > 128:
                break
            count += 1
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

        self.network = nn.Sequential(
            # 1 @ 100x100
            nn.Conv2d(in_channels=1, out_channels=20, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            # 16 @ 100x100
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0),
            # 16 @ 50x50
            nn.Conv2d(in_channels=20, out_channels=50, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            # 32 @ 50x50
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0),
            # 32 @ 25x25
            nn.Flatten(),
            nn.Linear(50 * (image_size // 2 // 2) ** 2, image_dimensions),
            nn.Linear(image_dimensions, len(yss_dictionary.keys())),
            nn.LogSoftmax(dim=1),
        )

    def forward(self, forward_xss):
        return self.network(torch.unsqueeze(forward_xss, dim=1))


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
    graph=0,
    print_lines=(-1,),
    gpu=(-1,)
)

# model, valids = dulib.cv_train(
#     model,
#     crit=criterion,
#     train_data=(xss_train, yss_train),
#     learn_params={'lr': learning_rate, 'mo': momentum},
#     epochs=epochs,
#     bs=batch_size,
#     verb=10,
#     k=10,
#     bail_after=30,
# )

pct_training = dulib.class_accuracy(model, (xss_train, yss_train), show_cm=False)

pct_testing = dulib.class_accuracy(model, (xss_test, yss_test), show_cm=True)

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

with torch.no_grad():
    model.eval()

    xss_list = [io.imread('record.png', as_gray=True)]
    # xss_list = [torch.FloatTensor((image_size, image_size))]
    xss = torch.FloatTensor(1, image_size, image_size).cuda()

    output = model(xss)

    print(output)
    print(output.argmax(axis=1).cpu().numpy())
