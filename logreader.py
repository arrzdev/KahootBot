last = ''

while True:
    with open('logs.txt', 'r') as f:
        last_line = f.readlines()[-1]
        
    if last_line != last:
        print(last_line)
        last = last_line
