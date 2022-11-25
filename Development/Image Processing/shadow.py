import numpy as np
import cv2

or_img = cv2.imread("factura.jpg")

y_cb_cr_img = cv2.cvtColor(or_img,cv2.COLOR_BGR2YCrCb)

binary_mask = np.copy(y_cb_cr_img)

y_mean = np.mean(cv2.split(y_cb_cr_img)[0])

y_std = np.std(cv2.split(y_cb_cr_img)[0])


for i in range(y_cb_cr_img.shape[0]):
    for j in range(y_cb_cr_img.shape[1]):

        if y_cb_cr_img[i, j, 0] < y_mean - (y_std / 3):
           
            binary_mask[i, j] = [255, 255, 255]
        else:
            
            binary_mask[i, j] = [0, 0, 0]


kernel = np.ones((3, 3), np.uint8)
erosion = cv2.erode(binary_mask, kernel, iterations=1)

spi_la = 0

spi_s = 0

n_la = 0

n_s = 0

for i in range(y_cb_cr_img.shape[0]):
    for j in range(y_cb_cr_img.shape[1]):
        if erosion[i, j, 0] == 0 and erosion[i, j, 1] == 0 and erosion[i, j, 2] == 0:
            spi_la = spi_la + y_cb_cr_img[i, j, 0]
            n_la += 1
        else:
            spi_s = spi_s + y_cb_cr_img[i, j, 0]
            n_s += 1

# get the average pixel intensities in the lit areas
average_ld = spi_la / n_la

# get the average pixel intensities in the shadow
average_le = spi_s / n_s

# difference of the pixel intensities in the shadow and lit areas
i_diff = average_ld - average_le

# get the ratio between average shadow pixels and average lit pixels
ratio_as_al = average_ld / average_le

# added these difference
for i in range(y_cb_cr_img.shape[0]):
    for j in range(y_cb_cr_img.shape[1]):
        if erosion[i, j, 0] == 255 and erosion[i, j, 1] == 255 and erosion[i, j, 2] == 255:

            y_cb_cr_img[i, j] = [y_cb_cr_img[i, j, 0] + i_diff, y_cb_cr_img[i, j, 1] + ratio_as_al,
                                 y_cb_cr_img[i, j, 2] + ratio_as_al]

# covert the YCbCr image to the BGR image
final_image = cv2.cvtColor(y_cb_cr_img, cv2.COLOR_YCR_CB2BGR)

cv2.imshow("im1", or_img)
cv2.imshow("im2", final_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

