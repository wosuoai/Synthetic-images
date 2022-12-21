import docx
import os


def replace_text(file_name, old_text, new_text):
    word_file=docx.Document(file_name)
    # 遍历每个段落
    for p in word_file.paragraphs:
        # 如果要搜索的内容在该段落
        if old_text in p.text:
            # 使用 runs 替换内容但不改变样式
            # 注意！runs 会根据样式分隔内容，确保被替换内容的样式一致
            for run in p.runs:
                if old_text in run.text:
                    run.text = run.text.replace(old_text, new_text)
    # 重新保存文件
    word_file.save(file_name)
    print("%s 替换成功"%file_name)


def main(file_dir,old_text,new_text):
    for root , dirs,files in os.walk(file_dir):
        for file in files:
            #print(file)
            replace_text(root+"/"+file,old_text,new_text)


if __name__ == "__main__":
    """main 第一个参数是word文档在的文件夹位置， 第二个参数是需要替换的单词，第三个参数是替换后的单词"""
    main("D:\存放文档文件夹","","")
    
