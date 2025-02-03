from django import template
from django.core.paginator import Paginator

register=template.Library()

@register.simple_tag
def elided_pagination_page(p,number,on_each_side=3,on_ends=2):
    print('per page is:',p.per_page)
    print('page_object is:',p.object_list.count())
    paginator=Paginator(p.object_list,p.per_page)
    return paginator.get_elided_page_range(number=number,on_each_side=on_each_side,on_ends=on_ends)

