from bilibili_api import video, sync
import os

'''
需要的库：bilibili_api  you-get   均可通过pip3指令安装
同时需要在环境变量链接ffmpeg(单独的exe怎么用命令行调用我不到啊)
'''


'''
暂不支持分p视频，未来加入
分辨率默认1920*1080
'''

def out_mkv(bilivideo,location):
    info = sync(bilivideo.get_info())
    name = info['title']
    order = 'ffmpeg' + ' -i ' + location + 'outpu.mp4' + ' -i ' + location + 'output.ass' + ' -c copy ' + location + 'out' + '.mkv'
    message = os.system(order)
    os.remove(location + 'outpu.mp4')
    os.remove(location + 'output.ass')
    os.remove(location + info['title'] + '.cmt.xml')
    os.rename(location + 'out' + '.mkv',location + info['title'] + '.mkv')
    if (message == 0):
        return 0
    else:
        return 1
	  


def video_download(bv,location):
    order = 'https://www.bilibili.com/video/' + bv
    message = os.system('you-get -o ' + location[:-1] + ' -O ' + 'outpu '+ order)
    if (message == 0):
        return 0
    else:
        return 1

def danmaku_to_ass(bilivideo,location):
		
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

    dms = sync(bilivideo.get_danmakus(page_index = 0))

    #字幕列表结构：[开始时间，结束时间，发射结束时间，弹幕文本，弹幕轨道，弹幕颜色，弹幕模式]
    danmus = []
    for dm in dms:
        danmus.append([dm.dm_time,0,0,dm.text,0,dm.color,int(dm.mode)])

    for danmu in danmus:
        if(danmu[6] != 4 and danmu[6] != 5):
            danmu[6] = 1

    danmus.sort(key = lambda sor:sor[0])
    for danmu in danmus:
        if(danmu[6] == 4 or danmu[6] == 5):
            danmu[1] = round(danmu[0] + 5,3)
            danmu[2] = round(danmu[0] + 0.2*len(danmu[3]),3)
        else:
            danmu[1] = round(danmu[0] + 0.2*len(danmu[3]) + 6.75,3)
            danmu[2] = round(danmu[0] + 0.2*len(danmu[3]),3)
        #print(danmu)

    dams = danmus
    i = 0
    for danmu in danmus:
        j = 0
        tracks0 = [] #冲突滚动弹幕库
        tracks1 = [] #冲突底端弹幕库
        tracks2 = [] #冲突顶端弹幕库
        if(danmu[6] == 4):
            track = 17
        else:
            track = 0
        z = 0
        for dam in dams:
            if(danmu[0] >= dam[0] and danmu[0] <= dam[1] and i != 0 and danmu[6] == 4 and dam[6] == 4 ):
                tracks1.append(dam[4])
            if(danmu[0] >= dam[0] and danmu[0] <= dam[1] and i != 0 and danmu[6] == 5 and dam[6] == 5 ):
                tracks2.append(dam[4])
            if(danmu[0] >= dam[0] and danmu[0] <= dam[2] and i != 0 and danmu[6] == 1 and dam[6] == 1 ):
                tracks0.append(dam[4])
            if(i == 0 or j == i - 1):
                break
            else:
                j = j + 1
        for y in range(0,18):
            if(y not in tracks0 and danmu[6] == 1):
                track = y
                z = 1
                break
        for y in range(0,18):
            if((17-y) not in tracks1 and danmu[6] == 4):
                track = 17-y
                z = 1
                break
        for y in range(0,18):
            if(y not in tracks2 and danmu[6] == 5):
                track = y
                z = 1
                break
        if(z == 0 and i != 0):
            overlaps0 = [] #满冲突滚动弹幕计数库
            overlaps1 = [] #满冲突底端弹幕计数库
            overlaps2 = [] #满冲突顶端弹幕计数库
            if (danmu[6] == 1):
                for y in range(0,18):
                    overlaps0.append([y,tracks0.count(y)])
                overlaps0.sort(key = lambda sro:sro[1])
                overlap0 = overlaps0[0]
                track = overlap0[0]
            if (danmu[6] == 4):
                for y in range(0,18):
                    overlaps1.append([17-y,tracks1.count(17-y)])
                overlaps1.sort(key = lambda sro:sro[1])
                overlap1 = overlaps1[0]
                track = overlap1[0]
            if (danmu[6] == 5):
                for y in range(0,18):
                    overlaps2.append([y,tracks2.count(y)])
                overlaps2.sort(key = lambda sro:sro[1])
                overlap2 = overlaps2[0]
                track = overlap2[0]
        danmu[4] = track
        i = i + 1

    #文件头构建
    ass = '[Script Info]\n'+'Title: QiuYi_help\n'+'ScriptType: v4.00+\n'+'WrapStyle: 0\n'+'ScaledBorderAndShadow: yes\n'+'PlayResX: 1920\n'+'PlayResY: 1080\n'
    ass = ass + '\n'

    #字体配置构建
    ass = ass + '[V4+ Styles]\n'+'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n'
    ass = ass + 'Style: Default,黑体,50,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,2,0,5,0,0,0,1\n'
    ass = ass + '\n'

    #字幕正文构建
    ass = ass + '[Events]\n'+'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
    for danmu in danmus:
        #print(danmu)
        ass = ass + 'Dialogue: 0,'+str(int(int(danmu[0])/3600))+':'+str(int(int(danmu[0])/60)-60*int(int(danmu[0])/3600))+':'+ str(int(danmu[0])%60)+'.'+str(int((danmu[0]-int(danmu[0]))*100))+','
        ass = ass + str(int(int(danmu[1])/3600))+':'+str(int(int(danmu[1])/60)-60*int(int(danmu[1])/3600))+':'+ str(int(danmu[1])%60)+'.'+str(int((danmu[1]-int(danmu[1]))*100))+','
        if (danmu[6] == 1):
            ass = ass + 'Default,,0,0,0,Banner;3;[0;[0]],{\pos(960,'+str(int(30+60*danmu[4]))+')'
        else:
            ass = ass + 'Default,,0,0,0,,{\pos(960,'+str(int(30+60*danmu[4]))+')'
        color = danmu[5]
        color = color[4:] + color[2:4] + color[:2]
        ass = ass + '\c&H' + color + '}'
        ass = ass + danmu[3]
        ass = ass + '\n'
    
    
    with open(location + 'output.ass','w',encoding = "utf-8") as f:
        f.write(ass)
	    
	    
bv = input('请输入bvid\n')
location = input('请输入目标文件夹绝对路径\n')
location = location + '\\'

#print(location)

v = video.Video(bvid=bv)

video_download(bv = bv, location = location)
danmaku_to_ass(bilivideo = v,location = location)
out_mkv(bilivideo = v,location = location)

    


    
    
