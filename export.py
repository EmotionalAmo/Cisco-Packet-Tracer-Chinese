from xml.etree import ElementTree as ET
from pygtrans import Translate


global temp


def trans(eng):
    return Translate().translate(eng, target='zh-CN').translatedText


tree = ET.parse("template.ts")

for children in tree.iter():
    if children.tag == 'source':
        if str(children.text).lower() == 'auto':
            temp = '自动'
        elif str(children.text).lower() == 'strings':
            temp = '字符串'
        elif str(children.text).lower() == 'min':
            temp = '最小'
        elif str(children.text).lower() == 'max':
            temp = '最大'
        elif str(children.text).lower() == 'mask':
            temp = '掩码'
        elif str(children.text).lower() == 'value':
            temp = '值'
        elif str(children.text).lower() == 'status':
            temp = '状态'
        else:
            temp = trans(str(children.text))
        print(str(children.text))
    if children.tag == 'translation':
        children.text = str(temp)  # type: ignore
        print(temp)

tree.write('chinese.8.2.2.0400.ts', encoding='UTF-8')
