from time import sleep
def progress_s(percent=0, width=30):
    left = width * percent // 100
    right = width - left
    print('\r[', '#' * left, ' ' * right, ']',f' {percent:.0f}%',sep='', end='', flush=True)
def progress(s)
    for i in range(101):
        progress(i)
        sleep(s)
