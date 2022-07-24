# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import src.utils as utils


def get_coordinates(bounding_box, image_size):
    """Returns the coordinates of the top left corner of each tile in the area of the bounding box.

    :param (int, int, int, int) bounding_box: bounding box (x_1, y_1, x_2, y_2)
    :param int image_size: image size in pixels
    :returns: coordinates (x, y) of each tile
    :rtype: list[(float, float)]
    """
    image_size_meters = image_size * utils.RESOLUTION
    coordinates = []

    columns = int((bounding_box[2] - bounding_box[0]) // image_size_meters)
    if (bounding_box[2] - bounding_box[0]) % image_size_meters:
        columns += 1

    rows = int((bounding_box[3] - bounding_box[1]) // image_size_meters)
    if (bounding_box[3] - bounding_box[1]) % image_size_meters:
        rows += 1

    for row in range(rows):
        for column in range(columns):
            coordinates.append((bounding_box[0] + column * image_size_meters,
                                bounding_box[1] + (row + 1) * image_size_meters))
    return coordinates
