
# with open('test.txt', 'r') as f:
#     for line in f.readlines():
#         dict_ = eval(line)
#         print(dict_['def'])

def judge_arg(parameter):
    try:
        x = int(parameter)
        return isinstance(x, int)
    except ValueError:
        return False

if __name__ == '__main__':
    print(judge_arg('-123a'))