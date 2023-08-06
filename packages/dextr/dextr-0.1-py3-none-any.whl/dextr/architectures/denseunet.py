# The MIT License (MIT)
#
# Copyright (c) 2020 University of East Anglia, Norwich, UK
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Developed by Geoffrey French in collaboration with Dr. M. Fisher and
# Dr. M. Mackiewicz.

# Used as reference:
# https://github.com/xmengli999/H-DenseUNet/blob/master/denseunet.py
# Uses torchvision densenet as the encoder

import torch.nn as nn, torch.nn.functional as F
from torchvision import models


class DecoderBlock(nn.Module):
    def __init__(self, x_chn_in, skip_chn_in, chn_out):
        super(DecoderBlock, self).__init__()

        if x_chn_in != skip_chn_in:
            raise ValueError('x_chn_in != skip_chn_in')

        self.x_chn_in = x_chn_in
        self.skip_chn_in = skip_chn_in
        self.chn_out = chn_out

        self.up = nn.Upsample(scale_factor=2)
        self.conv = nn.Conv2d(x_chn_in, chn_out, 3, padding=1, bias=False)
        self.conv_bn = nn.BatchNorm2d(chn_out)

    def forward(self, x_in, skip_in):
        if x_in.shape[1] != self.x_chn_in:
            raise ValueError('x_in.shape[1]={}, self.x_chn_in={}'.format(x_in.shape[1], self.x_chn_in))
        if skip_in.shape[1] != self.skip_chn_in:
            raise ValueError('skip_in.shape[1]={}, self.skip_chn_in={}'.format(skip_in.shape[1], self.skip_chn_in))
        x_up = self.up(x_in)
        x = x_up + skip_in
        x = F.relu(self.conv_bn(self.conv(x)))
        return x


class DenseUNet(nn.Module):
    BLOCK_SIZE = (32, 32)

    def __init__(self, base_model, num_classes):
        super(DenseUNet, self).__init__()

        # Module names for taps within encoder
        self.tap_names = []
        # Per tap number of channels
        enc_chn = []

        # Assign base model
        self.base_model = base_model

        # Tap after features.norm0 (next layer is pool0)
        enc_chn.append(base_model.features.norm0.num_features)
        self.tap_names.append('pool0')

        # Tap after features.denseblock1 (next layer is transition1)
        enc_chn.append(base_model.features.transition1.norm.num_features)
        self.tap_names.append('transition1')

        # Tap after features.denseblock2 (next layer is transition2)
        enc_chn.append(base_model.features.transition2.norm.num_features)
        self.tap_names.append('transition2')

        # Tap after features.denseblock3 (next layer is transition3)
        enc_chn.append(base_model.features.transition3.norm.num_features)
        self.tap_names.append('transition3')

        # Number of channels out of features model
        n_chn = base_model.features.norm5.num_features

        # A 1x1 conv layer mapping # features from denseblock3 to # of features from norm5
        self.line0_conv = nn.Conv2d(enc_chn[-1], n_chn, 1)
        enc_chn[-1] = n_chn

        # Decoder blocks
        self.decoder_blocks = nn.ModuleList()

        # We build the decoder in the reverse order in comparison to that of the encoder,
        # so reverse the order of `enc_chn`
        enc_chn = enc_chn[::-1]

        # Build the decoder blocks
        for e_chn_a, e_chn_b in zip(enc_chn, enc_chn[1:] + enc_chn[-1:]):
            decoder = DecoderBlock(n_chn, e_chn_a, e_chn_b)
            self.decoder_blocks.append(decoder)
            n_chn = e_chn_b

        # Reverse the order of the decoder block
        self.decoder_blocks = self.decoder_blocks[::-1]

        # Final part: upsample x2, a single 64 channel 3x3 conv layer, dropout, BN and finally pixel classification
        self.final_dec_up = nn.Upsample(scale_factor=2)
        self.final_dec_conv = nn.Conv2d(n_chn, 64, 3, padding=1, bias=False)
        self.final_dec_drop = nn.Dropout(0.3)
        self.final_dec_bn = nn.BatchNorm2d(64)

        # Final pixel classification layer
        self.final_clf = nn.Conv2d(64, num_classes, 1)

    def forward(self, x):
        # Apply layers from base_model.features, taking tensors at tap points
        enc_x = []
        for name, mod in self.base_model.features.named_children():
            if name in self.tap_names:
                enc_x.append(x)
            x = mod(x)
        # ReLu after encoder BN layer
        x = F.relu(x)

        # Apply line0_conv from last tap
        line0 = self.line0_conv(enc_x[-1])
        enc_x[-1] = line0

        # Apply decoder blocks in reverse order
        for dec_block, ex in zip(self.decoder_blocks[::-1], enc_x[::-1]):
            x = dec_block(x, ex)

        # Final layers
        x = self.final_dec_bn(self.final_dec_drop(self.final_dec_conv(self.final_dec_up(x))))
        x = F.relu(x)
        logits = self.final_clf(x)

        result = dict(out=logits)

        return result

    def pretrained_parameters(self):
        if self.pretrained:
            return list(self.base_model.features.parameters())
        else:
            return []

    def new_parameters(self):
        if self.pretrained:
            pretrained_ids = [id(p) for p in self.base_model.features.parameters()]
            return [p for p in self.parameters() if id(p) not in pretrained_ids]
        else:
            return list(self.parameters())


def dextr_denseunet161(num_classes=1):
    base_model = models.densenet161(pretrained=True)
    model = DenseUNet(base_model, num_classes)

    # Create new input `conv1` layer that takes a 4-channel input
    new_conv1 = nn.Conv2d(4, 96, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
    new_conv1.weight[:, :3, :, :] = model.base_model.features[0].weight
    model.base_model.features[0].weight.data = new_conv1.weight.data

    # Setup new and pre-trained parameters for fine-tuning
    pretrained_parameters = list(model.base_model.features.parameters())
    pretrained_ids = {id(p) for p in pretrained_parameters}
    new_parameters = [p for p in model.parameters() if id(p) not in pretrained_ids]

    model.pretrained_parameters = pretrained_parameters
    model.new_parameters = new_parameters

    return model



