import cv2
import numpy as np


def detect_potholes(image_path):
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print("无法读取图像!")
        return

    # 1. graying
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. Denoising - using Gaussian filtering
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. 直方图均衡化Histogram equalization
    equalized = cv2.equalizeHist(denoised)

    # 4. Edge Detection - Use Canny edge detection
    edges = cv2.Canny(equalized, 100, 200)


        # 寻找轮廓Contour finding
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Analyze the hole size and plot the results on the image
    for contour in contours:
            # 尝试使用轮廓近似
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # 计算轮廓面积
            area = cv2.contourArea(approx)
            if area > 100:  # 面积阈值
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, f"Area: {int(area)}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # 显示图像



    cv2.imshow('Detected Potholes', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = r"C:\\Users\Dell\Desktop\test3.JPG"  # 替换为你的图像路径
    detect_potholes(image_path)
