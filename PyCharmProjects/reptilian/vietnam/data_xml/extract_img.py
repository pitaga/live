import os
import sys
import re
import time
import base64


def extract_data(filename, dir):
    file = open(filename, "r")
    content = file.read()
    index = 0
    for match in re.finditer(r'(?=/9j)(.|\n)*?(?=(\n\n))', content):
        index = index + 1
        print("%s/%s.jpg" % (dir, index))
        newfile = open("%s/%s.jpg" % (dir, index), "wb")
        real = re.sub("\n", "", match.group())
        length = len(real)
        times = (4 - length % 4) % 4
        i = 0

        while i < times:
            real = "%sA===" % real
            i = i + 1

        # newfile.write(real)
        newfile.write(base64.b64decode(real))
        newfile.close()
    file.close()


def export_file(file_path):
    r = re.search(r"(?<=\\|/).*", file_path)
    file_name_ext = file_path
    while r != None:
        r = r.group()
        file_name_ext = r
        r = re.search(r"(?<=\\|/).*", r)

    pattern = "%s" % file_name_ext
    pattern = re.sub("\[", "\\\[", pattern)
    pattern = re.sub("\]", "\\\]", pattern)
    pattern = re.sub("\(", "\\\(", pattern)
    pattern = re.sub("\)", "\\\)", pattern)
    pattern = ".*?(?=%s)" % pattern

    path = re.search(pattern, file_path)
    if path != None:
        path = path.group()
    else:
        path = ""
    dot = re.search(r"\.", file_name_ext)
    file_name = file_name_ext
    if dot != None:
        file_name = re.search(r".*?(?=\.)", file_name_ext)
        file_name = file_name.group()
    else:
        file_name = file_name + "_dir"

    full_path = path + file_name
    bExist = os.path.exists(full_path)
    if bExist != True:
        os.mkdir(full_path)
    else:
        print("The Directory \"%s\" Exists!\n" % full_path)
    extract_data(file_path, full_path)


def main():
    print(os.name)

    index = 0
    for arg in sys.argv:
        index += 1
        if index == 1:
            continue
        if index == 2:
            export_file(arg)

    if index == 1:
        file_path = "source.mhtml"
        export_file(file_path)


if __name__ == "__main__":
    main()
    print("just wait for 2 seconds!\n")
    time.sleep(2)