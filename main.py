import pyb, sensor, image, time, os, tf
from machine import UART

# Settings
person_threshold = 0.7

# LED setting (1: red, 2: green, 3: blue, 4: IR)
led = pyb.LED(1)
led.off()

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.

net = tf.load('trained.tflite')
labels = ['person', 'no_person']

# Star the clock to measure FPS
clock = time.clock()

#Dinh nghia ham module sim
uart = UART(3, 115200, timeout_char=1000)                         # init with given baudrate
uart.init(115200, bits=8, parity=None, stop=1, timeout_char=1000) # init with given parameters

#Dinh nghia buzzer
#buzzer = Pin(4, PIN.IN, Pin.PULL_UP)

# Main while loop
while(True):

    # Measure time
    clock.tick()

    # Get image from camera
    img = sensor.snapshot()


    # default settings just do one detection... change them to search the image...
    for obj in net.classify(img, min_scale=1.0, scale_mul=0.0, x_overlap=0.0, y_overlap=0.0):

        # Give classification scores
        print("**********\nDetections at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
        for i in range(len(obj.output())):
            print("%s = %f" % (labels[i], obj.output()[i]))

        # Highlight identified object
        img.draw_rectangle(obj.rect())
        img.draw_string(obj.x()+3, obj.y()-1, labels[obj.output().index(max(obj.output()))], mono_space = False)

        # Light LED if person detected
        idx = labels.index('person')
        if obj.output()[idx] > person_threshold:
            led.on()
            ##########Khai bao module sim###################
            uart.write('ATD0966620946;\r')
            uart.read()
            #uart.write('AT+CMGS="0966620946\r')
            pyb.delay(10000)



            ##########Buzzer################
            #if buzzer.value() == 1:
                #beeper = PWM(Pin(14, Pin.OUT), freq=440, duty=512)

        else:
            led.off()
            #Neu khong co nguoi, thi dua MCU ve trang thai sleep
            #pyb.stop()

    print(clock.fps(), "fps")
