import cv2

def configure_cam(width=640,height=480,fps=30,autofocus=0):
    cam_port = "/sys/devices/pci0000:00/0000:00:14.0/usb3/3-4"
    cam = cv2.VideoCapture(2)

    cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
    cam.set(cv2.CAP_PROP_FPS,fps)
    cam.set(cv2.CAP_PROP_AUTOFOCUS,autofocus)
    cam.set(cv2.CAP_PROP_FOCUS,0)
    print(f'({width},{height}),{fps}fps')

    return cam