#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#
#  Copyright 2017  <odroid@odroid>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABLITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


def main(args):

    return 0
    

def encoding(data):
    newdata = data.encode("utf-8")
    return newdata

def sending():
    end = True
    while end:
        data = input()
        data = data.encode("utf-8")
        conn.send(data)

    conn.close()

def vfd_write1(string):

    port1.write("1b4c0000".decode("hex"))
    port1.write(string)

def vfd_write2(string):

    port1.write("1b4c0001".decode("hex"))
    port1.write(string)
def vfd_clr():

    port1.write("1b43".decode("hex"))

def getting():
    global end_socket
    global wait_final
    global set_millis
    global send_flag
    global retry_cnt           
    global conn
    while end_socket == True:
       
        while wait_final == True:
            pass
        
        print('\r\nsocket wait\r\n')
        port.write('\r\n<SP_ACK>HOTSPOT</SP_ACK>\r\n'.encode("utf-8"))
        vfd_clr()
        vfd_write1(' HOTSPOT ENABLE ')
        vfd_write2('  SOCKET WAIT   ')
        send_flag=0
        retry_cnt=0
        try:
            HOST = '192.168.43.1'
            PORT = 1470
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST,PORT))
            s.listen(1)
            conn,addr = s.accept()
        except socket.error as e:
            print(e)
            break
        end_socket1 = True
        print('connected by',addr)

        while end_socket1:
            data = conn.recv(1024)           
                        
            if not data:
                break
            
            else:
                try:
                    #data = str(data).split("b'",1)[1],rsplit("'",1)[0]
                    data = str(data)
                except ZeroDivisionError as e:
                    print(e)
                else:
                    print(data)
                    #hexdata = data.encode("hex")
                    #print(hexdata)

                if data == 'exit\r':

                    conn.send(encoding('good bye'))
                    end_socket = False
                    global end_program
                    end_program = False                

                if data == '\r\n<TX_READY/>\r\n':                    
                    
                    if send_flag == 0:
                        retry_cnt=0
                        set_millis = time.time()                        
                    send_flag=1
                    send_socket()
                    vfd_clr()
                    vfd_write1(' <SOCKET TEST>  ')
                    vfd_write2('T-T> GOT TX_RDY ')
                    

                if data == '\r\n<TX_BEGIN/>\r\n':
                    
                    if send_flag == 1:
                        retry_cnt=0
                        set_millis = time.time()
                        send_socket()
                    send_flag=2                   
                    vfd_clr()
                    vfd_write1(' <SOCKET TEST>  ')
                    vfd_write2('T-T> GOT TX_BGN ')
                    

                if data == 'START\r\n12345567890ABCDEFGHIJKLMNOPQRSTUVWXYZ\r\nEND':
                    
                    if send_flag == 2:
                        retry_cnt =0
                        set_millis = time.time()
                        send_socket()
                    send_flag=3                    
                    vfd_clr()
                    vfd_write1(' <SOCKET TEST>  ')
                    vfd_write2('T-T> GOT TX_DATA')
                    
                    #print(len(data))
                    
                #if (send_flag == 2) and (len(data) >=49)


                if data == '\r\n<TX_END/>\r\n':
                    
                    if send_flag == 3:
                        retry_cnt = 0
                        set_millis = time.time()
                        send_socket()                        
                    send_flag=4                    
                    vfd_clr()
                    vfd_write1(' <SOCKET TEST>  ')
                    vfd_write2('T-T> GOT TX_END ')
                    

                if data == '\r\n<TX_RX_CHANGE/>\r\n':
                    
                    if send_flag == 4:
                        retry_cnt = 0
                        set_millis = time.time()
                        send_socket()
                    send_flag=5                   
                    vfd_clr()
                    vfd_write1(' <SOCKET TEST>  ')
                    vfd_write2('T-T> GOT CHANGE ')
                    

                if data == '\r\n<RX_BEGIN_ACK/>\r\n':                    
                    
                    if send_flag == 5:
                        retry_cnt = 0
                        set_millis = time.time()
                        send_socket()
                    send_flag=6                    
                    vfd_clr()
                    vfd_write1(' <SOCKET TEST>  ')
                    vfd_write2('R-T> GOT RX_RD_A')
                    

                if data == '\r\n<RX_DATA_ACK/>\r\n':                    
                    
                    if send_flag == 6:
                        retry_cnt = 0
                        set_millis = time.time()
                        send_socket()
                    send_flag=7                    
                    vfd_clr()
                    vfd_write1(' <SOCKET TEST>  ')
                    vfd_write2('R-T> GOT RX_DT_A')
                    

                if data == '\r\n<RX_FINAL/>\r\n':
                    
                    print('<SP_FINAL/>')
                    vfd_clr()
                    vfd_write1(' <SOCKET TEST>  ')
                    vfd_write2('R-T> GOT SP_FIN ')
                    port.write('<SP_FINAL/>'.encode("utf-8"))
                    end_socket1=False
                    wait_final=True
                    conn.close()
                    s.close()
                    del s

                else:
                    pass
                
            if (set_millis + wait_time) < time.time(): #retry count
                retry_cnt=retry_cnt+1
                print(retry_cnt)
                send_socket()
                set_millis = time.time()
                
                if retry_cnt > 2:
                    print('retry_over')
                    vfd_clr()
                    vfd_write1('  <Retry Over>  ')
                    vfd_write2('PLEASE RESET....')
                    end_socket1=False
                    wait_final=True
                    conn.close()
                    s.close()                    
                    del s
            
            if (set_millis + total_time) < time.time():
                print('time over')
                vfd_clr()
                vfd_write1('   <Time Over>  ')
                vfd_write2('PLEASE RESET....')
                end_socket1=False
                wait_final=True
                conn.close()
                s.close()
                del s
                
            #conn.close()
            #s.close()



def send_socket():
    global send_flag
    global conn
    if send_flag == 1:
        conn.send(encoding('\r\n<TX_READY_ACK/>\r\n'))
        print('AP>TX_RD_ACK')
        vfd_write2('T-T> SD TX_RD_A ')
        
    elif send_flag == 2:
        conn.send(encoding('\r\n<TX_BEGIN_ACK>\r\n'))
        print('AP>TX_BG_AK')
        vfd_write2('T-T> SD TX_BG_A ')
        
    elif send_flag == 3:
        conn.send(encoding('\r\n<TX_DATA_ACK/>\r\n'))
        print('AP>TX_DT_AK')
        vfd_write2('T-T> SD TX_DT_A ')
        
    elif send_flag == 4:
        conn.send(encoding('\r\n<TX_OK/>\r\n'))
        print('AP>TX_OK')
        vfd_write2('T-T> SD TX_OK ')
        
    elif send_flag == 5:
        conn.send(encoding('\r\n<RX_BEGIN/>\r\n'))
        print('AP>RX_BG')
        vfd_write2('T-T> SD RX_BG_A ')
        
    elif send_flag == 6:
        conn.send(encoding('START\r\n12345567890ABCDEFGHIJKLMNOPQRSTUVWXYZ\r\nEND'))
        print('AP>SEND_DT')
        vfd_write2('T-T> SD DT ')
        
    elif send_flag == 7:
        conn.send(encoding('\r\n<RX_END/>\r\n'))
        print('AP>RX_END')
        vfd_write2('T-T> SD RX_END ')
        

    
        
        


def uartgetting():
    global end_socket1
    global end_socket
    global end_program
    global wait_final
    global conn
    global s
    end_uart = True
    i=0
    while end_uart:
        global rcv
        rcv += readlineCR(port)
        if rcv is None:
            pass
        else:

            if rcv.find('<SP_MAC>') != -1 and rcv.rfind('</SP_MAC>') == rcv.find('<SP_MAC>')+25:
                print(rcv[rcv.find('<SP_MAC>')+8:rcv.rfind('</SP_MAC>') ] )
                rcv=""
                port.write('<SP_SSID_ACK>AP</SP_SSID_ACK>'.encode("utf-8"))

            if rcv.find('<SP_FINAL_ACK/>') != -1:
                rcv=""               
                end_socket1 = True                
                wait_final = False
                vfd_clr()
                vfd_write1('SYSTEM')
                vfd_write2('    INITIALIZING')
                time.sleep(1)
                if conn != None:
                    conn.close()
                if s != None:
                    s.close()
                    del s
                vfd_clr()
                vfd_write1(' HOTSPOT ENABLE ')
                vfd_write2('  SOCKET WAIT   ')
                
                
                
            if rcv.find('test') != -1:
                
                port1.write("1b4c0001".decode("hex"))
                port1.write("010101010101".decode("hex"))
                
                
                
            if rcv.find('<RE_BOOT/>') != -1:
                rcv=""
                os.system('reboot')

            if rcv.find('end_program') != -1:
                rcv=""
                end_socket=False
                end_socket1=False
                end_program=False
                print('End this program.')
                if conn != None:
                    conn.close()
                if s != None:
                    s.close()
                    del s
                

           

                #print(rcv)
                #rcv =""

            #print(rcv)
            #hexdata = rcv.encode("hex")
            #print(hexdata)




def readlineCR(port):
    rv = ""
    ch = port.read()
    rv += ch
    return rv

def change_ssid():
    f = open('/home/odroid/Documents/setupwifi.txt','r')
    s = f.read()
    b = s.strip()
    SSIDCHANGE = 'sed -i "14s/.*/'+b+'/g" /etc/hostapd/hostapd.conf'
    subprocess.call(SSIDCHANGE,shell=True)



if __name__ == '__main__':
    import os
    import sys
    import subprocess
    import socket
    import threading
    import serial
    import time

    end_socket = True
    end_socket1 = True
    end_program = True
    wait_final = False
    conn = None
    s = None
    set_millis = 0
    wait_time = 1
    total_time = 10
    send_flag = 0
    retry_cnt=0
    rcv=""
    change_ssid()
    subprocess.call('service hostapd start',shell=True)
    
    port = serial.Serial("/dev/ttyUSB0",baudrate=9600,
    parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

    port1 = serial.Serial("/dev/ttyUSB1",baudrate=9600,
    parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

    print('port is open = ', port.isOpen())
    print('port1 is open = ', port1.isOpen())
    
    vfd_clr()
    vfd_write1('SYSTEM')
    vfd_write2('    INITIALIZING')
    
    time.sleep(2)
    
    threading._start_new_thread(getting,())
    threading._start_new_thread(uartgetting,())


    while end_program:
        pass
    sys.exit(main(sys.argv))


#port.write('hello'.encode("utf-8"))
