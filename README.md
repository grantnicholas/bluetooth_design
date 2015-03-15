# bluetooth_design
Code to communicate with the Adafruit nRF8001 bluetooth breakout board. 

[https://www.adafruit.com/product/1697](https://www.adafruit.com/product/1697)

##Special thanks to Nancy for her tutorial
[https://blog.adafruit.com/2014/07/28/gatttool-ubuntu-and-adafruits-nrf8001-bluetooth-low-energy-breakout-in-20-minutes/](https://blog.adafruit.com/2014/07/28/gatttool-ubuntu-and-adafruits-nrf8001-bluetooth-low-energy-breakout-in-20-minutes/)

##However I ran into a few issues with her tutorial:

1. Nancy's script was a bit complex and large for such a simple project. I favor small reusable components over big monolithic programs. 
2. Nancy only showed how to do data streaming from the computer to the Arduino. I needed to do 2-way data streaming.If you need help figuring that out look at this tutorial.  

###First read her tutorial which I attached here
As part of my work on Swarmbuddies (robots that dance to music and create formations) we decided to use bluetooth low energy for smartphone support, but also needed it to work on the desktop side for our computer vision software to work.

Here are the steps we needed to take to get it working.

1) Install Ubuntu 14.04

This is the easiest path. Really recommended, since bluez-5.20 wants some new version of dbus which can be installed on 12.04, but which will crash your computer incredibly hard when you reboot.

2) Install the latest version of bluez, bluez v 5.20 (or check http://www.kernel.org/pub/linux/bluetooth/ for the latest version), and uninstall your current version. Major help from jaredwolff.com/blog/get-started-with-bluetooth-low-energy for this step!

sudo apt-get remove bluez
sudo apt-get remove bluez-cups
sudo apt-get remove bluez-hcidump

wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.20.tar.xz
tar -xvf bluez-5.20.tar.xz
cd bluez-5.20/
sudo apt-get install libudev-dev libical-dev libreadline-dev
./configure –enable-library –disable-systemd
make
make check
sudo make install
sudo cp attrib/gatttool /usr/bin/

3) On the hardware side, your arduino should be hooked up and programmed as per Adafruit’s tutorial.

Let’s test your connection. Plugin your CSR 4.0 dongle ($6 on ebay) if your laptop doesn’t support bluetooth 4.0 (or even if it does, we’ve found the dongle to be more reliable):

sudo hcitool lescan

If this succeeds you should see a bunch of scrolling information, including the MAC address of the nrf8001 breakout, which should be something like “EF:FC:D3:56:41:B7″. If it says file descriptor not found or otherwise exits immediately, use

$ dmesg | tail

to check that your dongle is being recognized by your computer.

4) Open Arduino and the serial monitor. Now try writing wirelessly to the Arduino with gatttool

sudo gatttool -b EF:FC:D3:56:41:B7 -I -t random

> connect

The white characters should turn blue. Now try writing to the UART service:

char-write-cmd 0xb FF00FF

5) You should see “3 bytes received” and your command on the Arduino.

6) Now to script it!


##Now come back to my repo
Instead of using her script use my much simpler scripts

<code>python blue_write.py | decode.py > file_name.txt</code>

What does it do under the hood?

##blue_write.py
<code>
import os

os.system('gatttool -t random -b D9:84:67:85:30:19 -i hci0 --char-write-req --handle=0x00e -n 0100 --listen')
</code>

Ok this is literally just calling a shell command from python. So what does the shell command do?

it uses gatttool to 

1. connect to D9:84:67:85:30:19, the address of the bluetooth device. You need to change this to your device. 
2. connects using the hci0 interface
3. writes the characteristic with handle 0x000e to be 0100. the bytes 0100 signals that you want notifications when the bluetooth device sends data to your computer. By default these bytes are set to 0000 and you will get no notifcations of data. 
4. --listen says we want the device to listen constantly for data. 

Gatttool writes the data received to stndout, which is great! We can now pipe the output of this program to other programs for processing. 

##decode.py 
<code>
import re
import sys

rx = re.compile('value:(.+)')


def decode_line(aline):
    match_data = re.findall(rx, line)
    if match_data != []:
        match_data = match_data[0]
        no_whitespace = match_data.replace(' ', '')
        decoded = no_whitespace.decode('hex') 
        return decoded


for line in sys.stdin:
    var = decode_line(line)
    if var is not None:
        print var

</code>

This gathers information from stdin and decodes the input line by line and prints it to stdout. The decode_line function simply uses a regex to match only the data we care about (as gatttool prints out human readable stuff we dont care about). It then converts the data [which is sent as HEX over bluetooth] to ascii and returns the decoded line. 

Finally the output is written to a file of your choice. 

<code>python blue_write.py | decode.py > file_name.txt</code>

So that is the simple system I built to grab information from the Arduino over bluetooth using the standard linux/unix philosphy of programming. 

The other folders included here:

1. logged_data
2. process_data
3. upload_data

Are for my personal design project and are not needed but feel free to look through them if you're interested. 


