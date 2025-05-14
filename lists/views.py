from django.http import HttpResponse
from django.shortcuts import render,redirect
from lists.models import Item,List
def home_page(request):
    return render(request, 'home.html')

def view_list(request,list_id):
    list_user = List.objects.get(id=list_id)
    return render(request,'list.html',{'list':list_user})

'''def new_list(request):
    list_user = List.objects.create()
    Item.objects.create(text=request.POST['item_text'],list=list_user)
    return redirect(f'/lists/{list_user.id}/')'''
def new_list(request):
    print("DEBUG_VIEW: new_list called") # 或者 logger.debug("new_list called")
    if request.method == 'POST':
        print(f"DEBUG_VIEW: new_list POST data: {request.POST}")
        try:
            list_user = List.objects.create()
            print(f"DEBUG_VIEW: new_list created List with id: {list_user.id}")
            item_text = request.POST.get('item_text', 'DEFAULT TEXT IF MISSING') # 使用 .get() 避免 KeyError
            Item.objects.create(text=item_text, list=list_user)
            print(f"DEBUG_VIEW: new_list created Item with text: '{item_text}' for list_id: {list_user.id}")
            redirect_url = f'/lists/{list_user.id}/'
            print(f"DEBUG_VIEW: new_list redirecting to: {redirect_url}")
            return redirect(redirect_url)
        except Exception as e:
            print(f"DEBUG_VIEW: ERROR in new_list: {e}") # 捕获并打印任何异常
            # 也许在这里返回一个错误响应或者重新抛出，取决于你希望如何处理
            raise # 重新抛出异常，让 Django 处理它（通常是500错误页面）
    # 如果不是 POST 请求，或者 POST 处理中没有返回 redirect，则会执行到这里
    print("DEBUG_VIEW: new_list did not redirect (e.g., not a POST or error before redirect)")
    return redirect('/') # 或者其他合适的行为，比如渲染一个带有错误的首页

'''def add_item(request,list_id):
    list_user = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'],list=list_user)
    return redirect(f'/lists/{list_user.id}/')'''

# lists/views.py
def add_item(request, list_id):
    print(f"DEBUG_VIEW: add_item called for list_id: {list_id}")
    if request.method == 'POST':
        print(f"DEBUG_VIEW: add_item POST data: {request.POST}")
        try:
            list_user = List.objects.get(id=list_id)
            print(f"DEBUG_VIEW: add_item found List with id: {list_user.id}")
            item_text = request.POST.get('item_text', 'DEFAULT TEXT IF MISSING')
            Item.objects.create(text=item_text, list=list_user)
            print(f"DEBUG_VIEW: add_item created Item with text: '{item_text}' for list_id: {list_user.id}")
            redirect_url = f'/lists/{list_user.id}/'
            print(f"DEBUG_VIEW: add_item redirecting to: {redirect_url}")
            return redirect(redirect_url)
        except List.DoesNotExist:
            print(f"DEBUG_VIEW: ERROR in add_item: List with id {list_id} does not exist.")
            # 通常这里会导致404
            from django.http import Http404
            raise Http404("List does not exist")
        except Exception as e:
            print(f"DEBUG_VIEW: ERROR in add_item: {e}")
            raise
    print(f"DEBUG_VIEW: add_item for list_id {list_id} was not a POST or error before redirect")
    return redirect(f'/lists/{list_id}/') # 如果不是POST，重定向回列表页