# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import numpy as np
import rasterio as rio
import rasterio.features


class Postprocessor:
    def __init__(self,
                 resolution,
                 sieve_size):
        """Constructor method

        :param float resolution: resolution in meters per pixel
        :param int or None sieve_size: sieve size in pixels (minimum number of pixels to retain)
        :returns: None
        :rtype: None
        """
        self.resolution = resolution
        self.sieve_size = sieve_size

    def vectorize_mask(self,
                       mask,
                       coordinates):
        """Returns georeferenced features of the polygons in the mask given its coordinates of the top left corner.

        :param np.ndarray[np.uint8] mask: mask
        :param (float, float) coordinates: coordinates (x, y)
        :returns: features
        :rtype: dict
        """
        if self.sieve_size is not None:
            mask = rio.features.sieve(mask, size=self.sieve_size)

        transform = rio.transform.from_origin(west=coordinates[0],
                                              north=coordinates[1],
                                              xsize=self.resolution,
                                              ysize=self.resolution)
        vectorized_mask = rio.features.shapes(mask, transform=transform)

        features = [{'properties': {'class': int(value)}, 'geometry': shape}
                    for shape, value in vectorized_mask if int(value) != 0]
        return features
