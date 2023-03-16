def extructor(string):
    # Извлечение URL
    start = string.find('https')
    end = string.find('.jpg') + 4
    url = string[start:end]
    url = url.replace(',', "")
    url = url.replace('"', "")
    url = url.replace("'", "")
    # Вывод URL
    # print(url)

    tmp_str = string[end:string.__len__()]
    id = tmp_str.find('"')
    # print("id =", id)
    # print("s =", tmp_str)
    tmp_str = tmp_str[0:id]
    # print("s =", tmp_str)
    tmp_str = tmp_str.replace('"', '')
    print("url =", url)
    print("tmp_str =", tmp_str)
    url = url + tmp_str
    # print("URL = ", url)

    return url


i = 0
with open("parse_example.txt", "r") as file:
    for line in file:
        i += 1
        if i == 7:
            i = 0
# print(line)
line = line.replace(']', '\n')
line = line.replace(',', "")
#line = line.replace('"', "")
line = line.replace("'", "")
lil = line.split('\n')
while i != lil.__len__():
    print("lil[",i,"] = ", lil[i])
    print("src[",i,"] = ",extructor(lil[i]), "\n")
    i += 1
