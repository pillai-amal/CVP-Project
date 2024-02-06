import torch
import torch.nn as nn

class UNetPixelwiseRegression(nn.Module):
    def __init__(self, in_channels=1, out_channels=1):
        super(UNetPixelwiseRegression, self).__init__()

        # Contracting path
        self.encoder1 = self.conv_block(in_channels, 64)
        self.encoder2 = self.conv_block(64, 128)
        self.encoder3 = self.conv_block(128, 256)
        self.encoder4 = self.conv_block(256, 512)

        # Bottleneck
        self.bottleneck = self.conv_block(512, 1024)

        # Expanding path
        self.decoder4 = self.upconv_block(1024, 512)
        self.decoder3 = self.upconv_block(1024, 256)
        self.decoder2 = self.upconv_block(512, 128)
        self.decoder1 = self.upconv_block(256, 64)

        # Output layer with linear activation for regression
        self.out_conv = nn.Conv2d(128, out_channels, kernel_size=3, padding=1)

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
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        # Contracting path
        enc1 = self.encoder1(x)
        enc2 = self.encoder2(enc1)
        enc3 = self.encoder3(enc2)
        enc4 = self.encoder4(enc3)

        # Bottleneck
        bottleneck = self.bottleneck(enc4)

        # Expanding path
        dec4 = self.decoder4(bottleneck)
        concat4 = torch.cat([dec4, enc4], dim=1)

        dec3 = self.decoder3(concat4)
        concat3 = torch.cat([dec3, enc3], dim=1)

        dec2 = self.decoder2(concat3)
        concat2 = torch.cat([dec2, enc2], dim=1)

        dec1 = self.decoder1(concat2)
        concat1 = torch.cat([dec1, enc1], dim=1)

        # Output layer with linear activation
        final_out = self.out_conv(concat1)
        return final_out
