from django.http import HttpResponse
from django.shortcuts import render, redirect , get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from apps.tables.utils import product_filter
from apps.common.models import Cart

# Create your views here.

def datatables(request):
  context = {
    'segment'  : 'datatables',
    'parent'   : 'apps'
  }
  
  return render(request, 'apps/datatables.html', context)



@login_required(login_url='/users/signin/')
def post_request_handling(request, form):
    form.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/users/signin/')
def delete_product(request, id):
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/signin/')
def update_product(request, id):
    return redirect(request.META.get('HTTP_REFERER'))



