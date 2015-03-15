import os
import time
import pexpect
import re


os.system('gatttool -t random -b D9:84:67:85:30:19 -i hci0 --char-write-req --handle=0x00e -n 0100 --listen')

# while True:
# 	time.sleep(.01)
# 	os.system("gatttool -t random -b D9:84:67:85:30:19 --char-write -a 0x00b -n 505050;")
# 	# pexpect.run('gatttool -t random -b D9:84:67:85:30:19 --char-write -a 0x00b -n 505050;')
# 	