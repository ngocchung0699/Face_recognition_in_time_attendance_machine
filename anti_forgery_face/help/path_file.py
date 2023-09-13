import os
from imutils import paths

def path_image(link_dir):
    imagePaths = list(paths.list_images(link_dir))
    list_link_image = []
    for (i, imagePath) in enumerate(imagePaths):
        link_cup = imagePath.split(os.path.sep)
        link_cup.insert(0, i+1)
        list_link_image.append(link_cup)
    return list_link_image

