
import os
import re
from urllib.parse import unquote, quote

from qiniu import Auth, put_file


"""
1. 打开.md文件（由于Github无法识别断开的链接，因此文件名不要断开的好）
2. 替换.md文件中所有的图片链接
    1. 匹配出.md文件中的路径，一般就是relative_source_dir_path + file_name
        1. 如果是本地的话，直接open打开即可（比如Typora）
        2. 如果是在线的话，需要用cookie访问，并保存到本地（比如为知）
        3. 由于七牛云的api基于本地文件路径，所以需要建立一个转换函数
    2. 将图片上传到七牛云，并返回七牛云反馈的图片网址
    3. 将返回的图片网址插入到原.md链接处
3. 保存成另一份.md文件
"""

def img_path_online2local(img_path: str) -> str:
    """
    图片的在线地址解析、下载到本地后，返回本地真实地址
    :param img_path:
    :return:
    """
    # 如果是为知笔记的话
    pass
    return img_path


def get_online_img_path(rel_img_href, abs_img_dir_path):
    abs_img_path = os.path.join(abs_img_dir_path, rel_img_href.split("/")[-1])
    print("Parsing: {}".format(abs_img_path))
    if not os.path.exists(abs_img_path):
        return print("Warning, No img found @ {}".format(abs_img_path))

    online_img_path = "/".join(abs_img_path.replace("\\", "/").rsplit("/", 2)[-2:])
    online_img_path = online_img_path.replace(" ", "")

    from settings import AK, SK, DOMAIN, BUCKET_NAME
    q = Auth(AK, SK)
    token = q.upload_token(BUCKET_NAME, online_img_path, 3600)
    try:
        ret, info = put_file(token, online_img_path, abs_img_path)
    except FileNotFoundError as e:
        print("No this local file: {}".format(abs_img_path))
        return abs_img_path
    else:
        online_img_path = DOMAIN + "/" + online_img_path
        print("Uploaded to: " + online_img_path)
        return online_img_path


def add_appendix(content: str):
    appendix = "\n### References\n"
    seq = 0
    for title, href in re.findall(r'[^!]\[(.*?)\]\((.*?)\)', content):
        seq += 1
        appendix += "<i>[{}] {}: {}</i>\n\n".format(seq, title, href)
    return content + appendix


def run_conversion(abs_md_path: str, replace: bool=False, reverse: bool=True):

    # Open File
    with open(abs_md_path, "r", encoding="utf-8") as f:
        print("Open md content from {}".format(abs_md_path))
        md_str = f.read()
        print("Converting img hrefs in the md file...")

    abs_img_dir_path = abs_md_path.replace(".md", ".assets")
    img_dir_to_match = quote(abs_img_dir_path.rsplit("\\", 1)[-1]).replace("%B2", "+")
    img_href_to_match = r'(?<=\()%s/.*?(?=\))' % img_dir_to_match
    print("img_href_to_match: " + img_href_to_match)

    md_str_converted = re.sub(img_href_to_match,
                              lambda x: get_online_img_path(x.group(0), abs_img_dir_path), md_str)

    md_str_converted = add_appendix(md_str_converted)

    if replace:
        md_file_path_new = abs_md_path
    else:
        from datetime import datetime
        md_file_path_new = abs_md_path.replace(".md", "_{}.md".format(int(datetime.now().timestamp())))

    if not reverse:
        with open(md_file_path_new, 'w', encoding="utf-8") as f:
            f.write(md_str_converted)
            print("Saved new md file to {}".format(md_file_path_new))
    else:
        os.rename(abs_md_path, md_file_path_new)
        with open(abs_md_path, "w", encoding="utf-8") as f:
            f.write(md_str_converted)
            print("Saved new md file to {}, and the old one has moved to {}".format(abs_md_path, md_file_path_new))

