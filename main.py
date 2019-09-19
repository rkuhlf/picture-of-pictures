import os
from google_images_download import google_images_download  # importing the library
from skimage.io import imread, imsave
from skimage.transform import rescale
from skimage.color import rgb2gray
from PIL import Image



redownload_pictures = False
turn_to_gray = True
reformat_images = True
generate_new_image = True
targetImageWidth = 40
targetImageHeight = 20
folder_path = "\\picture-of-pictures"
folderToLoop = "President"
directory = os.getcwd() + folder_path + "\\downloads\\" + folderToLoop



def ComparePictures(img1, img2):
    # print(img1)
    # print(img2)
    total_dif = 0
    for x in range(img1.shape[0]):
        for y in range(img1.shape[1]):
            try:
                # print(str(int(img1[x, y])) + " - " + str(int(img2[x, y])))
                total_dif += abs(int(img1[x, y]) - int(img2[x, y])) # if undefined return math.inf
            except:
                total_dif += 255

    return total_dif



if (redownload_pictures):
    response = google_images_download.googleimagesdownload()  # class instantiation

    if not (os.path.exists(os.getcwd() + folder_path + "\\downloads")):
        os.mkdir(os.getcwd() + folder_path + "\\downloads")
    arguments = {"keywords": "President", "output_directory": os.getcwd() + folder_path + "\\downloads", "limit": 160, "print_urls": True, "chromedriver": "C:\\Users\\Trevor and Riley\\Downloads\\chromedriver_win32\\chromedriver.exe"}  # creating list of arguments
    paths = response.download(arguments)  # passing the arguments to the function
    print(paths)  # printing absolute paths of the downloaded images



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
    targetname = os.getcwd() + folder_path + "\\target_image.jpg"
    targetImage = imread(targetname)
    targetImage = rgb2gray(targetImage)


    centerX = targetImage.shape[1] / 2
    centerY = targetImage.shape[0] / 2
    newWidth = targetImage.shape[1] - (targetImage.shape[1] % (targetImageWidth * 2))
    newHeight = targetImage.shape[0] - (targetImage.shape[0] % (targetImageHeight * 2))
    targetImage = targetImage[int(centerY - newHeight * 2):int(centerY + newHeight * 2), int(centerX - newWidth * 2):int(centerX + newWidth * 2)]
    imsave(targetname[:-4] + "using.jpg", targetImage)



    final_image = Image.new('RGB', (newWidth, newHeight))
    for x in range(0, int(targetImage.shape[1] / (targetImageWidth)) + 1):
        for y in range(0, int(targetImage.shape[0] / (targetImageHeight)) + 1):
            recordDifference = None
            recordFile = None
            for filename in os.listdir(directory):
                try:
                    f = imread(os.path.join(directory, filename))
                except:
                    continue
                    print("Skipped bad file: " + filename)


                n = ComparePictures(targetImage[y * targetImageHeight * 2:(y + 1) * targetImageHeight * 2, x * targetImageWidth * 2:(x + 1) * targetImageWidth * 2] * 255, f) # multiply target image height by 2?
                # print(str(n) + " : " + filename)

                if recordDifference == None:
                    recordDifference = n
                    recordFile = directory + "/" + filename

                # print(recordDifference)
                if n < recordDifference:
                    recordDifference = n
                    recordFile = directory + "/" + filename

            print("----" + recordFile + "----")
            # append the picture
            paste_x = x * targetImageWidth * 2
            paste_y = y * targetImageHeight * 2
            print(paste_x, paste_y)
            final_image.paste(Image.open(recordFile), (paste_x, paste_y)) # pasted x, y from top left # newHeight - paste_y - targetImageHeight
            # final_image.save(os.getcwd() + '/final_image' + str(x) + "," + str(y) + '.jpg')

    final_image.save(os.getcwd() + '/final_image.jpg')

