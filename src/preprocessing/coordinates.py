# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import src.utils as utils


def get_coordinates(bounding_box):
    """Returns the coordinates of the top left corner of each tile in the area of the bounding box.
    The bounding box is quantized to the image size in meters.

    :param (int, int, int, int) bounding_box: bounding box (x_1, y_1, x_2, y_2)
    :returns: coordinates (x, y) of each tile
    :rtype: list[(int, int)]
    """
    coordinates = []

    bounding_box = (bounding_box[0] - (bounding_box[0] % utils.IMAGE_SIZE_METERS),
                    bounding_box[1] - (bounding_box[1] % utils.IMAGE_SIZE_METERS),
                    bounding_box[2],
                    bounding_box[3])

    columns = (bounding_box[2] - bounding_box[0]) // utils.IMAGE_SIZE_METERS
    if (bounding_box[2] - bounding_box[0]) % utils.IMAGE_SIZE_METERS:
        columns += 1

    rows = (bounding_box[3] - bounding_box[1]) // utils.IMAGE_SIZE_METERS
    if (bounding_box[3] - bounding_box[1]) % utils.IMAGE_SIZE_METERS:
        rows += 1

    for row in range(rows):
        for column in range(columns):
            coordinates.append((bounding_box[0] + column * utils.IMAGE_SIZE_METERS,
                                bounding_box[1] + (row + 1) * utils.IMAGE_SIZE_METERS))
    return coordinates
