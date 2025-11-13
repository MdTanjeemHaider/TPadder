"""Utility functions for TPadder"""
from PIL import Image, ImageFilter


# Constants
BLOCK_SIZE = 16
PADDING = 2


def convert(source_img):
    """Convert a source image into a tiled texture with padding between blocks."""
    width, height = source_img.size
    blocks_per_row = width // BLOCK_SIZE
    blocks_per_column = height // BLOCK_SIZE

    new_width = width + (blocks_per_row - 1) * PADDING
    new_height = height + (blocks_per_column - 1) * PADDING
    result_img = Image.new("RGBA", (new_width, new_height))

    for row in range(blocks_per_row):
        for col in range(blocks_per_column):
            x = row * BLOCK_SIZE
            y = col * BLOCK_SIZE
            new_x = row * (BLOCK_SIZE + PADDING)
            new_y = col * (BLOCK_SIZE + PADDING)

            block = source_img.crop((x, y, x + BLOCK_SIZE, y + BLOCK_SIZE))
            result_img.paste(block, (new_x, new_y))

    return result_img


def convert_highlighted(source_img, color=(255, 255, 255, 255)):
    """Convert a source image into a tiled texture with padding between blocks and a highlighted outline."""
    outline = source_img.filter(ImageFilter.FIND_EDGES)
    pixels = outline.load()

    for x in range(outline.width):
        for y in range(outline.height):
            if pixels[x, y][3] == 255:
                pixels[x, y] = color

    return convert(outline)
