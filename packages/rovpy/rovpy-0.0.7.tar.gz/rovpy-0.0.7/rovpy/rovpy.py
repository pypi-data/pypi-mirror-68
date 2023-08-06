from pymavlink import mavutil
import numpy as np
import cv2
import imutils
import serial

x = 0
y = 0
r = 0
print("Rovpy library starting...")
def colors(color):
    colors = {
    "red": {"upper": "255, 255, 255",
            "lower":"171, 160, 60"},

    "blue": {"upper": "126, 255, 255",
            "lower":"94, 80, 2"},

    "brown": {"upper": "30,255,255", 
            "lower":"20,100,100"},

    "green": {"upper": "102, 255, 255",
            "lower":"25, 52, 72"},

    "orange": {"upper": "25, 255, 255",
            "lower":"10, 100, 20"},

    "pink": {"upper": "11,255,255",
            "lower":"10,100,100"},

    "black": {"upper": "50,50,100",
            "lower":"0,0,0"},

    "purple": {"upper": "120, 255, 255",
            "lower":"80, 10, 10]"},

    "yellow": {"upper": "44, 255, 255",
            "lower":"24, 100, 100"},

    "white": {"upper": "0,0,255",
            "lower":"0,0,0"},
            }
    return colors[color]["upper"] , colors[color]["lower"]

def colordetect(frame,color,w=320,h=240):
     up, low = colors(color)
     low1 = low.split(",")
     up1 = up.split(",")
     colorLower = (int(low1[0]),int(low1[1]),int(low1[2]))
     colorUpper = (int(up1[0]),int(up1[1]),int(up1[2]))


     frame = imutils.resize(frame, width=w, height=h) 
     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
     mask = cv2.inRange(hsv, colorLower, colorUpper) 
     mask = cv2.erode(mask, None, iterations=2) 
     mask = cv2.dilate(mask, None, iterations=2)
     cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
     cv2.CHAIN_APPROX_SIMPLE)[-2]
     center = None
     cv2.putText(frame,"Rovpy", (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
     if len(cnts) > 0:

             c = max(cnts, key=cv2.contourArea)
             ((x, y), radius) = cv2.minEnclosingCircle(c)
             M = cv2.moments(c)
             center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))


             if radius > 10:
                 cv2.circle(frame, (int(x), int(y)), int(radius),
                 (0, 255, 255), 2)
                 cv2.circle(frame, center, 5, (0, 0, 255), -1)
     else:
          x = 0
          y = 0
          radius = 0
     return frame ,x ,y, radius

def circledetect(frame,param1=35,param2=50,minRadius=0,maxRadius=0,w=320,h=240):    
    global x,y,r
    frame = imutils.resize(frame, width=w, height=h)
    output = frame.copy()
    cv2.putText(output,"Rovpy", (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),0);
    gray = cv2.medianBlur(gray,5)
    gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,3.5)
    kernel = np.ones((5,5),np.uint8)
    gray = cv2.erode(gray,kernel,iterations = 1)
    gray = cv2.dilate(gray,kernel,iterations = 1)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius) 
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int") 
        for (x, y, r) in circles:
    
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            
    else:
        x = 0
        y = 0
        r = 0
    return output,x,y,r

def connectrov(mode="STABILIZE",connect="/dev/ttyACM0"):
    try:
        master = mavutil.mavlink_connection(connect,baud=115200)
    except:
        master = mavutil.mavlink_connection(connect)
    master.wait_heartbeat()

    if mode not in master.mode_mapping():
        print('Mode not found : {}'.format(mode))
        print('you can check : ', list(master.mode_mapping().keys()))
        exit(1)
    """
    Ardusub destekleyen modlar
        0: 'STABILIZE',
        1: 'ACRO',
        2: 'ALT_HOLD',
        3: 'AUTO',
        4: 'GUIDED',
        7: 'CIRCLE',
        9: 'SURFACE',
        16: 'POSHOLD',
        19: 'MANUAL',
    """
    mode_id = master.mode_mapping()[mode]
    master.mav.set_mode_send(master.target_system,mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,mode_id)
    return master

#master.arducopter_arm() #robotu arm yapmak
#master.arducopter_disarm() #robotu disarm yapmak
def arm():
    connectrov.arducopter_arm()
def disarm():
    connectrov.arducopter_disarm()
def hiz(value):
    hizMin = -1 
    hizMax = 1 
    pwmMin = 1100 
    pwmMax = 1900 
    hizSpan = hizMax - hizMin
    pwmSpan = pwmMax - pwmMin
    valueScaled = float(value - hizMin) / float(hizSpan)
    return pwmMin + (valueScaled * pwmSpan)

def control(id, pwm=0):
    if id < 1:
        print("Channel 1 ve 9 araliginda olmalidir.")
        return

    if id < 9:
        rc_channel_values = [65535 for _ in range(8)]
        rc_channel_values[id - 1] = hiz(pwm)
        connectrov.mav.rc_channels_override_send(
            connectrov.target_component,             
            *rc_channel_values)
def sendgps(timestamp=0,idd=0,flags=8|16|32,gpstime=0,gpsweeknumber=0,dgps=3,lat=0,lon=0,alt=0,gpshdop=1,gpsvdop=1,northvelocity=0,eastvelocity=0,downvelocity=0,gpsspeed=0,gpshorizontal=0,gpsvertical=0,numberofsattalities=7):
    connectrov.mav.gps_input_send(
        timestamp,          #Timestamp (micros since boot or Unix epoch)
        idd,          #ID of the GPS for multiple GPS inputs
        flags,    #Flags indicating which fields to ignore (see GPS_INPUT_IGNORE_FLAGS enum). All other fields must be provided.
        gpstime,          #GPS time (milliseconds from start of GPS week)
        gpsweeknumber,          #GPS week number
        dgps,          #0-1: no fix, 2: 2D fix, 3: 3D fix. 4: 3D with DGPS. 5: 3D with RTK
        lat,          #Latitude (WGS84), in degrees * 1E7
        lon,          #Longitude (WGS84), in degrees * 1E7
        alt,          #Altitude (AMSL, not WGS84), in m (positive for up)
        gpshdop,          #GPS HDOP horizontal dilution of position in m
        gpsvdop,          #GPS VDOP vertical dilution of position in m
        northvelocity,          #GPS velocity in m/s in NORTH direction in earth-fixed NED frame
        eastvelocity,          #GPS velocity in m/s in EAST direction in earth-fixed NED frame
        downvelocity,          #GPS velocity in m/s in DOWN direction in earth-fixed NED frame
        gpsspeed,          #GPS speed accuracy in m/s
        gpshorizontal,          #GPS horizontal accuracy in m
        gpsvertical,          #GPS vertical accuracy in m
        numberofsattalities           #Number of satellites visible.
    )
def rovinfo():
    return connectrov.recv_match().to_dict()

def pitch(speed):
    control(1,speed)
def roll(speed):
    control(2,speed)
def throttle(speed):
    control(3,speed)
def yaw(speed):
    control(4,speed)
def forward(speed):
    control(5,speed)
def lateral(speed):
    control(6,speed)
def camerapan(speed):
    control(7,speed)
def cameratilt(speed):
    control(8,speed)
def light1level(power):
    control(9,power)
def light2level(power):
    control(10,power)
def videoswitch(speed):
    control(11,speed)