import torch
import torch.nn as nn

class UNetPixelwiseRegression(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(UNetPixelwiseRegression, self).__init__()

        # Contracting path
        self.conv1 = self.conv_block(in_channels, 64)
        self.conv2 = self.conv_block(64, 128)
        self.conv3 = self.conv_block(128, 256)
        self.conv4 = self.conv_block(256, 512)

        # Bottleneck
        self.bottleneck = self.conv_block(512, 1024)

        # Expanding path
        self.upconv4 = self.upconv_block(1024, 512)
        self.upconv3 = self.upconv_block(512, 256)
        self.upconv2 = self.upconv_block(256, 128)
        self.upconv1 = self.upconv_block(128, 64)

        # Output layer with linear activation for regression
        self.out_conv = nn.Conv2d(64, out_channels, kernel_size=1)

    def conv_block(self, in_channels, out_channels):
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

    def upconv_block(self, in_channels, out_channels):
        return nn.Sequential(
            nn.ConvTranspose2d(in_channels, out_channels, kernel_size=2, stride=2),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        # Contracting path
        conv1_out = self.conv1(x)
        conv2_out = self.conv2(conv1_out)
        conv3_out = self.conv3(conv2_out)
        conv4_out = self.conv4(conv3_out)

        # Bottleneck
        bottleneck_out = self.bottleneck(conv4_out)

        # Expanding path
        upconv4_out = self.upconv4(bottleneck_out)
        concat4_out = torch.cat([upconv4_out, conv4_out], dim=1)
        
        upconv3_out = self.upconv3(concat4_out)
        concat3_out = torch.cat([upconv3_out, conv3_out], dim=1)

        upconv2_out = self.upconv2(concat3_out)
        concat2_out = torch.cat([upconv2_out, conv2_out], dim=1)

        upconv1_out = self.upconv1(concat2_out)
        concat1_out = torch.cat([upconv1_out, conv1_out], dim=1)

        # Output layer with linear activation
        final_out = self.out_conv(concat1_out)

        return final_out