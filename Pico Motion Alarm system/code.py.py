import machine
import time
from lcd1602 import LCD
import utime

SEGCODE = [0x6f,0x7f,0x07,0x7d,0x6d,0x66,0x4f,0x5b,0x06,0x3f]

sdi = machine.Pin(0,machine.Pin.OUT)
rclk = machine.Pin(1,machine.Pin.OUT)
srclk = machine.Pin(2,machine.Pin.OUT)
pir_sensor = machine.Pin(14, machine.Pin.IN)
buzzer = machine.Pin(15, machine.Pin.OUT)
blue_button = machine.Pin(6,machine.Pin.IN)
red_button = machine.Pin(10,machine.Pin.IN)
blue_led = machine.Pin(7,machine.Pin.OUT)
red_led = machine.Pin(11,machine.Pin.OUT)
    
def BOOM():
    buzzer.toggle()
    lcd = LCD()
    string = " BOoOoOoOoO!\n"
    lcd.message(string)
    utime.sleep(2)
    string = "MMMMMMMMMMMMMMMM!!!"
    lcd.message(string)
    utime.sleep(1)
    lcd.clear()
    utime.sleep_ms(100)
    
def RedButton():
    for i in range(30):
        buzzer.toggle()
        utime.sleep_ms(100)
        
    for i in range(20):
        buzzer.toggle()
        utime.sleep_ms(60)
                        
        BOOM()
    
    
def motion_detected(pin):
    Motion = True
    lcd= LCD()
    lcd.message("Bir cisim yakla-\n  siyor efendim!!!")
    if Motion:
        for num in range(10):
            hc595_shift(SEGCODE[num])
            time.sleep_ms(500)
            
            if blue_button.value():
                blue_led.toggle()
                time.sleep(0.5)
                lcd.clear()
                lcd.message("Bomba imha\n")
                utime.sleep(1)
                lcd.message("   edilmistir!!!")
                Motion= False
                break
            
            elif red_button.value():
                RedButton()
                red_led.toggle()
                time.sleep(0.5)
                Motion= False
                break         
            else:
                Motion= True
            
    if Motion:
        RedButton()
        
    lcd.clear()
    Motion = False
       
print("Intruder Alarm Start!")

def hc595_shift(dat):
    rclk.low()
    time.sleep_ms(5)
    for bit in range(7, -1, -1):
        srclk.low()
        time.sleep_ms(5)
        value = 1 & (dat >> bit)
        sdi.value(value)
        time.sleep_ms(5)
        srclk.high()
        time.sleep_ms(5)
    time.sleep_ms(5)
    rclk.high()
    time.sleep_ms(5)
    
while True:
    pir_sensor.irq(trigger=machine.Pin.IRQ_RISING, handler=motion_detected)
        