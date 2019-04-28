'''
分页器:  属于控制器, 需要前后端传入数据
     1. 设定每页显示多少数据                               per_counts
     2. 从后端获得数据总条目                               total_counts
     3. 根据1，2计算总页数                                total_pages
     4. 从前端获取当前页码                                current_page
     5. 根据1，4计算当前页码的数据在数据库中的位置            start_item, end_item
     6. 数据库中取数据
     7. 传入模板中渲染

     其他功能:
     1. 首页/尾页      front_page/tail_page
     2. 前一页/后一页   prev_page/next_page
     3. 要显示多少页码  display_pages
'''
from django.utils.functional import cached_property        # 带缓存的@property
class PageManager:
    def __init__(self,total_counts,current_info,per_counts,display_pages):
        self.total_counts = total_counts
        self.current_info = current_info
        self.per_counts = per_counts
        self.display_pages = display_pages

    @property
    def total_pages(self):
        total_pages, add = divmod(self.total_counts,self.per_counts)
        if add:
            total_pages = total_pages + bool(add)
        return total_pages

    @cached_property
    def current_page(self):
        if self.current_info == None:
            current_page = 1
        else:
            current_page = int(self.current_info)
            if current_page < 1:
                current_page = 1
            elif current_page > self.total_pages:
                current_page = self.total_pages
        return current_page

    @property
    def prev_page(self):
        prev_page = self.current_page - 1
        if self.current_page == 1:
            prev_page = 1
        return prev_page

    @property
    def next_page(self):
        next_page = self.current_page + 1
        if self.current_page == self.total_pages:
            next_page = self.total_pages
        return next_page

    @property
    def front_page(self):
        return 1

    @property
    def tail_page(self):
        return self.total_pages

    def index(self):
        '''
        根据当前页和每页显示的数据量，计算当前所需数据在数据库的起止位置
        :return: start_item, end_item
        这里下标是针对list
        '''
        '''
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        '''
        start_item = (self.current_page - 1) * self.per_counts
        end_item = start_item + self.per_counts
        if end_item > self.total_counts:
            end = self.total_counts
        return start_item, end_item

    def pages_list(self):
        '''
        根据要显示多少页码，返回要显示的页号
        :return: pages_list
        '''
        if self.display_pages > self.total_pages:
            pages_list = list(range(1,self.total_pages+1))
        half_display, add = divmod(self.display_pages,2)
        if add:
            half_display = half_display + bool(add)
        if self.current_page <= half_display:
            pages_list = list(range(1,self.display_pages+1))
        elif self.current_page > self.total_pages - self.display_pages:
            pages_list = list(range(self.total_pages - self.display_pages + 1,self.total_pages+1))
        else:
            start_page = self.current_page - half_display + 1
            end_page = start_page + self.display_pages
            pages_list = list(range(start_page,end_page))
        return pages_list



if __name__ == '__main__':
    total_counts = 100
    current_info = 2
    per_counts = 10
    display_pages = 3
    p_manager = PageManager(total_counts,current_info,per_counts,display_pages)
    start_item, end_item =p_manager.index()
    print(p_manager.total_pages)
    print(p_manager.current_page)
    print(p_manager.prev_page)
    print(p_manager.next_page)
    print(start_item,end_item)
    print(p_manager.pages_list())