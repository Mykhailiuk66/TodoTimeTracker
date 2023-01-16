from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def pagination_tasks(request, tasks, results):
    page = request.GET.get('page', 1)
    paginator = Paginator(tasks, results)
    
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        tasks = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        tasks = paginator.page(page)
        
    left_index = (int(page) - 3)
    right_index = (int(page) + 3)
        
    if left_index < 1: left_index = 1
    if right_index > paginator.num_pages: right_index = paginator.num_pages+1 
    
    custom_range = range(left_index, right_index)
    
    return custom_range, tasks