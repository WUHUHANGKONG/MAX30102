from machine import SPI, Pin,I2C,PWM
import max30102
import st7789
import urequests
import network
import utime
import ujson
import gc
spi = SPI(0, baudrate=40000000, polarity=1, phase=0, bits=8, endia=0, sck=Pin(6), mosi=Pin(8))
display = st7789.ST7789(spi, 240, 240, reset=Pin(11,func=Pin.GPIO, dir=Pin.OUT), dc=Pin(7,func=Pin.GPIO, dir=Pin.OUT))
display.init()
backgroud_clr = st7789.color565(255, 255, 255) #设置背景颜色为白色
display.fill(backgroud_clr)
i2c = I2C(1, sda=Pin(0), scl=Pin(1),freq=400000)
def draw_start_enum():
    

    display.fill_rect(20, 40, 5, 20, st7789.color565(239, 91, 91))
    display.fill_rect(25, 35, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(30, 30, 20, 5, st7789.color565(239, 91, 91))
    display.fill_rect(50, 35, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(55, 40, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(60, 35, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(65, 30, 20, 5, st7789.color565(239, 91, 91))
    display.fill_rect(85, 35, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(90, 40, 5, 20, st7789.color565(239, 91, 91))
    display.fill_rect(85, 60, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(80, 65, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(75, 70, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(70, 75, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(65, 80, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(60, 85, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(55, 90, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(50, 85, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(45, 80, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(40, 75, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(35, 70, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(30, 65, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(25, 60, 5, 5, st7789.color565(239, 91, 91))
    display.fill_rect(30, 35, 20, 5, st7789.color565(250, 142, 142))
    display.fill_rect(65, 35, 20, 5, st7789.color565(250, 142, 142))
    display.fill_rect(25, 40, 30, 5, st7789.color565(250, 142, 142))
    display.fill_rect(60, 40, 30, 5, st7789.color565(250, 142, 142))
    display.fill_rect(25, 45, 65, 5, st7789.color565(250, 142, 142))
    display.fill_rect(25, 50, 65, 5, st7789.color565(250, 142, 142))
    display.fill_rect(25, 55, 65, 5, st7789.color565(250, 142, 142))
    display.fill_rect(30, 60, 55, 5, st7789.color565(250, 142, 142))
    display.fill_rect(35, 65, 45, 5, st7789.color565(250, 142, 142))
    display.fill_rect(40, 70, 35, 5, st7789.color565(250, 142, 142))
    display.fill_rect(45, 75, 25, 5, st7789.color565(250, 142, 142))
    display.fill_rect(50, 80, 15, 5, st7789.color565(250, 142, 142))
    display.fill_rect(55, 85, 5, 5, st7789.color565(250, 142, 142))
def heart_beat():
    draw_start_enum()
    utime.sleep(0.5)
    display.fill_rect(20,30,75,75,st7789.color565(255,255,255))
    utime.sleep_ms(500)
sta_wlan = network.WLAN(network.STA_IF)#创建一个站点模式的WLAN对象
sta_wlan.active(True)
sta_wlan.scan()
sta_wlan.connect('iQOO Neo5', '123123123', security=network.AUTH_PSK)
while(sta_wlan.config() == '0.0.0.0'):
        utime.sleep(1)


print('Connected...')
display.line(40,105,40,225,st7789.color565(0,0,233))
display.line(40,225,225,225,st7789.color565(0,0,233))
display.line(40,120,40,224,st7789.color565(0,233,0))

display.draw_string(15,210,"50",size=2,color=st7789.color565(0,0,233))
display.draw_string(15,160,"70",size=2,color=st7789.color565(0,0,233))
display.draw_string(5,110,"90",size=2,color=st7789.color565(0,0,233))
url="http://post.blackwalnut.zucc.edu.cn/thingswise/idos/jets/streams/dev/32101289/HRSPO2___MAX30102.max30102Data_input_json"
headers = {
    "content-type": "application/json",
}
formData = {
    'data':{
        "case": "healthcondition",
        "sensor": "MAX30102"
    },
    'auth':{
        'user': 'demo',
        'password': '123@abc456D'
    }
}


m=max30102.Max30102(i2c)
cnt=1
hr=70
x_old=40
y_old=225
while True:
    
    red,ir=m.read_fifo()
    R=red/ir
    print(red,ir)
    if red<20228:
        
        display.fill_rect(41,120,190,130,st7789.color565(255,255,255))
        display.draw_string(50,105,"place finger",size=3,color=st7789.color565(250, 142, 142))
        display.fill_rect(40,225,165,120,st7789.color565(255,255,255))
    else:
        hr=str(int(30/30000*(red-230000)+65))
        spo2=str(int(-45.060*R*R+36.354*R+94.845))
    

        print(red,ir,spo2,hr)
        if int(hr)>50 and int(hr)<100:
            
            x_new=x_old+10
            y_new=225-(int(hr)-50)*3
            display.line(x_old,y_old,x_new,y_new,st7789.color565(0,0,0))
            x_old=x_new
            y_old=y_new
            cnt=cnt+1

            if(int(hr)>78):
                p = PWM(3, Pin(12))
                p.freq(1048)
                p.duty(50)
                utime.sleep(0.1)
                p.duty(0)


            if cnt==19:
                display.fill_rect(41,105,190,135,st7789.color565(255,255,255))
                display.line(40,225,225,225,st7789.color565(0,0,233))
                x_old=40
                y_old=240-(int(hr)-45)
                cnt=1
        display.fill_rect(45, 100, 180,50, st7789.color565(255, 255, 255))
        display.draw_string(90,10,"HR %s " %str(int(hr)),size=3,color=st7789.color565(0,0,233))
        display.draw_string(90,50,"Spo2 %s" %str(int(spo2)),size=3,color=st7789.color565(0,0,233))
        utime.sleep_ms(50)
        display.fill_rect(90,10,130,80,st7789.color565(255,255,255))
    while 1:
        try:
            HR=int(hr)
            Spo2=int(spo2)    

            formData['data']['HR'] = HR
            formData['data']['Spo2'] = Spo2
                
            res = urequests.post(url, data=ujson.dumps(formData),
                        headers=headers)
            print(res.status_code)
            print(res.text)
        except Exception as err:
            print(err)
        gc.collect()

        break    

           
                

