import heartrate; heartrate.trace(browser=True)
import requests as re
import tkinter as tk
import time as t
from bs4 import BeautifulSoup as bs
import json
import os
import subprocess
import random
#from moviepy.editor import *



headers = {
	"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
	"Accept-Encoding" : "gzip, deflate, br",
	"Accept-Language" : "zh-CN,zh;q=0.9,en;q=0.8",
	"Cache-Control" : "max-age=0",
	"Connection" : "keep-alive",
	"Origin" : "https://www.bilibili.com",
	"Cookie" : "_uuid=1CB02DD5-AF1C-8423-ABF8-658233E3B70A99205infoc; LIVE_BUVID=AUTO9415454877048565; sid=6nce2kpi; CURRENT_FNVAL=16; im_notify_type_22740478=0; fts=1545916484; _ga=GA1.2.1445943855.1548946807; gr_user_id=d1ae60cf-0ad8-4667-b9af-eb5b4728c483; grwng_uid=59352159-974b-47c1-afe7-808ab863db12; stardustvideo=1; buvid3=D2620E5E-F3B8-4133-9816-A4FB41D9FD0F47173infoc; rpdid=|(u)YJR|mYYR0J'ullYJR)Yu|; UM_distinctid=16b84db1e5eb3-0c91e92b315d1d-3e385b04-15f900-16b84db1e60da; stardustpgcv=0606; finger=9dd9df7d; DedeUserID=22740478; DedeUserID__ckMd5=03cba76602fd78d4; SESSDATA=0b273fcf%2C1566381239%2Ce7bb9e71; bili_jct=ef9e882416bd6263ebc14ae6e5511a04; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1561560376,1563964362; _uuid=548F5891-F56F-E1D3-97CA-620AF7308C3905252infoc; balh_mode=replace; balh_server_inner=https//www.biliplus.com; balh_=oss; balh_upos_server=oss; im_seqno_22740478=116; im_local_unread_22740478=0; CURRENT_QUALITY=64; bp_t_offset_22740478=285663600616769137",
	"Host" : "www.bilibili.com",
	"Referer" : "https://space.bilibili.com/22740478/favlist?fid=217160278&ftype=create",
	"Upgrade-Insecure-Requests" : "1",
	"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
}


url = "https://www.bilibili.com/video/av"

clarity = {
	16 : '流畅360P',
	32 : '清晰480P',
	64 : '高清720P',
	80 : '超清1080P'
	}


def get_page(url,out,headers=headers):
	#发送请求
	rp = re.get(url, headers=headers)
	code = rp.status_code
	print("网页状态码: %s" % (code))
	out.insert('insert',"网页状态码: %s\n" % (code))
	return rp.text


def get_videos_info(webpage,out):
	#获取视频文件列表信息
	soup = bs(webpage, 'html.parser')
	soup_part = str(soup.head.find_all('script')[1])[28:-9]
	json_data = json.loads(soup_part)
	json_video = json_data['data']['dash']['video']
	json_audio = json_data['data']['dash']['audio']
	all_videos = []
	all_audio = []
	for video_url in json_video:
		videos = []
		videos_Clarity = {}
		videos.append(video_url['baseUrl'])
		videos_Clarity[clarity[video_url['id']]] = video_url['baseUrl']
		all_videos.append(videos_Clarity)
	for audio_url in json_audio:
		all_audio.append(audio_url['baseUrl'])
	video_audio = []
	video_audio.append(all_videos)
	video_audio.append(all_audio)
	print('视频列表已获取')
	out.insert('insert','视频列表已获取\n')

	return video_audio
	
def downloads_url_video(video_list,vc,ac,out):
	video_url_json = video_list[0]
	video_dist = {}
	#去除多余链接
	if len(video_url_json) > 4:
		for a in video_url_json:
			for aa in a:
				for b in video_url_json:
					for ba in b:
						if aa == ba:
							video_url_json.remove(b)
	#重新生成列表
	for i in video_url_json:
		for a in i:
			video_dist[a] = i[a]
	#清晰度选择
	flag = 1
	while flag:
		try:
			if vc == 3:
				video_url = video_dist['超清1080P']
				print('清晰度:1080P')
				out.insert('insert','清晰度:1080P\n')
			elif vc == 2:
				video_url = video_dist['高清720P']
				print('清晰度:720P')
				out.insert('insert','清晰度:720P\n')
			elif vc == 1:
				video_url = video_dist['清晰480P']
				print('清晰度:480P')
				out.insert('insert','清晰度:480P\n')
			elif vc == 0:
				video_url = video_dist['流畅360P']
				print('清晰度:360P')
				out.insert('insert','清晰度:360P\n')
		except :
			vc -= 1
			continue
		else:
			break

	audio_url_json = video_list[1]
	audio_url = audio_url_json[ac]
	all_video_audio = []
	all_video_audio.append(audio_url)
	all_video_audio.append(video_url)
	print('视频url已获取')
	out.insert('insert','视频url已获取\n')

	return all_video_audio

def downlaod_video(url_list,out,headers=headers):
	#下载视频到本地
	video_url = url_list[1]
	start_time = t.time()
	sp = re.get(video_url, headers=headers)
	out_time = t.time()-start_time
	file_name = 'bilibili_video.flv'
	with open(file_name, 'wb') as f:
		print('开始写入视频')
		out.insert('insert','开始写入视频\n')
		f.write(sp.content)
	size = os.stat(file_name).st_size/(1024*1024)
	speed = size/out_time
	print('视频写入完成-文件大小:%.2fMB-下载速度:%.2fMB/s' % (size, speed))
	out.insert('insert','视频写入完成-文件大小:%.2fMB-下载速度:%.2fMB/s\n' % (size, speed))
	return file_name



def download_audio(url_list,out,headers=headers):
	#下载音频到本地
	audio_url = url_list[0]
	start_time = t.time()
	sp = re.get(audio_url, headers=headers)
	out_time = t.time()-start_time
	file_name = 'bilibili_audio.mp3'
	with open(file_name, 'wb') as f:
		print('开始写入音频')
		out.insert('insert','开始写入音频\n')
		f.write(sp.content)
	size = os.stat(file_name).st_size/(1024*1024)
	speed = size/out_time
	print('音频写入完成-文件大小:%.2fMB-下载速度:%.2fMB/s\n' % (size, speed))
	out.insert('insert','音频写入完成-文件大小:%.2fMB-下载速度:%.2fMB/s\n' % (size, speed))
	return file_name

def make_video(audio_name,video_name,fps):
	audioclip = AudioFileClip(audio_name)
	videoclip = VideoFileClip(video_name)
	video = videoclip.set_audio(audioclip)
	video.write_videofile(str(fps)+'.mp4', fps=fps, codec='mpeg4')


def main_0(url,out):
	#主函数
	video_page = get_page(url,out=out)
	video_info = get_videos_info(video_page,out)
	video_list = downloads_url_video(video_info,vc=3,ac=0,out=out)
	video_name = downlaod_video(video_list,out=out)
	audio_name = download_audio(video_list,out=out)
	cmd = subprocess.Popen('ffmpeg_program.bat',shell=True,stdout=subprocess.PIPE)
	shell = cmd.stdout.read().decode('gbk')
	out.insert('insert',shell)
	#make_video(audio_name,video_name,fps=24)

def main_1(clarity,out,url,suffix='flv?'):
	#备用主函数
	video_page = get_page(url,out)
	soup = bs(video_page, 'html.parser')
	soup_part = str(soup.head.find_all('script')[1])[28:-9]
	json_data = json.loads(soup_part)
	video_url = json_data['data']['durl'][0]['url']
	clarity_num = choose_clarity(clarity,out)
	video_url = pick_url(video_url,clarity_num,suffix)
	start_time = t.time()
	while 1:
		sp = re.get(video_url,headers=headers)
		if sp.status_code != 200:
			print(sp.url)
			print('状态码:',sp.status_code)
			out.insert('insert',sp.url+'\n')
			out.insert('insert','状态码:'+str(sp.status_code)+'\n')
			clarity = choose_clarity(clarity-1,out)
			video_url = pick_url(video_url,clarity,suffix)
			continue
		else:
			break
	out_time = t.time()-start_time
	file_name = 'video.flv'
	with open(file_name, 'wb') as f:
		print('开始写入视频')
		out.insert('insert','开始写入视频\n')
		f.write(sp.content)
	out_time = t.time()-start_time
	size = os.stat(file_name).st_size/(1024*1024)
	speed = size/out_time
	print('视频写入完成-文件大小:%.2fMB-下载速度:%.2fMB/s' % (size, speed))
	out.insert('insert','视频写入完成-文件大小:%.2fMB-下载速度:%.2fMB/s\n' % (size, speed))

def pick_url(url,clarity,suffix):
	num = url.index(suffix)
	url = list(url)
	url[num-3] = str(clarity)[0]
	url[num-2] = str(clarity)[1]
	url = ''.join(url)
	return url

def choose_clarity(clarity,out):
	#清晰度选择
	while 1:
		if clarity == 3:
			clarity = 80
			print("清晰度:1080P")
			out.insert('insert',"清晰度:1080P\n")
			return clarity
		elif clarity == 2:
			clarity = 64
			print("清晰度:720P")
			out.insert('insert',"清晰度:720P\n")
			return clarity
		elif clarity == 1:
			clarity = 32
			print("清晰度:480P")
			out.insert('insert',"清晰度:480P\n")
			return clarity
		elif clarity == 0:
			clarity = 16
			print("清晰度:360P")
			out.insert('insert','清晰度:360P\n')
			return clarity
		else:
			clarity -= 1
			continue

def start_program(url,out):
	try:
		main_0(url,out)
	except Exception as e:
		print(e)
		try:
			print('发生错误,准备重试')
			out.insert('insert','发生错误,准备重试\n')
			main_1(3,out=out,url=url)
		except Exception as e:
			try:
				print(e)
				print('再次重试')
				out.insert('insert','再次重试\n')
				main_1(3,out=out,url=url,suffix='mp4?')
			except Exception as e:
				print(e)
				print('视频获取失败')
				out.insert('insert','视频获取失败\n')


win = tk.Tk()
win.title('bilibili视频下载器')
win.resizable(0,0)
win.geometry('700x500')
tk.Label(win,text='声明:无论以任何方式在任何时间任何地点下载任何东西都与本程序作者没有任何关系').place(relx=0.5,rely=0.98,anchor='center')
tk.Label(win,text='本程序效果极其随缘\n只能保证大部分视频的下载\n默认画质音频最高品质\n下载成品默认存储在本程序目录\n(你也改不了)\n第一次运行时会有卡顿(之后也有)\n请稍等3秒不要操作窗口').place(x=480,y=300)
tk.Label(win,text='请输入AV号(数字):').place(x=500,y=50)

entry_0 = tk.Entry(win,)
entry_0.place(x=500,y=70,width=143)
text_0 = tk.Text(win,)
#text_0.place(x=20,y=20,width=400,height=400)
def get_input(entry=entry_0,url=url,text_0=text_0):
	text = entry.get()
	url = url+text
	text_0.insert('insert',url+'\n')
	start_program(url,text_0)
	return text
def get_audio(entry=entry_0,url=url,out=text_0):
	text = entry.get()
	url = url+text
	print(url)
	video_page = get_page(url,out=out)
	video_info = get_videos_info(video_page,out)
	video_list = downloads_url_video(video_info,vc=3,ac=0,out=out)
	download_audio(video_list,out)


tk.Button(win,text='获取视频',height=4,width=19,command=get_input).place(x=500,y=110)
tk.Button(win,text='获取视频中的音频\n部分视频无法提取',height=4,width=19,command=get_audio).place(x=500,y=200)
text_0.place(x=20,y=20,width=400,height=400)
win.mainloop()
