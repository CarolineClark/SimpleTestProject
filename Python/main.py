from PIL import Image
from PIL import ImageColor
import os
import numpy as np
import sys

IMAGE_DIR = "images"
RIGHT_IMAGE_FILE = os.path.join(IMAGE_DIR, "zombies/zombie-right-lit.png")
UP_IMAGE_FILE = os.path.join(IMAGE_DIR, "zombies/zombie-up-lit.png")
DOWN_IMAGE_FILE = os.path.join(IMAGE_DIR, "zombies/zombie-under-lit.png")
LEFT_IMAGE_FILE = os.path.join(IMAGE_DIR, "zombies/zombie-left-lit.png")
NORMAL_MAP_FILE_NAME = os.path.join(IMAGE_DIR, "normal-map.png")


def main():
    check_file_exists(RIGHT_IMAGE_FILE)
    check_file_exists(UP_IMAGE_FILE)

    red_data = get_red_data()
    green_data = get_green_data()
    blue_data = get_blue_data()

    blue_green_data = np.add(blue_data, green_data)
    all_data = np.add(blue_green_data, red_data)

    show_image(all_data)
    write_normal_map_to_file(all_data, NORMAL_MAP_FILE_NAME)
    print "Success!"

def get_red_data():
    data_left = left_lit_image(LEFT_IMAGE_FILE)
    data_right = right_lit_image(RIGHT_IMAGE_FILE)
    red_data = average_data(data_left, data_right)
    # show_image(red_data)
    return red_data

def get_green_data():
    data_up = up_lit_image(UP_IMAGE_FILE)
    data_down = down_lit_image(DOWN_IMAGE_FILE)
    green_data = average_data(data_up, data_down)
    # show_image(green_data)
    return green_data

def get_blue_data():
    data_left = get_blue_lit_image(LEFT_IMAGE_FILE)
    data_right = get_blue_lit_image(RIGHT_IMAGE_FILE)
    data_up = get_blue_lit_image(UP_IMAGE_FILE)
    data_down = get_blue_lit_image(DOWN_IMAGE_FILE)
    blue_data = average_blue_data(data_up, data_down, data_left, data_right)
    return blue_data

def check_file_exists(path):
    if not os.path.exists(path):
        print "Your file {} doesn't exist. Exiting.".format(path)
        sys.exit(1)


def write_normal_map_to_file(data, filename):
    im = Image.fromarray(data)
    im.save(filename)


def show_image(data):
    im = Image.fromarray(data)
    im.show()    


def get_blue_lit_image(filename):
    data = parse_image_to_data(filename)
    remove_red(data)
    remove_green(data)
    return data


def up_lit_image(filename):
    data = parse_image_to_data(filename)
    remove_red(data)
    remove_blue(data)
    return data


def down_lit_image(filename):
    data = parse_image_to_data(filename)
    data[:,:,1] = 255 - data[:,:,1]
    remove_red(data)
    remove_blue(data)
    return data


def left_lit_image(filename):
    data = parse_image_to_data(filename)
    data[:,:,0] = 255 - data[:,:,0]
    remove_green(data)
    remove_blue(data)
    return data


def right_lit_image(filename):
    data = parse_image_to_data(filename)
    remove_green(data)
    remove_blue(data)
    return data


def average_data(*data_list):
    length = len(data_list)
    data_list = [(x[:,:,:]) / length for (x) in data_list]
    return sum(data_list)


def average_blue_data(*data_list):
    length = len(data_list)
    data_list = np.array([(x[:,:,:]) / length for (x) in data_list])
    data = data_list.sum(0)
    data[:,:,2] = data[:,:,2]/2 + 127
    return data.astype('uint8')


def remove_red(data):
    data[:,:,0] = 0


def remove_green(data):
    data[:,:,1] = 0


def remove_blue(data):
    data[:,:,2] = 0


def parse_image_to_data(filename):
    im = Image.open(filename)
    im = im.convert('RGBA')
    return np.array(im)


if __name__ == "__main__":
    main()