import os


os.system('gatttool -t random -b D9:84:67:85:30:19 -i hci0 --char-write-req --handle=0x00e -n 0100 --listen')
