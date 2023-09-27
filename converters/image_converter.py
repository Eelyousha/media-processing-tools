import numpy as np

from PIL import Image

from .basic_converter import BasicConverter


class ImageConverter(BasicConverter):
    gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    gscale2 = "@%#*+=-:. "

    def _get_average_l(self, image):
        """
        Given PIL Image, return average value of grayscale value
        """
        im = np.array(image)
        w, h = im.shape
        return np.average(im.reshape(w * h))

    def _process(self, fileName, cols, scale, more_levels):
        """
        Given Image and dims (rows, cols) returns an m*n list of Images
        """
        image = Image.open(fileName).convert("L")

        W, H = image.size[0], image.size[1]
        print("input image dims: %d x %d" % (W, H))

        w = W / cols
        h = w / scale
        rows = int(H / h)

        print("cols: %d, rows: %d" % (cols, rows))
        print("tile dims: %d x %d" % (w, h))

        if cols > W or rows > H:
            print("Image too small for specified cols!")
            return ""

        aimg = []
        for j in range(rows):
            y1 = int(j * h)
            y2 = int((j + 1) * h)

            if j == rows - 1:
                y2 = H

            aimg.append("")

            for i in range(cols):
                x1 = int(i * w)
                x2 = int((i + 1) * w)

                if i == cols - 1:
                    x2 = W

                img = image.crop((x1, y1, x2, y2))

                avg = int(self._get_average_l(img))

                if more_levels:
                    gsval = self.gscale1[int((avg * (len(self.gscale1)-1)) / 255)]
                else:
                    gsval = self.gscale2[int((avg * (len(self.gscale2)-1)) / 255)]

                aimg[j] += gsval

        return aimg

    def convert_data(
        self,
        filename: str,
        cols: int | None,
        scale: float | None,
        more_levels: bool | None,
    ):
        """Converts image to ASCII art, more_levels represents higher contrast result"""
        if cols is None:
            cols = 64
        if scale is None:
            scale = 0.43
        if more_levels is None:
            more_levels = False

        aimg = self._process(filename, cols, scale, more_levels)

        f = ""
        for row in aimg:
            f = f"{f}{row}\n"

        return f
