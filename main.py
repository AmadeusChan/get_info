import re
import urllib2
import Queue

class spider(object):

	def __init__(self, initial_page_list):
		self.initial_page_list = initial_page_list

	def deal_with_page(self, url, html):
		f = file("url_list.txt", "a")
		f.write(url+'\n')
		f.close()
		if re.search(re.compile(r'\.pdf'), url) != None:
			f = file("pdf_list.txt", "a")
			f.write(url)
	
	def get_new_urls(self, url, html):
		url_list = []
		href_pattern = re.compile(r'href=".*?"')
		herf_list = re.findall(href_pattern, html)
		for herf in herf_list:
			herf_parts = re.split(re.compile(r'"'), herf)
			new_url = herf_parts[1]
			
			#f = file("A.txt","a")
			#f.write(new_url+'\n');
			#f.close()

			#print "new_url:", new_url
			if new_url[:4] == "http":
				pass
			else:
				url_parts = re.split(re.compile(r'/'), new_url)
				first_part = ''
				for part in url_parts:
					if len(part):
						first_part = '/' + part
						break
				#print first_part+'.*'
				try:
					first_part_pattern = re.compile(first_part+'.*')
				except re.error, e:
					print e
				if re.search(first_part_pattern, url) != None:
					new_url = re.sub(first_part_pattern, new_url, url)
				else:
					new_url = url + new_url
					
			if re.search(re.compile(r'tsinghua\.edu\.cn'),new_url) != None:
				url_list.append(new_url)
				#print new_url
		return url_list

	def work(self):
		cnt = 0

		url_queue = Queue.Queue()
		url_set = set()
		for initial_page in self.initial_page_list:
			url_queue.put(initial_page)
			url_set.add(initial_page)

		while url_queue.empty() == False:

			current_url = url_queue.get()
			#user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
			#headers = {'User-Agent' : user_agent}
			try:
				#request = urllib2.Request(current_url,None,headers)
				#print "requested"
				request = urllib2.Request(current_url)
				response = urllib2.urlopen(request,None,timeout=2)
			except Exception, e:
				print e
				continue
			current_html = response.read()

			self.deal_with_page(current_url, current_html)
			cnt = cnt + 1
			print cnt, ':', current_url, "            queue_size:", url_queue.qsize(), "set_size:", len(url_set)

			new_url_list = self.get_new_urls(current_url, current_html)
			for new_url in new_url_list:
				if new_url not in url_set:
					#pass
					url_queue.put(new_url)
					url_set.add(new_url)



initial_list = ["http://info.tsinghua.edu.cn/", "http://www.tsinghua.edu.cn/publish/newthu/index.html","http://learn.tsinghua.edu.cn/","http://academic.tsinghua.edu.cn/"]
spider = spider(initial_list)
spider.work()
#url = "http://info.tsinghua.edu.cn"
#response = urllib2.urlopen(url)
#html = response.read()
#urls = spider.get_new_urls(url, html)
#for u in urls:
#	print u
