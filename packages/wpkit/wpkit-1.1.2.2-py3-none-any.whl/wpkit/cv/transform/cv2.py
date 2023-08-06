import cv2
import numpy as np
import random,math
# 几何变换 geometrical

# 缩放
def resize(img,size):
    return cv2.resize(img,size)
def rescale(img,scale):
    h,w=img.shape[:2]
    h,w=int(h*scale),int(w*scale)
    return cv2.resize(img,(h,w))
# crop
def randomCrop(img,size):
    h,w=img.shape[:2]
    nw,nh=size
    spaceX=w-nw
    spaceY=h-nh
    ofx=random.randint(0,spaceX+1)
    ofy=random.randint(0,spaceY+1)
    img=img[ofy:ofy+spaceY,ofx:ofx+spaceX]
    return img
# flip
def herizontal_flip(img):
    return cv2.flip(img,1)
def vertical_flip(img):
    return cv2.flip(img,0)
# shift
def shift(image,offset):
    x,y=offset
    M = np.float32([[1, 0, x], [0, 1, y]])  # 4  //X轴移动x, Y中移动y
    shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))  # 5
    return shifted
# rotate
def rotate(image, angle):
    # 获取图像的尺寸
    # 旋转中心
    (h, w) = image.shape[:2]
    (cx, cy) = (w / 2, h / 2)
    # 设置旋转矩阵
    M = cv2.getRotationMatrix2D((cx, cy), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    # 计算图像旋转后的新边界
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    # 调整旋转矩阵的移动距离（t_{x}, t_{y}）
    M[0, 2] += (nW / 2) - cx
    M[1, 2] += (nH / 2) - cy
    return cv2.warpAffine(image, M, (nW, nH))

# affine
def affine(img,pnts1,pnts2,size=None):
    pnts1=np.array(pnts1)
    pnts2=np.array(pnts2)
    M=cv2.getAffineTransform(pnts1,pnts2)
    img=cv2.warpAffine(img,M,size)
    return img
def randomAffine(img):
    pass
# perspective
def perspective(img,pnts1,pnts2,size=None):
    pnts1=np.array(pnts1)
    pnts2=np.array(pnts2)
    M=cv2.getPerspectiveTransform(pnts1,pnts2)
    img=cv2.warpPerspective(img,M,size)
    return img
def randomPerspective(img):
    pass
# 环形图像展开成为长条形
def get_huan_by_circle(img, circle_center, radius, radius_width):
    black_img = np.zeros((radius_width, int(2 * radius * math.pi), 3), dtype='uint8')
    for row in range(0, black_img.shape[0]):
        for col in range(0, black_img.shape[1]):
            theta = math.pi * 2 / black_img.shape[1] * (col + 1)
            rho = radius - row - 1
            p_x = int(circle_center[0] + rho * math.cos(theta) + 0.5)
            p_y = int(circle_center[1] - rho * math.sin(theta) + 0.5)
            black_img[row, col, :] = img[p_y, p_x, :]
    return black_img
# distort


# 光学变换 optical
# PCA jitter
def PCA_Jittering(img):
    img = np.asanyarray(img, dtype='float32')
    img = img / 255.0
    img_size = img.size // 3
    img1 = img.reshape(img_size, 3)
    img1 = np.transpose(img1)
    img_cov = np.cov([img1[0], img1[1], img1[2]])
    lamda, p = np.linalg.eig(img_cov)
    p = np.transpose(p)
    alpha1 = random.gauss(0, 1)
    alpha2 = random.gauss(0, 1)
    alpha3 = random.gauss(0, 1)
    v = np.transpose((alpha1 * lamda[0], alpha2 * lamda[1], alpha3 * lamda[2]))
    add_num = np.dot(p, v)
    img2 = np.array([img[:, :, 0] + add_num[0], img[:, :, 1] + add_num[1], img[:, :, 2] + add_num[2]])
    img2 = np.swapaxes(img2, 0, 2)
    img2 = np.swapaxes(img2, 0, 1)
    return img2
# light
def equalizeHist(img):
    imgYUV = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    # cv2.imshow("src", img)
    channelsYUV = cv2.split(imgYUV)
    channelsYUV[0] = cv2.equalizeHist(channelsYUV[0])
    channels = cv2.merge(channelsYUV)
    result = cv2.cvtColor(channels, cv2.COLOR_YCrCb2BGR)
    return result

# blur
def motion_blur(image, degree=12, angle=45):
    image = np.array(image)
    # 这里生成任意角度的运动模糊kernel的矩阵， degree越大，模糊程度越高
    M = cv2.getRotationMatrix2D((degree / 2, degree / 2), angle, 1)
    motion_blur_kernel = np.diag(np.ones(degree))
    motion_blur_kernel = cv2.warpAffine(motion_blur_kernel, M, (degree, degree))

    motion_blur_kernel = motion_blur_kernel / degree
    blurred = cv2.filter2D(image, -1, motion_blur_kernel)
    # convert to uint8
    cv2.normalize(blurred, blurred, 0, 255, cv2.NORM_MINMAX)
    blurred = np.array(blurred, dtype=np.uint8)
    return blurred

def guassion_blur(img,kernel_size=(3,3),sigmaX=0,sigmaY=0):
    img=cv2.GaussianBlur(img,kernel_size=kernel_size,sigmaX=sigmaX,sigmaY=sigmaY)
    return img

# noise
def sp_noise(image,prob):
  '''
  添加椒盐噪声
  prob:噪声比例
  '''
  output = np.zeros(image.shape,np.uint8)
  thres = 1 - prob
  for i in range(image.shape[0]):
    for j in range(image.shape[1]):
      rdn = random.random()
      if rdn < prob:
        output[i][j] = 0
      elif rdn > thres:
        output[i][j] = 255
      else:
        output[i][j] = image[i][j]
  return output
def gaussion_noise(image, mean=0, var=0.001):
  '''
    添加高斯噪声
    mean : 均值
    var : 方差
  '''
  image = np.array(image/255, dtype=float)
  noise = np.random.normal(mean, var ** 0.5, image.shape)
  out = image + noise
  if out.min() < 0:
    low_clip = -1.
  else:
    low_clip = 0.
  out = np.clip(out, low_clip, 1.0)
  out = np.uint8(out*255)
  #cv.imshow("gasuss", out)
  return out
# random color

# randome **


