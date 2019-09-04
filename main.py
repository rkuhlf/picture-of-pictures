redownload_pictures = False
turn_to_gray = False
reformat_images = False
generate_new_image = True

if (redownload_pictures):
    from google_images_download import google_images_download  # importing the library

    response = google_images_download.googleimagesdownload()  # class instantiation

    arguments = {"keywords": "President", "limit": 40, "print_urls": True}  # creating list of arguments
    paths = response.download(arguments)  # passing the arguments to the function
    print(paths)  # printing absolute paths of the downloaded images

import os, random

folderToLoop = "President"
directory = os.getcwd() + "/downloads/" + folderToLoop
from skimage.io import imread, imsave
from skimage.color import rgb2gray

if (turn_to_gray):

    for filename in os.listdir(directory):
        print(filename)
        fullname = os.path.join(directory, filename)
        try:
            img = imread(fullname)
            img_grayscale = rgb2gray(img)
            imsave(fullname, img_grayscale)
        except Exception as e:
            print(e)

if (reformat_images):
    from skimage.transform import rescale

    targetImageWidth = 100
    targetImageHeight = 50

    for filename in os.listdir(directory):
        print(filename)
        fullname = os.path.join(directory, filename)

        try:
            img = imread(fullname)

            if (targetImageHeight / targetImageWidth < img.shape[0] / img.shape[1]):
                # if too tall, scale by width
                img_rescaled = rescale(img, targetImageWidth / img.shape[1] * 2, anti_aliasing=False)

                # crop off the top
                center = img_rescaled.shape[0] / 2

                img_rescaled = img_rescaled[int(center - targetImageHeight):int(center + targetImageHeight)]
            else:
                # scale by height
                img_rescaled = rescale(img, targetImageWidth / img.shape[1] * 2, anti_aliasing=False)

                # crop off the sides
                center = img_rescaled.shape[1] / 2

                img_rescaled = img_rescaled[:, int(center - targetImageWidth):int(center + targetImageWidth)]


            imsave(fullname, img_rescaled)
        except:
            print("Couldn't Rescale")




if (generate_new_image):
    targetImage = random.choice(os.listdir(directory))
    print(targetImage)