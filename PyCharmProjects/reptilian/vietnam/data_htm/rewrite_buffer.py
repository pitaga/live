start = "../vietnam/start.txt"
end = "../vietnam/source.txt"


start_file = open(start, 'r')
end_file = open(end, 'r')

start_list = start_file.read().split()
end_list = end_file.read().split()

start_file.close()
end_file.close()


result = open(end, 'w')
lst = list(set(end_list) - set(start_list))
for item in lst:
    result.write(item + '\n')
result.close()

file = open(start, 'w')
file.write("")
file.close()
