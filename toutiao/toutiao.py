#coding=utf-8
import requests
from bs4 import BeautifulSoup
import json
import datetime
import re
import sys
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def tt_info(email,password):
	print >>sys.stderr, email, password
	info = {}
	payload = {'name_or_email': email, 'password': password}
	s = requests.Session()
	s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
	r = s.post("http://mp.toutiao.com/auth/login_post/", data=payload)
	login = json.loads(r.text)
	if login['message'] == 'success':
		m = s.get('https://mp.toutiao.com/',verify=False)
		soup = BeautifulSoup(m.text,'lxml')
		index_sum = soup.find('div',class_="indexsum_btns")
		index_a_list = index_sum.find_all('a')
		info['login'] = email
		info[u'主页'] = {}
		for a in index_a_list:
			info[u'主页'][a.span.text] = int(a.b.text.strip().replace(',',''))

		info[u'手动更新'] = []
		r = s.get('https://mp.toutiao.com/api/media_article_list/?count=10&source_type=0&status=all&from_time=0&item_id=0&flag=2')
		while True:
			res = json.loads(r.text)
			for article in res['data']['articles']:
				item = {}
				item[u'标题'] = article['title']
				item[u'发表时间'] = datetime.datetime.fromtimestamp(article['create_time']).isoformat()
				item[u'标签'] = article['tag_name']
				item[u'状态'] = article['status_desc']
				if article['status_desc'] == u'已发表':
					item[u'转发'] = article['share_count']
					item[u'评论'] = article['comment_count']
					item[u'收藏'] = article['favorite_count']
					item[u'阅读'] = article['go_detail_count']
					item[u'推荐'] = article['impression_count']
					item[u'已推荐'] = article['was_recommended']
				info[u'手动更新'].append(item)
			if not res['data']['time_pagination']['has_next']:
				break
			else:
				last_time = res['data']['last_time']
				url = 'https://mp.toutiao.com/api/media_article_list/?count=10&source_type=0&status=all&from_time=%d&item_id=0&flag=1' %(last_time)
				r = s.get(url)

		info[u'评论管理'] = []
		r = s.get('https://mp.toutiao.com/comment/')
		if re.findall('data\'\s:\s([^data\'].*\])',r.text):
			data = json.loads(re.findall('data\'\s:\s([^data\'].*\])',r.text)[0])
			for comment in data:
				item = {}
				item[u'内容'] = comment['content']
				item[u'文章'] = comment['group']['title']
				item[u'点赞'] = comment['digg_count']
				item[u'评论数'] = comment['comment_count']
				item[u'评论人'] = comment['user']['screen_name']
				info[u'评论管理'].append(item)

		info[u'文章分析'] = {}
		info[u'文章分析'][u'概况'] = {}
		today = datetime.datetime.now().date().isoformat()
		info[u'文章分析'][u'概况'][u'时间'] = today
		url = 'https://mp.toutiao.com/statistic/content_overview/?start_date=%s&end_date=%s' %(today,today)
		r = s.get(url,verify=False)
		data = json.loads(r.text)['data']
		info[u'文章分析'][u'概况'][u'推荐量'] = data['impression_count']
		info[u'文章分析'][u'概况'][u'阅读量'] = data['go_detail_count']
		info[u'文章分析'][u'概况'][u'评论量'] = data['comment_count']
		info[u'文章分析'][u'概况'][u'转发量'] = data['share_count']
		info[u'文章分析'][u'概况'][u'收藏量'] = data['repin_count']

		info[u'文章分析'][u'详情'] = {}
		info[u'文章分析'][u'详情'][u'按文章'] = []
		weekbefore = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
		monthbefore = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
		info[u'文章分析'][u'详情'][u'开始时间'] = monthbefore
		info[u'文章分析'][u'详情'][u'结束时间'] = today
		pagenum = 1
		while True:
			url = 'https://mp.toutiao.com/statistic/content_article_stat/?start_date=%s&end_date=%s&pagenum=%d' %(monthbefore,today,pagenum)
			r = s.get(url)
			total_pagenum = json.loads(r.text)['data']['total_pagenum']
			data = json.loads(r.text)['data']['data_list']
			for detail in data:
				item = {}
				item[u'标题'] = detail['title']
				item[u'推荐量'] = detail['impression_count']
				item[u'阅读量'] = detail['go_detail_count']
				item[u'评论量'] = detail['comment_count']
				item[u'收藏量'] = detail['repin_count']
				item[u'转发量'] = detail['share_count']
				item[u'article_id'] = detail['article_id']
				item[u'文章分析'] = {}
				url = 'https://mp.toutiao.com/statistic/item_related_stat/'+detail['article_id']+'/?'
				r = s.get(url)
				result = json.loads(r.text)['data']
				item[u'文章分析'][u'平均阅读进度'] = result['item_read_or_play_avg_progress_pct']
				item[u'文章分析'][u'跳出率'] = result['item_read_or_play_avg_bounce_pct']
				item[u'文章分析'][u'平均阅读速度'] = result['item_read_avg_speed']
				info[u'文章分析'][u'详情'][u'按文章'].append(item)
			pagenum += 1
			if pagenum > total_pagenum:
				break

		info[u'文章分析'][u'详情'][u'按时间'] = []
		url = 'https://mp.toutiao.com/statistic/content_daily_stat/?start_date=%s&end_date=%s&pagenum=1' %(weekbefore,today)
		r = s.get(url)
		data_list = json.loads(r.text)['data']['data_list']
		for data in data_list:
			item = {}
			item[u'时间'] = data['date']
			item[u'推荐量'] = data['impression_count'] 
			item[u'阅读量'] = data['go_detail_count'] 
			item[u'播放量'] = data['play_effective_count'] 
			item[u'评论量'] = data['comment_count'] 
			item[u'收藏量'] = data['repin_count'] 
			item[u'转发量'] = data['share_count']
			info[u'文章分析'][u'详情'][u'按时间'].append(item) 
			
		
		info[u'头条号指数'] = {}
		r = s.get('https://mp.toutiao.com/statistic/recommend_factor_overview/?')
		data = json.loads(r.text)['data']
		info[u'头条号指数'][u'实际提升推荐量'] = data['improvement_impression_count']
		info[u'头条号指数'][u'提升百分比'] = data['improvement_percent']

		url = 'https://mp.toutiao.com/statistic/recommend_factor/?start_date=%s&end_date=%s&radar_date=%s' %(weekbefore,today,today)
		r = s.get(url)
		data = json.loads(r.text)['data']
		info[u'头条号指数'][u'数据详情'] = data

		info[u'订阅用户'] = []
		r = s.get('https://mp.toutiao.com/statistic/subscriber_list/0?pagesize=28&pagenum=1')
		data = json.loads(r.text)['data']['subscirber_info']
		for rss_user in data:
			info[u'订阅用户'].append({u'用户名':rss_user['screen_name']})

		info[u'收益概览'] = {}
		r = s.get('https://mp.toutiao.com/media_income/data/toutiao_ad/abstract/?')
		data = json.loads(r.text)['data']['ad']
		info[u'收益概览'][u'开始时间'] = weekbefore
		info[u'收益概览'][u'结束时间'] = today
		info[u'收益概览'][u'收入'] = {}
		info[u'收益概览'][u'收入'][u'昨天收入'] = data['lastday']
		info[u'收益概览'][u'收入'][u'本月收入'] = data['month']
		info[u'收益概览'][u'日报表'] = []
		url = 'https://mp.toutiao.com/media_income/data/toutiao_ad/detail/?start_date=%s&end_date=%s&pagenum=1' %(weekbefore,today)
		r = s.get(url)
		data = json.loads(r.text)['data']['detail']
		for detail in data:
			item = {}
			item[u'日期'] = detail['day']
			item[u'总计金额'] = detail['total']
			item[u'头条广告'] = detail['toutiao_ad']
			item[u'广告展示量'] = detail['impr']
			item[u'视频收益'] = detail['praise_income']
			item[u'视频播放量'] = detail['praise_times']
			info[u'收益概览'][u'日报表'].append(item)

		info[u'账号信息'] = {}
		r = s.get('https://mp.toutiao.com/edit_media_account/')
		info[u'账号信息'][u'头条号名称'] = json.loads(re.findall('name:([^n].*),',r.text)[0])
		info[u'账号信息'][u'头条号介绍'] = json.loads(re.findall('desc:([^d].*),',r.text)[0])
		info[u'账号信息'][u'头条号头像'] = json.loads(re.findall('avatar_url:([^a].*),',r.text)[0])
		info[u'账号信息'][u'邮箱'] = json.loads(re.findall('email:([^e].*),',r.text)[0])
		info[u'账号信息'][u'作者二维码'] = re.findall('qrcode:([^q].*),',r.text)[0].replace('\'','').replace('+','')
		info[u'账号信息'][u'联系人'] = json.loads(re.findall('dot_name:([^d].*),',r.text)[0])
		info[u'账号信息'][u'联系电话'] = json.loads(re.findall('mobile:([^m].*),',r.text)[0])
		info[u'账号信息'][u'所在地'] = json.loads(re.findall('ext\.location_name=([^ext].*?);',r.text)[0].replace(' ',''))
		# print(json.dumps(info[u'账号信息'],indent=2,ensure_ascii=False).encode('utf-8'))

		info[u'账号状态'] = {}
		r = s.get('https://mp.toutiao.com/account_info/')
		soup = BeautifulSoup(r.text,'lxml')
		table = soup.find('table',class_='account-status-tbl')
		td_list = []
		for string in table.stripped_strings:
			td_list.append(string)
		info[u'账号状态'][u'账号状态'] = td_list[4]
		info[u'账号状态'][u'账号分值'] = td_list[8]
		info[u'账号状态'][u'发文篇数'] = td_list[12]
		print(json.dumps(info,ensure_ascii=False).encode('utf-8'))
	else:
		print(json.dumps(login,ensure_ascii=False).encode('utf-8'))
	return s

def command(s,c):
	r = s.get('http://mp.toutiao.com/api/media_article_list/?count=10&source_type=0&status=draft&from_time=0&item_id=0&flag=2')
	articles_data = json.loads(r.text)
	pgc_id = articles_data['data']['articles'][0]['pgc_id']
	title = articles_data['data']['articles'][0]['title']
	tag = articles_data['data']['articles'][0]['tag']
	url = 'http://mp.toutiao.com/edit_article/?pgc_id=%s' %(pgc_id)
	r = s.get(url)

	lines = re.findall('.*\n',r.text)
	for line in lines:
	    if re.findall('content:',line):
	        content = json.loads("\"" + re.findall('<p>.*<\\\\/p>',line)[0]+ "\"")
	payload = {
			'title': title,
			'abstract': '',
			'content':content, 
			'authors':'', 'tag':tag, 
			'self_appoint' :0,
			'save':1,
			'pgc_id':pgc_id,
			'show_ads':1,
			'video_vid':0,
			'video_vu':'',
			'video_vname':'',
			'video_vposter':'',
			'vids_to_del':[],
			'force_ads':2,
			'after_pass_modify':0,
			'urgent_push':0,
			'subsidy':0,
			'pgc_feed_covers':[],
			'slave_title':'',
			'is_abtest':0,
			'slave_item_id':0
		     }  

	r = s.post("http://mp.toutiao.com/edit_article_post/", data=payload)
	post_res = json.loads(r.text)
	print json.dumps(post_res,ensure_ascii=False)

if __name__ == "__main__":
	email = sys.argv[1]
	password = sys.argv[2]
	s = tt_info(email,password)
	while True:
		c = (sys.stdin.readline()).replace('\n','')
		if c == 'Q':
			break
		else:
			command(s,c)

