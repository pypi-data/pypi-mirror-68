import numpy as np
from torch.autograd import Variable
from pytorch2keras.converter import pytorch_to_keras

"""
    MENet, implemented in PyTorch.
    Original paper: 'Merging and Evolution: Improving Convolutional Neural Networks for Mobile Applications'
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as init


def depthwise_conv3x3(channels,
                      stride):
    return nn.Conv2d(
        in_channels=channels,
        out_channels=channels,
        kernel_size=3,
        stride=stride,
        padding=1,
        groups=channels,
        bias=False)


def group_conv1x1(in_channels,
                  out_channels,
                  groups):
    return nn.Conv2d(
        in_channels=in_channels,
        out_channels=out_channels,
        kernel_size=1,
        groups=groups,
        bias=False)


def channel_shuffle(x,
                    groups):
    """Channel Shuffle operation from ShuffleNet [arxiv: 1707.01083]
    Arguments:
        x (Tensor): tensor to shuffle.
        groups (int): groups to be split
    """
    batch, channels, height, width = x.size()
    channels_per_group = channels // groups
    x = x.view(batch, groups, channels_per_group, height, width)
    x = torch.transpose(x, 1, 2).contiguous()
    x = x.view(batch, channels, height, width)
    return x


class ChannelShuffle(nn.Module):

    def __init__(self,
                 channels,
                 groups):
        super(ChannelShuffle, self).__init__()
        if channels % groups != 0:
            raise ValueError('channels must be divisible by groups')
        self.groups = groups

    def forward(self, x):
        return channel_shuffle(x, self.groups)


class ShuffleInitBlock(nn.Module):

    def __init__(self,
                 in_channels,
                 out_channels):
        super(ShuffleInitBlock, self).__init__()

        self.conv = nn.Conv2d(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=3,
            stride=2,
            padding=1,
            bias=False)
        self.bn = nn.BatchNorm2d(num_features=out_channels)
        self.activ = nn.ReLU(inplace=True)
        self.pool = nn.MaxPool2d(
            kernel_size=3,
            stride=2,
            padding=1)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.activ(x)
        x = self.pool(x)
        return x


def conv1x1(in_channels,
            out_channels):
    return nn.Conv2d(
        in_channels=in_channels,
        out_channels=out_channels,
        kernel_size=1,
        bias=False)


def conv3x3(in_channels,
            out_channels,
            stride):
    return nn.Conv2d(
        in_channels=in_channels,
        out_channels=out_channels,
        kernel_size=3,
        stride=stride,
        padding=1,
        bias=False)


class MEModule(nn.Module):

    def __init__(self,
                 in_channels,
                 out_channels,
                 side_channels,
                 groups,
                 downsample,
                 ignore_group):
        super(MEModule, self).__init__()
        self.downsample = downsample
        mid_channels = out_channels // 4

        if downsample:
            out_channels -= in_channels

        # residual branch
        self.compress_conv1 = group_conv1x1(
            in_channels=in_channels,
            out_channels=mid_channels,
            groups=(1 if ignore_group else groups))
        self.compress_bn1 = nn.BatchNorm2d(num_features=mid_channels)
        self.c_shuffle = ChannelShuffle(
            channels=mid_channels,
            groups=(1 if ignore_group else groups))
        self.dw_conv2 = depthwise_conv3x3(
            channels=mid_channels,
            stride=(2 if self.downsample else 1))
        self.dw_bn2 = nn.BatchNorm2d(num_features=mid_channels)
        self.expand_conv3 = group_conv1x1(
            in_channels=mid_channels,
            out_channels=out_channels,
            groups=groups)
        self.expand_bn3 = nn.BatchNorm2d(num_features=out_channels)
        if downsample:
            self.avgpool = nn.AvgPool2d(kernel_size=3, stride=2, padding=1)
        self.activ = nn.ReLU(inplace=True)

        # fusion branch
        self.s_merge_conv = conv1x1(
            in_channels=mid_channels,
            out_channels=side_channels)
        self.s_merge_bn = nn.BatchNorm2d(num_features=side_channels)
        self.s_conv = conv3x3(
            in_channels=side_channels,
            out_channels=side_channels,
            stride=(2 if self.downsample else 1))
        self.s_conv_bn = nn.BatchNorm2d(num_features=side_channels)
        self.s_evolve_conv = conv1x1(
            in_channels=side_channels,
            out_channels=mid_channels)
        self.s_evolve_bn = nn.BatchNorm2d(num_features=mid_channels)

    def forward(self, x):
        identity = x
        # pointwise group convolution 1
        x = self.activ(self.compress_bn1(self.compress_conv1(x)))
        x = self.c_shuffle(x)
        # merging
        y = self.s_merge_conv(x)
        y = self.s_merge_bn(y)
        y = self.activ(y)
        # depthwise convolution (bottleneck)
        x = self.dw_bn2(self.dw_conv2(x))
        # evolution
        y = self.s_conv(y)
        y = self.s_conv_bn(y)
        y = self.activ(y)
        y = self.s_evolve_conv(y)
        y = self.s_evolve_bn(y)
        y = F.sigmoid(y)
        x = x * y
        # pointwise group convolution 2
        x = self.expand_bn3(self.expand_conv3(x))
        # identity branch
        if self.downsample:
            identity = self.avgpool(identity)
            x = torch.cat((x, identity), dim=1)
        else:
            x = x + identity
        x = self.activ(x)
        return x


class MENet(nn.Module):

    def __init__(self,
                 block_channels,
                 side_channels,
                 groups,
                 num_classes=1000):
        super(MENet, self).__init__()
        input_channels = 3
        block_layers = [4, 8, 4]

        self.features = nn.Sequential()
        self.features.add_module("init_block", ShuffleInitBlock(
            in_channels=input_channels,
            out_channels=block_channels[0]))

        for i in range(len(block_channels) - 1):
            stage = nn.Sequential()
            in_channels_i = block_channels[i]
            out_channels_i = block_channels[i + 1]
            for j in range(block_layers[i]):
                stage.add_module("unit_{}".format(j + 1), MEModule(
                    in_channels=(in_channels_i if j == 0 else out_channels_i),
                    out_channels=out_channels_i,
                    side_channels=side_channels,
                    groups=groups,
                    downsample=(j == 0),
                    ignore_group=(i == 0 and j == 0)))
            self.features.add_module("stage_{}".format(i + 1), stage)

        self.features.add_module('final_pool', nn.AvgPool2d(kernel_size=7))

        self.output = nn.Linear(
            in_features=block_channels[-1],
            out_features=num_classes)

        self._init_params()

    def _init_params(self):
        for name, module in self.named_modules():
            if isinstance(module, nn.Conv2d):
                init.kaiming_uniform_(module.weight)
                if module.bias is not None:
                    init.constant_(module.bias, 0)

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.output(x)
        return x


def get_menet(first_block_channels,
              side_channels,
              groups,
              pretrained=False,
              **kwargs):
    if first_block_channels == 108:
        block_channels = [12, 108, 216, 432]
    elif first_block_channels == 128:
        block_channels = [12, 128, 256, 512]
    elif first_block_channels == 160:
        block_channels = [16, 160, 320, 640]
    elif first_block_channels == 228:
        block_channels = [24, 228, 456, 912]
    elif first_block_channels == 256:
        block_channels = [24, 256, 512, 1024]
    elif first_block_channels == 348:
        block_channels = [24, 348, 696, 1392]
    elif first_block_channels == 352:
        block_channels = [24, 352, 704, 1408]
    elif first_block_channels == 456:
        block_channels = [48, 456, 912, 1824]
    else:
        raise ValueError("The {} of `first_block_channels` is not supported".format(first_block_channels))

    if pretrained:
        raise ValueError("Pretrained model is not supported")

    net = MENet(
        block_channels=block_channels,
        side_channels=side_channels,
        groups=groups,
        **kwargs)
    return net


def menet108_8x1_g3(**kwargs):
    return get_menet(108, 8, 3, **kwargs)


def menet128_8x1_g4(**kwargs):
    return get_menet(128, 8, 4, **kwargs)


def menet160_8x1_g8(**kwargs):
    return get_menet(160, 8, 8, **kwargs)


def menet228_12x1_g3(**kwargs):
    return get_menet(228, 12, 3, **kwargs)


def menet256_12x1_g4(**kwargs):
    return get_menet(256, 12, 4, **kwargs)


def menet348_12x1_g3(**kwargs):
    return get_menet(348, 12, 3, **kwargs)


def menet352_12x1_g8(**kwargs):
    return get_menet(352, 12, 8, **kwargs)


def menet456_24x1_g3(**kwargs):
    return get_menet(456, 24, 3, **kwargs)


if __name__ == '__main__':
    max_error = 0
    for i in range(10):
        model = menet228_12x1_g3()
        for m in model.modules():
            m.training = False

        input_np = np.random.uniform(0, 1, (1, 3, 224, 224))
        input_var = Variable(torch.FloatTensor(input_np))
        output = model(input_var)

        k_model = pytorch_to_keras(model, input_var, (3, 224, 224,), verbose=True)

        pytorch_output = output.data.numpy()
        keras_output = k_model.predict(input_np)

        error = np.max(pytorch_output - keras_output)
        print(error)
        if max_error < error:
            max_error = error

    print('Max error: {0}'.format(max_error))
