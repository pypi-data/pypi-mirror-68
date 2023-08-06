import numpy as np
import torch
from torch import nn

from torch.nn import functional as F
from torch.autograd import Variable
from onnx2keras import onnx_to_keras, check_torch_keras_error
import onnx


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, 5, 1)
        self.conv2 = nn.Conv2d(20, 50, 5, 1)
        self.fc1 = nn.Linear(4*4*50, 500)
        self.fc2 = nn.Linear(500, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4*4*50)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.softmax(x, dim=1)



if __name__ == '__main__':
    model = Net()

    input_np = np.random.uniform(0, 1, (1, 1, 28, 28))
    input_var = Variable(torch.FloatTensor(input_np), requires_grad=False)
    output = model(input_var)

    torch.onnx.export(model, (input_var), "_tmpnet.onnx",
                      verbose=True,
                      input_names=['test_in1'],
                      output_names=['test_out']
    )

    onnx_model = onnx.load('_tmpnet.onnx')
    k_model = onnx_to_keras(onnx_model, ['test_in1'])

    error = check_torch_keras_error(model, k_model, input_np)

    print('Max error: {0}'.format(error))

