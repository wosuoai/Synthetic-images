import os
import shutil
import zipfile

# 路径
parent_path = r'G:\2222'

# 文件类型
file_flag = '.zip'

# 删除已解压的zip文件
def del_old_zip(file_path):
    os.remove(file_path)

# 解压
def decompress(file_path, root):

    # zipfile打开zip文件
    z = zipfile.ZipFile(f'{file_path}', 'r')

    # 解压
    z.extractall(path=f"{root}")  # path为解压路径，解包后位于该路径下

    # 判断是否需要重复解包
    for names in z.namelist():
        if names.endswith(file_flag):
            z.close()
            return 1

    z.close()
    return 0

"""
使用过程中发现有些zip解包后会混在一起
下面的两个函数解决这一问题
"""

# 先创建一个大文件夹与压缩包名字相同,避免后期混乱
def start_dir_make(root, dirname):
    os.chdir(root)
    os.mkdir(dirname)
    return os.path.join(root, dirname)

# 去除多余文件夹
def rem_dir_extra(root, father_dir_name):
    # 递归要注意信息的正常处理,搞不好上一个调用已经改变了东西,而下面的调用还是使用之前的数据

    try:

        # 判断文件夹是否重名
        for item in os.listdir(os.path.join(root, father_dir_name)):

            # 判断是不是一个文件夹，如果不是则跳过本次循环
            if not os.path.isdir(os.path.join(root, father_dir_name, item)):
                continue

            # 判断是否要脱掉一层目录结构
            # 文件夹名字要相同，且子目录中只有单独的一个文件夹
            if item == father_dir_name and len(
                    os.listdir(os.path.join(root, father_dir_name))) == 1:

                # 改变工作目录
                os.chdir(root)

                # 将无用文件夹重命名，因为直接移动会有重名错误
                os.rename(father_dir_name, father_dir_name + '-old')

                # 移动文件后删除空文件夹
                shutil.move(os.path.join(root, father_dir_name + '-old', item), os.path.join(root))
                os.rmdir(os.path.join(root, father_dir_name + '-old'))

                # 将去掉一层目录结构后的文件夹继续作为父本递归处理下去
                rem_dir_extra(root, item)

            else:

                # 处理不满足上述条件的文件夹
                rem_dir_extra(os.path.join(root, father_dir_name), item)

    except Exception as e:
        print("清除文件夹出错" + str(e))


if __name__ == '__main__':

    flag = 1
    while flag:

        for root, dirs, files in os.walk(parent_path):
            for name in files:
                if name.endswith(file_flag):
                    # 创建文件夹
                    new_ws = start_dir_make(root, name.replace(file_flag, ''))

                    # zip文件地址
                    zip_path = os.path.join(root, name)

                    # 解压
                    flag = decompress(zip_path, new_ws)

                    # 删除解压后的文件，不删除可能会重复运行
                    del_old_zip(zip_path)

                    # 去掉多余的文件结构
                    rem_dir_extra(root, name.replace(file_flag, ''))

                    print(f'{root}\{name}'.join(['文件：', 'n解压完成n']))

    # 由于解压可能执行了多次，可能会有已经解压好的父目录重名无法处理，这里要再处理一次
    rem_dir_extra(os.path.split(parent_path)[0], os.path.split(parent_path)[1])

    print("解压完成啦！！！！")

    
    
#将解压后的文件整合到一个文件夹下
for root, dirs, files in os.walk("G:\\2222"):
    for fileName in files:
        try:
            #shutil.move(root+'/'+fileName,"G:\\333")
            shutil.copy(root+'/'+fileName,"G:\\333")
        except Exception as error:
            print("{}移动失败".format(fileName))
print("-------------文件移动成功-------------")


for root, dirs, files in os.walk("G:\\333"):
    count=1
    for fileName in files:
        try:
            # # 获取图片前缀
            # fileNameInitial=fileName.split('.jpg')[0]
            shutil.copy(root+'/'+fileName,root+"/{}.jpg".format(count))
            #shutil.move(root+'/'+fileName,root+"/{}.jpg".format(count))
            count=count+1
        except Exception as error:
            print("{}重命名失败".format(fileName))
print("-------------文件夹里的图片重命名成功-------------")
