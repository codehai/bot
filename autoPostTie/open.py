#ecoding=utf-8
import os
import json
import random
import sys
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from urllib import quote
import tuling
import time
from PIL import Image
import base64 
import cStringIO
import requests
import postgres
import base64
import tempfile

#reload(sys)
#sys.setdefaultencoding("utf-8")
print os.environ['PATH']
print sys.getdefaultencoding()
def rndString():
	a='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
	b=list(a)
	return "".join(random.sample(b,5))
def rndColor():
	return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
def rndRotate():
	return random.randint(-30,30)
def generateImg(imgDir,pid): 
	# imgDir = sys.argv[1] #图片路径
	# imgDir = '/home/hao/bot/shuiyin/0b7b02087bf40ad13ef034aa552c11dfa9ecce67.jpg'
	comand = 'python shuiyin.py'
	fontsize = random.uniform(0.064,0.11)
	color = rndColor() 
	rotate = rndRotate() 
	offsetX = random.uniform(-0.7,0.7) 
	offsetY = random.uniform(-0.7,0.7)
	os.system("%s %s %s %s %s %s %s %s %s %s" %(comand,fontsize,rotate,offsetX,offsetY,color[0],color[1],color[2],imgDir,pid))
	return {'fontsize':fontsize,'rotate':rotate,'offsetX':offsetX,'offsetY':offsetY,'R':color[0],'G':color[1],'B':color[2]}
def doesWebElementExist(driver,selector,element):
	try:
		driver.find_element(selector,element)
		return True
	except:
		return False
def sendCodeImg(region):
	time.sleep(1)
	imgstring = driver.get_screenshot_as_base64()
	imgdata = base64.b64decode(imgstring)
	file_like = cStringIO.StringIO(imgdata)
	img = Image.open(file_like)
	cropImg = img.crop(region)
	buffer = cStringIO.StringIO()
	cropImg.save(buffer,format="JPEG")
	img_str = base64.b64encode(buffer.getvalue())
	if region[3] == 40:
		r = requests.post("http://reniku.cn/ef22ed0d31cf2eccdfe4f2cd0ef8198b/tiebaC4", data=img_str)
	else:
		r = requests.post("http://reniku.cn/ef22ed0d31cf2eccdfe4f2cd0ef8198b/tieba33", data=img_str)
	r.encoding = 'utf-8'
	print  r.encoding
	print json.dumps(r.json(),ensure_ascii=False,indent=2).encode('utf-8')
	return r.json()["Result"]
def fillType1Code(): 
	print("有验证码type1!!!!!!!!!!!!!!!!!!!")
	driver.execute_script('$(".captcha_img").css({"position":"fixed","margin-top":"0","margin-left":"0","left":"0","top":"0","z-index":"99998"});' )
	region = (0,0,180,40)
	resultCode = sendCodeImg(region)
	print  resultCode
	driver.find_element_by_css_selector(".pb_poster_layer .old_vcode_wrapper .captcha_input").send_keys(resultCode)
	driver.execute_script("document.querySelector('div.pb_poster_layer div.blue_kit_right a.j_submit_btn').click()")
def fillType2Code():
	print("有验证码type2!!!!!!!!!!!!!!!!!!!")
	region = (0,0,145,180)
	driver.execute_script('$(".pb_poster_layer .vcode_panel_input_tip").before("<div></div>");'\
		'$(".pb_poster_layer .vcode_panel_input_tip").prev().addClass("bj");'\
		'$(".bj").css({"position":"fixed","margin-top":"0","margin-left":"0","left":"0","top":"0","height":"180px","width":"145px","background-color":"white","z-index":"99998"});'\
		'$(".pb_poster_layer .j_vcode_target_img").css({"position":"fixed","margin-top":"0","margin-left":"0","left":"0","top":"0","z-index":"99999"});'\
		'var x=0;'\
		'console.log(x);'\
		'var y=1;'\
		'var grids = $(".pb_poster_layer .grid_img");'\
		'for(var i=0;i<grids.length;i++) {'\
		        '$(grids[i]).css("position","fixed");'\
		        '$(grids[i]).css("top",y*50+"px");'\
		        '$(grids[i]).css("left",x*50+"px");'\
		        '$(grids[i]).css("z-index","99999");'\
		        'x++;'\
		        'if(x>2){'\
		                'x=0;'\
		                'y++;'\
		        '}'\
		'}'\
	 )
	resultCode = sendCodeImg(region)
	print  resultCode
	gridsButton = driver.find_elements_by_css_selector('.pb_poster_layer .grid_button')
	for code in resultCode.encode("utf-8"):
		TouchActions(driver).tap(gridsButton[int(code)-1]).perform()
def testStatus(vcodeType):
	for count in range(1,3):
		if vcodeType==1:
			fillType1Code()
		elif vcodeType==2:
			fillType2Code()
		time.sleep(4)
		status =  driver.execute_script('return $(".toast").text()')
		#status = driver.find_element_by_class_name("toast").text	
		print status
		if status=='none':
			print 'status none'
			ActionChains(driver).click(driver.find_element_by_css_selector(".blue_kit_left a.blue_kit_btn_back")).perform()
			wait.until(EC.presence_of_element_located((By.LINK_TEXT,'主题贴')))
			printPageAttr()
			break
		else:
			if  status.encode("utf-8")=='未知错误':
				print '404 err'
				# wait.until(EC.presence_of_element_located((By.LINK_TEXT,'主题贴')))
				ActionChains(driver).click(driver.find_element_by_css_selector(".blue_kit_left a.blue_kit_btn_back")).perform()
				wait.until(EC.presence_of_element_located((By.LINK_TEXT,'主题贴')))
				printPageAttr()
				break
			elif status.encode("utf-8")=='验证码输入错误,请重新输入':
				print str(count)+':vcode err type'+str(vcodeType)
				# ActionChains(driver).click(driver.find_element_by_css_selector(".blue_kit_left a.blue_kit_btn_back")).perform()
				# wait.until(EC.presence_of_element_located((By.LINK_TEXT,'主题贴')))
			elif status.encode("utf-8")=='回贴成功！':
				print 'send ok!'
				break
			elif status.encode("utf-8")=='发贴含有不适当内容或广告,请重新提交':
				ActionChains(driver).click(driver.find_element_by_css_selector(".blue_kit_left a.blue_kit_btn_back")).perform()
				wait.until(EC.presence_of_element_located((By.LINK_TEXT,'主题贴')))
				printPageAttr()
				break
			else:
				ActionChains(driver).click(driver.find_element_by_css_selector(".blue_kit_left a.blue_kit_btn_back")).perform()
				wait.until(EC.presence_of_element_located((By.LINK_TEXT,'主题贴')))
				printPageAttr()	
				break
def floorContent():
	try:
		wait.until(EC.presence_of_element_located((By.CLASS_NAME,'post_title_embed')))
		printPageAttr()
	except Exception, e:
		return False
	title = driver.find_element_by_class_name('post_title_embed').text
	postList = driver.find_element_by_id('pblist').find_elements_by_class_name('post_list_item')
	tiezi=[]
	tiezi.append(title)
	for p in postList:
		postContent = p.find_element_by_class_name('content').text
		if(len(postContent)):
			# reply = tuling.chat(postContent)
			# print(reply)                         
			#print('postContent:'+postContent)
			tiezi.append(postContent)
	return tiezi
def printPageAttr():
	Attr = {}
	Attr['page_source'] = driver.page_source
	Attr['current_url'] = driver.current_url
	Attr['current_window_handle'] = driver.current_window_handle
	Attr['desired_capabilities'] = driver.desired_capabilities
	# Attr['file_detector'] = driver.file_detector
	Attr['log_types'] = driver.log_types
	Attr['name'] = driver.name
	Attr['title'] = driver.title
	Attr['window_handles'] = driver.window_handles
	print json.dumps(Attr,ensure_ascii=False,indent=2)
# chromedriver = "./chromedriver"
# os.environ["webdriver.chrome.driver"] = chromedriver
options = Options()
userAgent = "--user-agent='"+sys.argv[3]+"'"
# print userAgent
options.add_argument(userAgent)
options.add_argument("--no-sandbox")
options.add_argument("--disable-setuid-sandbox")
print "CP 54321"
driver = webdriver.Chrome("chromedriver",chrome_options=options)

# profile = webdriver.FirefoxProfile()
# profile.set_preference("general.useragent.override", "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1")
# driver = webdriver.Firefox(profile)

print "CP 11111"
wait = WebDriverWait(driver, 10)
print sys.argv[1]
cookieString = sys.argv[2]
#cookieString = postgres.findCookie('4')[0][3]
print cookieString
print "CP 22222"
cookies = json.loads(cookieString)
try:
	# with open('2.cookie.json','r') as data:
	#     cookieString = data.read();
	print "CP 37145"
	driver.get('http://tieba.baidu.com/tb/error.html')
	if(re.findall(u'无法访问',driver.title)):
		print '无法访问'
		printPageAttr()
		raise Exception
	print "CP 37146"
	driver.delete_all_cookies()
	for cookie in cookies:
		name = cookie['name']
		value = cookie['value']
		driver.add_cookie({'name':name, 'value':value})
	#driver.refresh()
	print "CP 34863"
	print sys.argv[1]
	missionUrl = re.findall('http://\d+.\d+.\d+.\d+:\d+',sys.argv[1])
	if(missionUrl):
		if(re.findall('http://\d+.\d+.\d+.\d+:\d+/',sys.argv[1])):
			driver.get(sys.argv[1])
		else:
			print '没有查找到/'
			printPageAttr()
			raise Exception
			
	else:
		driver.get(sys.argv[1])
	print "CP 34864"
	print driver.current_url
	assert(driver.current_url == sys.argv[1]);
	#print driver.page_source
	missionString = driver.find_element_by_tag_name("pre").text
	missions = json.loads(missionString)
	driver.get('http://tieba.baidu.com')
	# time.sleep(5)
	# cookie= driver.get_cookies()
	# print json.dumps(cookie)
	driver.find_element_by_link_text("我").click()
	try:
		wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'user_info_name')))
		user = driver.find_element_by_class_name('user_info_name').text
		printPageAttr()	
	except Exception, e:
		print "没有查询到用户"
		user = 'null'
		printPageAttr()
		# raise Exception
		pass
	print 'user:'+user.encode("utf-8")
	try:
		element = driver.find_element_by_link_text("进吧")
	except Exception, e:
		print "未登录成功，没有查询到用户"
		raise Exception
	driver.find_element_by_link_text("进吧").click()
	driver.execute_script("document.querySelector('div[lgoinprompt]').remove()")
	for mission in missions:
		ba = mission['ba']
		# ba = u'女优'
		hui = mission['hui']
		lou_min = hui['lou-min']
		lou_max = hui['lou-max']
		posts = hui['posts']
		for post in posts:
			content = post[0]
			if(len(post)>1 and post[1][0]=='i'):
				srcImg = post[1][1]
				# pid = base64.b16encode(rndString()+'_'+str(os.getpid()))
				temp = tempfile.NamedTemporaryFile(suffix='.jpg',dir='/dev/shm')
				randomImg = generateImg(srcImg,temp.name)
				# imgPath = '/dev/shm/'+pid+'.jpg'  
				imgPath = temp.name
			else:
				srcImg = ""
				imgPath = ""
				randomImg = ""
			if doesWebElementExist(driver,By.CSS_SELECTOR,'a.top_search'):
				topSearch = driver.find_element_by_css_selector('a.top_search')
				ActionChains(driver).click(topSearch).perform()
			elif doesWebElementExist(driver,By.LINK_TEXT,'搜索'):
				search_btn = driver.find_element_by_link_text('搜索')
				ActionChains(driver).move_to_element(search_btn).click().perform()
			elif doesWebElementExist(driver,By.CSS_SELECTOR,'a.blue_kit_icon_search'):
				icon_search = driver.find_element_by_css_selector('a.blue_kit_icon_search')
				ActionChains(driver).click(icon_search).perform()
			wait.until(EC.presence_of_element_located((By.TAG_NAME,'input')))
			printPageAttr()
			driver.find_element_by_tag_name('input').send_keys(ba)
			wait.until(EC.element_to_be_clickable((By.ID,'btn')))
			printPageAttr()
			ActionChains(driver).click(driver.find_element_by_id('btn')).perform()
			time.sleep(1)
			if doesWebElementExist(driver,By.CLASS_NAME,'blue_kit_text'):
				print driver.find_element_by_class_name('blue_kit_text').text
				ActionChains(driver).click(driver.find_element_by_css_selector(".blue_kit_left a.blue_kit_btn_back")).perform()
				break
			wait.until(EC.presence_of_element_located((By.CLASS_NAME,'btn_icon')))
			printPageAttr()
			if doesWebElementExist(driver,By.ID,'app-special'):
				driver.execute_script("document.getElementById('app-special').remove()")
			tls = driver.find_elements_by_class_name('tl_shadow')
			btns = driver.find_elements_by_class_name('btn_icon')
			driver.execute_script("document.querySelector('div[lgoinprompt]').remove()")
			if doesWebElementExist(driver,By.CSS_SELECTOR,'button.frs_pb_leadapp_pop_close'):
				driver.execute_script("document.querySelector('button.frs_pb_leadapp_pop_close').click()")
			elif doesWebElementExist(driver,By.CSS_SELECTOR,'button.daoliu_sign_in_prompt_close'):
				driver.execute_script("document.querySelector('button.daoliu_sign_in_prompt_close').click()")
			if doesWebElementExist(driver,By.CLASS_NAME,'editor-tips'):
				editorTips = driver.find_elements_by_class_name('editor-tips').text
				if editorTips == u'抱歉，您被封禁，无法发贴':
					print editorTips
					printPageAttr()
					raise
			maxFloor = 0
			for btn in btns:
				btn_string = btn.text
				if (btn_string == u"回复"):
					btn_num = 0
				else:
					btn_num = int(btn_string)
				if (btn_num >= 0 and btn_num < 30):
					maxFloor=maxFloor + 1
			if maxFloor==0:
				break
			print 'Max Floor'+str(maxFloor)
			tagetFloor = random.randint(1,maxFloor)
			print 'Target Floor'+str(tagetFloor)
			resultFloor = 0
			for btn in btns:
				btn_string = btn.text
				if btn_string == u"回复":
					btn_num = 0
				else:
					btn_num = int(btn_string)
				if btn_num>=0 and btn_num<30:
					resultFloor+=1
					if resultFloor==tagetFloor:
						print 'find target floor'
						ActionChains(driver).move_to_element(btn).click().perform()
						break
			if floorContent():
				print json.dumps(floorContent(),ensure_ascii=False,indent=2).encode('utf-8')
			else:
				break
			driver.execute_script("document.querySelector('div[lgoinprompt]').remove()")
			if doesWebElementExist(driver,By.CLASS_NAME,'overlay_content'):
				print driver.find_element_by_class_name("toast").text
				ActionChains(driver).click(driver.find_element_by_css_selector(".blue_kit_left a.blue_kit_btn_back")).perform()
				try:
					wait.until(EC.presence_of_element_located((By.LINK_TEXT,ba+u'吧')))
					printPageAttr()
				except Exception, e:
					ActionChains(driver).click(driver.find_element_by_css_selector(".blue_kit_left a.blue_kit_btn_back")).perform()
					pass

			else:
				driver.find_element_by_css_selector("a.btn_reply").click()
				wait.until(EC.visibility_of_element_located((By.TAG_NAME,"textarea")))
				printPageAttr()
				driver.find_element_by_tag_name("textarea").send_keys(content)
				if imgPath:
					driver.find_element_by_id("pic").send_keys(imgPath)
					try:
						wait.until(EC.presence_of_element_located((By.CLASS_NAME,'item_span')))
						printPageAttr()
					except Exception, e:
						print '图片没有加载成功'
						pass	
				preTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
				print preTime
				#print driver.execute_script('return $(".pb_poster_layer .vcode_baseImg_big").css("background-image")')
				driver.execute_script("document.querySelector('div.pb_poster_layer div.blue_kit_right a.j_submit_btn').click()")
				time.sleep(1)
				if doesWebElementExist(driver,By.CLASS_NAME,'overlay_content'):
					toast = driver.find_element_by_class_name("toast").text
					print toast
					if toast==u'您的帐号可能存在不当操作，暂无法正常发贴，您可申请一键恢复':
						#改用 tempfile 模块, 不要手工删除
						if imgPath:
							os.remove(imgPath)
						printPageAttr()
						raise Exception('帐号异常')
				time.sleep(3)
				bigImg = driver.execute_script('return $(".pb_poster_layer .vcode_baseImg_big").css("background-image")')
				if  len(driver.execute_script('return $(".captcha_img").attr("src")'))>100:
					testStatus(1)	
				gridImg = driver.execute_script('return $(".pb_poster_layer .grid_img").css("background-image")')
				if gridImg != 'none':
					testStatus(2)
				sendedUrl = driver.current_url
				sended = {'ba':ba,'content':content,'imgPath':imgPath,'url':sendedUrl, 'srcImg':srcImg, 'randomImg':randomImg}
				#改用 tempfile 模块, 不要手工删除
				if imgPath:
					# os.remove(imgPath)
					temp.close()
				afterTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
				print afterTime
				print json.dumps(sended,ensure_ascii=False,indent=2).encode('utf-8')
				if floorContent():
					print json.dumps(floorContent(),ensure_ascii=False,indent=2).encode('utf-8')
				else:
					break
				ActionChains(driver).click(driver.find_element_by_css_selector(".blue_kit_left a.blue_kit_btn_back")).perform()
				try:
					wait.until(EC.presence_of_element_located((By.LINK_TEXT,ba+u'吧')))
					printPageAttr()
				except Exception, e:
					ActionChains(driver).click(driver.find_element_by_css_selector(".blue_kit_left a.blue_kit_btn_back")).perform()
					pass
	cookie= driver.get_cookies()
	print json.dumps(cookie,ensure_ascii=False)
	driver.quit()
except Exception as e:
	# currentUrl= driver.current_url
	# curretntTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	# savePath = curretntTime+quote(currentUrl).replace('/','%2f')+'.png'
	# print savePath
	# driver.save_screenshot(savePath)
	cookie= driver.get_cookies()
	print cookie
	driver.quit()
	raise
else:
	pass
finally:
	pass
