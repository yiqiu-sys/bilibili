from bilibili_api import video, sync
import jieba
from wordcloud import WordCloud
#from xml.dom.minidom import parse

"""
Args:
    text      (str)               : 弹幕文本。
    dm_time   (float, optional)   : 弹幕在视频中的位置，单位为秒。Defaults to 0.0.
    send_time (float, optional)   : 弹幕发送的时间。Defaults to time.time().
    crc32_id  (str, optional)     : 弹幕发送者 UID 经 CRC32 算法取摘要后的值。Defaults to None.
    color     (str, optional)     : 弹幕十六进制颜色。Defaults to "ffffff".
    weight    (int, optional)     : 弹幕在弹幕列表显示的权重。Defaults to -1.
    id_       (int, optional)     : 弹幕 ID。Defaults to -1.
    id_str    (str, optional)     : 弹幕字符串 ID。Defaults to "".
    action    (str, optional)     : 暂不清楚。Defaults to "".
    mode      (Mode, optional)    : 弹幕模式。Defaults to Mode.FLY.
    font_size (FontSize, optional): 弹幕字体大小。Defaults to FontSize.NORMAL.
    is_sub    (bool, optional)    : 是否为字幕弹幕。Defaults to False.
    pool      (int, optional)     : 暂不清楚。Defaults to -1.
    attr      (int, optional)     : 暂不清楚。 Defaults to -1.
"""

bv = input('请输入bvid\n')

v = video.Video(bvid=bv)
dms = sync(v.get_danmakus(0))

strs = ''
for dm in dms:
    strs = strs + dm.text
strs = strs.replace('\n','').replace('\r','').replace(' ','')

texts = jieba.lcut(strs)
texts = ' '.join(texts)

wc = WordCloud(font_path=r'C:\Users\DELL\AppData\Local\Microsoft\Windows\Fonts\FZXBSK.ttf',width=1920,height=1080,mode='RGBA',background_color=None,max_words=100).generate(texts)
wc.to_file(r'try.png')

'''
DOMTree=parse(r'《灯火里的中国》.cmt.xml')
bcs=DOMTree.documentElement

dms=bcs.getElementsByTagName('d')
print(len(dms))

strs = ''
for dm in dms:
    strs = strs + str(dm.childNodes[0].data)
strs = strs.replace('\n','').replace('\r','').replace(' ','')
'''
