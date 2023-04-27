import os


def remove_comments_and_empty_lines(lines):
    comments = []
    comment = False
    startIndex = 0
    for i, line in enumerate(lines):
        if comment:
            if len(line) > 3 and line.strip()[-3:] == '"""':
                comments.append((startIndex, i))
                comment = False
        else:
            if len(line) > 3 and line.strip()[:3] == '"""' and line.strip()[-3:] == '"""':
                comments.append((i,))
            elif len(line) > 3 and line.strip()[:3] == '"""':
                comment = True
                startIndex = i
            if len(line) > 1 and line.strip()[0] == "#":
                comments.append((i,))
            if line == '\n':
                comments.append((i,))
    for j, cmt in enumerate(comments):
        erased = 0
        for ci in range(j):
            if len(comments[ci]) > 1:
                erased += comments[ci][1] - comments[ci][0] + 1
            else:
                erased += 1
        if j != 0:
            if len(comments[j]) > 1:
                comments[j] = comments[j][0] - erased, comments[j][1] - erased
            else:
                comments[j] = comments[j][0] - erased,
    for c in comments:
        if len(c) < 2:
            lines.pop(c[0])
        else:
            for _ in range(c[1] - c[0] + 1):
                lines.pop(c[0])

    return lines


def calc_independent_function_loc(filtered_lines):
    functions = []
    is_function = False
    start_index = 0
    for i, line in enumerate(filtered_lines):
        if is_function:
            if line[:4].strip() != "" or i == len(filtered_lines)-1:
                if i == len(filtered_lines)-1:
                    functions.append((start_index, i+1))
                else:
                    functions.append((start_index, i))
                is_function = False
                if line[:4] == "def ":
                    is_function = True
                    start_index = i
        else:
            if line[:4] == "def ":
                is_function = True
                start_index = i
    return len(functions), list(map(lambda x: x[1] - x[0], functions))


def calc_classes_loc(filtered_lines):
    classes = []
    is_class = False
    start_index = 0
    for i, line in enumerate(filtered_lines):
        if is_class:
            if line[:4].strip() != "" or i == len(filtered_lines) - 1:
                if i == len(filtered_lines) - 1:
                    classes.append((start_index, i + 1))
                else:
                    classes.append((start_index, i))
                is_class = False
                if line[:6] == "class ":
                    is_class = True
                    start_index = i
        else:
            if line[:6] == "class ":
                is_class = True
                start_index = i

    class_methods_loc = calc_methods_loc(filtered_lines, classes)
    return len(classes), list(map(lambda x: x[1] - x[0], classes)), class_methods_loc


def calc_methods_loc(filtered_lines, classes):
    methods = []
    is_method = False
    start_index = 0
    for _class in classes:
        class_methods_loc = []
        for i in range(_class[0], _class[1]):
            if is_method:
                if filtered_lines[i][:8].strip() != "" or i == len(filtered_lines) - 1 or i == _class[1]-1:
                    if i == len(filtered_lines) - 1:
                        class_methods_loc.append((start_index, i + 1))
                    else:
                        class_methods_loc.append((start_index, i))
                    is_method = False
                    if filtered_lines[i][:8].strip() == "def":
                        is_method = True
                        start_index = i
            else:
                if filtered_lines[i][:8].strip() == "def":
                    is_method = True
                    start_index = i
        methods.append(class_methods_loc)

    return [len(class_method) for class_method in methods], [list(map(lambda x: x[1]-x[0], method)) for method in methods]


def count_loc(filename):
    with open(filename) as fileObj:
        lines = fileObj.readlines()
        filtered_lines = remove_comments_and_empty_lines(lines)
        independent_function_loc = calc_independent_function_loc(filtered_lines)
        class_loc = calc_classes_loc(filtered_lines)
        return len(filtered_lines), independent_function_loc, class_loc[:2], class_loc[-1]

#replace the below string with your path to the package folder
#and don't forget to add two '\\' like given
target_path = "C:\\Users\\kgavu\\Downloads\\xml\\xml" 

total_loc = 0
directories = list((os.walk(target_path)))
modules = []
modules_loc = []
submodules = []
submodules_loc = []
independent_function_loc = []
class_loc = []
methods_loc = []

for index, (path, dirs, files) in enumerate(directories):
    module_loc = 0
    submodule_loc = []
    sub_independent_function_loc = []
    sub_class_loc = []
    sub_methods_loc = []
    for file in files:
        file_loc = count_loc(path + '\\' + file)
        module_loc += file_loc[0]
        submodule_loc.append(file_loc[0])
        sub_independent_function_loc.append(file_loc[1])
        sub_class_loc.append(file_loc[2])
        sub_methods_loc.append(file_loc[3])

    if index == 0:
        modules = dirs
    else:
        submodules.append(files)
        modules_loc.append(module_loc)
        submodules_loc.append(submodule_loc)
        independent_function_loc.append(sub_independent_function_loc)
        class_loc.append(sub_class_loc)
        methods_loc.append(sub_methods_loc)

    total_loc += module_loc

print("---------Total LOC----------")
print(total_loc)
print()
print("---------Module LOC----------")
print("No. of modules: ", len(modules))
print()
print("LOC of each module:", dict(zip(modules, modules_loc)))
print()

print("---------Sub-Module LOC----------")
print("No. of sub-modules under each module: ", list(map(lambda x: len(x), submodules)))
print()
print("LOC of sub-modules under each module: ")
for keys, values in zip(submodules, submodules_loc):
    print(dict(zip(keys, values)))
print()

print("---------Independent Functions LOC----------")
print("No. of Independent Functions under each sub-module: ")
for keys, values in zip(submodules, independent_function_loc):
    print(dict(zip(keys, map(lambda x: x[0], values))))
print()
print("LOC of Independent Functions under each sub-module: ")
for keys, values in zip(submodules, independent_function_loc):
    print(dict(zip(keys, map(lambda x: x[1], values))))
print()

print("---------Classes LOC----------")
print("No. of Classes under each sub-module: ")
for keys, values in zip(submodules, class_loc):
    print(dict(zip(keys, map(lambda x: x[0], values))))
print()
print("LOC of Classes under each sub-module: ")
for keys, values in zip(submodules, class_loc):
    print(dict(zip(keys, map(lambda x: x[1], values))))
print()

print("---------Methods LOC----------")
print("No. of methods under each class:")
for key, values in zip(submodules, methods_loc):
    print(list(zip(key, map(lambda x: x[0], values))))
print()
print("LOC of methods under each class")
for key, values in zip(submodules, methods_loc):
    print(list(zip(key, map(lambda x: x[1], values))))
print()

print("---------LOC of other lines of code----------")
others_loc = 0
for loc in class_loc:
    others_loc += sum(map(lambda x: sum(x[1]), loc))
for loc in independent_function_loc:
    others_loc += sum(map(lambda x: sum(x[1]), loc))
print(total_loc-others_loc)
