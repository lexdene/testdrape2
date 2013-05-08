import drape
import math

class WidgetBase(drape.controller.Controller):
	def __str__(self):
		return self.run()

class Pager(WidgetBase):
	def __init__(self,runbox,total_count,current_page,item_per_page=10,page_width=5):
		super(Pager,self).__init__(runbox)
		self.__total_count = total_count
		self.__current_page = current_page
		self.__item_per_page = item_per_page
		self.__page_width = page_width
	
	def limit(self):
		return dict(
			length = self.__item_per_page,
			offset = self.__current_page*self.__item_per_page
		)
	
	def process(self):
		page_count = int(math.ceil(self.__total_count*1.0/self.__item_per_page))
		self.setVariable('page_count',page_count)
		self.setVariable('current_page',self.__current_page)
		self.setVariable('total_count',self.__total_count)
		
		page_begin = self.__current_page - self.__page_width/2
		page_end = page_begin + self.__page_width
		self.setVariable('page_begin_1',page_begin)
		self.setVariable('page_end_1',page_end)
		if page_begin < 1 :
			page_begin = 1;
			page_end = min(self.__page_width,page_count-2)+1
		elif page_end >= page_count:
			page_end = page_count-1
			if page_count < self.__page_width+2:
				page_begin = 1
			else:
				page_begin = page_end - self.__page_width
		
		self.setVariable('page_begin',page_begin)
		self.setVariable('page_end',page_end)
