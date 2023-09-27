import argparse
import numpy as np

from PIL import Image

from .basic_converter import BasicConverter


class ImageConverter(BasicConverter):
    gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    gscale2 = "@%#*+=-:. "

    # def __init__(self):
    #     pass

    def _getAverageL(self, image):
        """
        Given PIL Image, return average value of grayscale value
        """
        # get image as numpy array
        im = np.array(image)

        # get shape
        w, h = im.shape

        # get average
        return np.average(im.reshape(w * h))

    def _process(self, fileName, cols, scale, moreLevels):
        """
        Given Image and dims (rows, cols) returns an m*n list of Images
        """
        # declare globals

        # open image and convert to grayscale
        image = Image.open(fileName).convert("L")

        # store dimensions
        W, H = image.size[0], image.size[1]
        print("input image dims: %d x %d" % (W, H))

        # compute width of tile
        w = W / cols

        # compute tile height based on aspect ratio and scale
        h = w / scale

        # compute number of rows
        rows = int(H / h)

        print("cols: %d, rows: %d" % (cols, rows))
        print("tile dims: %d x %d" % (w, h))

        # check if image size is too small
        if cols > W or rows > H:
            print("Image too small for specified cols!")
            return ""

        # ascii image is a list of character strings
        aimg = []
        # generate list of dimensions
        for j in range(rows):
            y1 = int(j * h)
            y2 = int((j + 1) * h)

            # correct last tile
            if j == rows - 1:
                y2 = H

            # append an empty string
            aimg.append("")

            for i in range(cols):
                # crop image to tile
                x1 = int(i * w)
                x2 = int((i + 1) * w)

                # correct last tile
                if i == cols - 1:
                    x2 = W

                # crop image to extract tile
                img = image.crop((x1, y1, x2, y2))

                # get average luminance
                avg = int(self._getAverageL(img))

                # look up ascii char
                if moreLevels:
                    gsval = self.gscale1[int((avg * 69) / 255)]
                else:
                    gsval = self.gscale2[int((avg * 9) / 255)]

                # append ascii char to string
                aimg[j] += gsval

        # return txt image
        return aimg

    def convert_data(self, filename):
        # set scale default as 0.43 which suits
        # a Courier font
        scale = 0.43

        # set cols
        cols = 64

        # print("generating ASCII art...")
        # convert image to ascii txt
        aimg = self._process(filename, cols, scale, True)

        f = ""
        for row in aimg:
            f = f'{f}{row}\n'

        return f
