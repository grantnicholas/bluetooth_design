import math
from dateutil import parser


def mean(arr):
    asum = sum(arr)
    amean = asum / len(arr)
    return amean


def stdev(arr):
    amean = mean(arr)
    asum = 0.0
    for v in arr:
        asum += (v - amean) ** 2

    return math.sqrt(asum / len(arr))


def get_dist(xval, yval, zval):
    return math.sqrt(xval ** 2 + yval ** 2 + zval ** 2)


def get_arrs(filename):
    time_arr = []
    r_arr = []
    with open(filename, 'r') as f:
        for line in f:
            if line != "\n":
                print line
                try:
                    time, xval, yval, zval = map(int, line.split(','))
                    time = float(time) / 1000.0
                    rval = get_dist(xval, yval, zval)
                    time_arr.append(time)
                    r_arr.append(rval)
                except:
                    pass

    return time_arr, r_arr


def process_data(arrs):

    t, z = arrs
    m_z = mean(z)
    s_z = stdev(z)
    num_stdevs = 3

    z_cut_up = m_z + num_stdevs * s_z
    z_cut_down = m_z - num_stdevs * s_z

    print m_z
    print z_cut_up
    print z_cut_down

    time_total = 0
    time_start = 0
    time_recent = 0
    time_cut = 1  # 5000 in ms
    top_cut = z_cut_up
    bot_cut = z_cut_down
    count = 0

    for i in range(len(z)):
        if (z[i] > top_cut) or (z[i] < bot_cut):
            if t[i] - time_recent > time_cut:
                if time_recent - time_start > time_cut:  # %time_cut
                    count = count + 1

                time_total = time_total + (time_recent - time_start)
                time_start = t[i]
                time_recent = t[i]
            else:
                time_recent = t[i]

    count = count + 1
    print time_total, t[i]
    if time_recent != 0:
        time_total = time_total + (time_recent - time_start)

    return count, time_total


def process_file(infile, outfile):
    data = get_arrs(infile)
    count, total_time = process_data(data)
    name = "treadmill"
    date = parser.parse('March 13 2014')
    print name
    print count, total_time
    with open(outfile, 'w') as f:
        f.write("name: " + str(name) + "\r\n")
        f.write("date: " + str(date) + "\r\n")
        f.write("count: " + str(count) + "\r\n")
        f.write("time: " + str(total_time) + "\r\n")


def main():
    process_file('log.txt', 'output.txt')

if __name__ == '__main__':
    main()
