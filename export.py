from xml.etree import ElementTree as ET
from pygtrans import Translate

global temp


def trans(eng):
    return Translate().translate(eng, target='zh-CN').translatedText


tree = ET.parse("template.ts")

for children in tree.iter():
    if children.tag == 'source':
        temp = trans(str(children.text))
    if children.tag == 'translation':
        children.text = str(temp)  # type: ignore

tree.write('chinese.1.8.1.ts', encoding='UTF-8')
