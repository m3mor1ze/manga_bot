def extructor_width(string):
    start = string.find('"', string.__len__() - 12)
    end = string.__len__()
    url = string[start:end]
    url = url.replace('"', "")
    url = url.replace(',', "", 1)
    x = url.split(",")
    width = x[0]
    return width

def extructor_height(string):
    start = string.find('"', string.__len__() - 12)
    end = string.__len__()
    url = string[start:end]
    url = url.replace('"', "")
    url = url.replace(',', "", 1)
    x = url.split(",")
    height = x[1]
    return height

def extructor_links(string):
    start = string.find('https')
    len = string.__len__() - 13
    end = string.find('"', len)
    url = string[start:end]
    url = url.replace(',', "")
    url = url.replace('"', "")
    url = url.replace("'", "")
    tmp_str = string[end:string.__len__()]
    id = tmp_str.find('"')
    tmp_str = tmp_str[0:id]
    tmp_str = tmp_str.replace('"', '')
    url = url + tmp_str
    return url

i = 0
with open("parse_example.txt", "r") as file:
    for line in file:
        i += 1
        if i == 7:
            i = 0

line = line.replace(']', '\n')
links_list = line.split('\n')
width = 0
height = 0

links_list.pop()
links_list.pop()
links_list.pop()
links_list.pop()

width_list=[]
height_list=[]
while i != links_list.__len__():
    width_list.append(extructor_width(links_list[i]))
    height_list.append(extructor_height(links_list[i]))
    links_list[i] = extructor_links(links_list[i])
    i += 1

print(links_list)
print(width_list)
print(height_list)