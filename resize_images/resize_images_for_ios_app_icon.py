#!/usr/bin/env python3

from PIL import Image
import sys

ios_appicon_sizes = [20,29,40,58,60,76,80,87,120,152,167,180,1024]

def resize_image(image, size, file_name):
    resized_image = image.resize((size,size))
    output_name, output_format = file_name.split('.')
    resized_image.save('resized_images/'+output_name+str(size)+'x'+str(size)+'.'+output_format, image.format)

def resize_images(image_path, file_name):
    with open(image_path+'/'+file_name, 'r+b') as f:
        with Image.open(f) as image:
            for size in ios_appicon_sizes:
                resize_image(image, size, file_name)

if __name__ == '__main__':
    relative_path = sys.argv[1]
    image_path, file_name = relative_path.split('/')
    resize_images(image_path, file_name)
