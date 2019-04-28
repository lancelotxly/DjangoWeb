from django.utils.functional import cached_property
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

class CustomPaginator(Paginator):
    def __init__(self,current_page,max_pager_num,*args,**kwargs):
        '''
        :param current_page: 当前页
        :param max_pager_num: 最多显示页
        :param args: obj_list, per_page
        :param kwargs:
        '''
        if current_page == None:
            self.current_page = 1
        else:
            self.current_page  = int(current_page)
        self.max_pager_num = max_pager_num
        super(CustomPaginator,self).__init__(*args,**kwargs)

    def page_num_range(self):
        if self.num_pages < self.max_pager_num:
            return range(1,self.num_pages+1)
        part = int(self.max_pager_num/2)
        if self.current_page - part < 1:
            return range(1,self.max_pager_num+1)
        if self.current_page + part > self.num_pages:
            return range(self.num_pages + 1 - self.max_pager_num, self.num_pages+1)
        return range(self.current_page-part,self.current_page+part+1)

if __name__ == '__main__':
    USER_LIST = []
    for i in range(1, 101):
        item = {'name': 'root' + str(i), 'age': i}
        USER_LIST.append(item)

    current_page = None
    per_page = 10
    max_pager_num = 20
    p_manager = CustomPaginator(current_page,max_pager_num,USER_LIST,per_page)
    print(p_manager.page_num_range())