from md_local2online.imgs_convert import run_conversion

import os
README_FILENAME = "readme.md"
README_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README_PATH = os.path.join(README_DIR, README_FILENAME)


if __name__ == '__main__':
    run_conversion(README_PATH, replace=False)
    print("ATTENTION! \n"
          "After the conversion, PLEASE use the converted .md file as your script and save as the raw .md file.")