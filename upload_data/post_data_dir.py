import glob
import post_data as pd
import shutil


def main():
    for afilepath in glob.glob('/home/grant/Desktop/serial_py/upload_data/upload_files/*.txt'):
        pd.post_data(afilepath)
        file_name = afilepath.split('/')[-1]
        print file_name
        move_path = '/home/grant/Desktop/serial_py/upload_data/uploaded_files/{0}'.format(file_name)
        shutil.move(afilepath, move_path)

if __name__ == '__main__':
    main()
