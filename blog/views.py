from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views import generic
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory


from .models import Thinkpiece, BillBreakdown, BreakdownItem, Images, Roundup, Wastebook

from .forms import ThinkpieceForm, BillBreakdownForm, BreakdownItemForm, RoundupForm, ImageForm, WastebookForm


# Blog Pages
def wastebooks(request):
    """Show all Wastebooks"""
    wastebooks = Wastebook.objects.filter(status=1).order_by('-created_on')
    context = {'wastebooks':wastebooks}
    return render(request,'wastebooks.html',context)


def bill_breakdowns(request):
    """Show all Breakdowns"""
    bill_breakdowns = BillBreakdown.objects.filter(status=1).order_by('-created_on')
    context = {'bill_breakdowns':bill_breakdowns}
    return render(request,'bill_breakdowns.html',context)

def bill_breakdown(request,slug_text):
    """Show single breakdown and all items"""
    bill_breakdown = BillBreakdown.objects.filter(slug=slug_text)
    
    if bill_breakdown.exists():
        bill_breakdown = bill_breakdown.first()
        
    else:
        raise Http404
        
    breakdownitems = BreakdownItem.objects.filter(billbreakdown=bill_breakdown).order_by('created_on')

    context = {
        'bill_breakdown':bill_breakdown,
        'breakdownitems':breakdownitems,
        }
    return render(request, 'breakdown_detail.html',context)

def pics(request,slug_text, pic_id):
    bill_breakdown = BillBreakdown.objects.filter(slug=slug_text)
    
    if bill_breakdown.exists():
        bill_breakdown = bill_breakdown.first()
        
    else:
        raise Http404
        
    
    pics = get_object_or_404(BreakdownItem, id=pic_id)
    pic = Images.objects.filter(breakdownitem=pics)
    
    context = {
        'bill_breakdown':bill_breakdown, 
        'pics':pics,
        'pic':pic,
        }
    return render(request, 'pics.html',context)


   
class ThinkpieceList(generic.ListView):
    queryset = Thinkpiece.objects.filter(status=1).order_by('-created_on')
    template_name = 'thinkpieces.html'
    
class ThinkpieceDetail(generic.DetailView):
    model = Thinkpiece
    template_name = 'thinkpiece_detail.html'
    
class RoundupList(generic.ListView):
    queryset = Roundup.objects.filter(status=1).order_by('-created_on')
    template_name = 'roundups.html'   
    
class RoundupDetail(generic.DetailView):
    model = Roundup
    template_name = 'roundup_detail.html'


# Home Page
def index(request):

    return render(request,'index.html',{
        'wastebooks':Wastebook.objects.filter(status=1)[:1],
        'bill_breakdowns':BillBreakdown.objects.filter(status=1)[:1],
        'thinkpieces': Thinkpiece.objects.filter(status=1)[:1],
    
        })


#Admin Home

@login_required
def admin_main(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    return render(request,'admin_main.html', {
        'wastebooks':Wastebook.objects.filter(author=request.user).order_by('-created_on'),
        'bill_breakdowns':BillBreakdown.objects.filter(author=request.user).order_by('-created_on'),
        'thinkpieces':Thinkpiece.objects.filter(author=request.user).order_by('-created_on'),
        'roundups':Roundup.objects.filter(author=request.user).order_by('-created_on'),
        })



# New Wastebook
@login_required
def new_wastebook(request):
    """add new wastebook"""
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if request.method != 'POST':
        
        form = WastebookForm()
    else:
        
        form = WastebookForm(request.POST, request.FILES)
        if form.is_valid():
            form_set = form.save(commit=False)
            form_set.author = request.user
            form_set.save()
            messages.success(request, "Post successfully created")
            return redirect('blog:admin_main')

    context = {'form':form}
    return render(request,'new_wastebook.html',context)

@login_required
def edit_wastebook(request, id):
    """edit wastebook"""
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    
    wastebook = Wastebook.objects.get(id=id)
    if wastebook.author != request.user:
        raise Http404
    form_class = WastebookForm
    if request.method == 'POST':
        form = WastebookForm(data=request.POST or None, 
                                    files=request.FILES or None, 
                                    instance=wastebook)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes successful")
            return redirect('blog:admin_main')
            
    else:
        
        form = form_class(instance=wastebook)
    
    return render(request,'edit_wastebook.html',
                  {'wastebook':wastebook,'form':form})
    
@login_required        
def delete_wastebook(request, id):
    
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    
    wastebook = get_object_or_404(Wastebook, id=id)
    if wastebook.author != request.user:
        raise Http404
    if request.method =='POST':
        wastebook.delete()
        messages.success(request, "Post deleted")
        return redirect('blog:admin_main')
    
    context = {
        'wastebook':wastebook
        }
    return render(request, 'delete_wastebook.html', context)




# Thinkpieces
@login_required
def new_thinkpiece(request):
    """add new thinkpiece"""
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if request.method != 'POST':
        
        form = ThinkpieceForm()
    else:
        
        form = ThinkpieceForm(request.POST, request.FILES)
        if form.is_valid():
            form_set = form.save(commit=False)
            form_set.author = request.user
            form_set.save()
            messages.success(request, "Post successfully created")
            return redirect('blog:admin_main')
    
    
    context = {'form':form}
    return render(request,'new_thinkpiece.html',context)

@login_required
def edit_thinkpiece(request, slug):
    """add new thinkpiece"""
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    
    thinkpiece = Thinkpiece.objects.get(slug=slug)
    if thinkpiece.author != request.user:
        raise Http404
    form_class = ThinkpieceForm
    if request.method == 'POST':
        form = ThinkpieceForm(data=request.POST or None, 
                                    files=request.FILES or None, 
                                    instance=thinkpiece)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes successful")
            return redirect('blog:admin_main')
            
    else:
        
        form = form_class(instance=thinkpiece)
    
    return render(request,'edit_thinkpiece.html',
                  {'thinkpiece':thinkpiece,'form':form})

@login_required        
def delete_thinkpiece(request, slug):
    
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    
    thinkpiece = get_object_or_404(Thinkpiece, slug=slug)
    if thinkpiece.author != request.user:
        raise Http404
    if request.method =='POST':
        thinkpiece.delete()
        messages.success(request, "Post deleted")
        return redirect('blog:admin_main')
    
    context = {
        'thinkpiece':thinkpiece
        }
    return render(request, 'thinkpiece_delete.html', context)
    



# Bill Breakdowns


 # New Breakdown items
@login_required
def new_bill_breakdown(request):
    """add new bill breakdown"""
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if request.method != 'POST':
        # No data, generate blank form
        form = BillBreakdownForm()
    else:
        # POST data submitted; process data
        form = BillBreakdownForm(data=request.POST)
        if form.is_valid():
            form_set = form.save(commit=False)
            form_set.author = request.user
            form_set.save()
            return redirect('blog:admin_main')
        
    # Display blank form
    context = {'form':form}
    return render(request,'new_bill_breakdown.html',context)   

@login_required
def new_breakdown_detail(request, slug_text):
    
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    bill_breakdown = BillBreakdown.objects.filter(slug=slug_text)
    
    if bill_breakdown.exists():
        bill_breakdown = bill_breakdown.first()
        
    else:
        raise Http404
        
    
    ImageFormSet = modelformset_factory(Images,fields=('image',), extra=4)
    #'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':
    
        postForm = BreakdownItemForm(request.POST)
        formset = ImageFormSet(request.POST or None, request.FILES or None)
    
    
        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()
            
            for form in formset.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if form:
                    photo = Images(breakdownitem=post_form, image=form['image'])
                    photo.save()
            # use django messages framework
            messages.success(request,
                             "Success!")
            BreakdownItemForm()
            ImageFormSet(queryset=Images.objects.none())
        else:
            print(postForm.errors, formset.errors)
    else:
        postForm = BreakdownItemForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'new_breakdown_detail.html',
                  {'bill_breakdown':bill_breakdown,'postForm': postForm, 'formset': formset})



# Edit Breakdown Items
@login_required
def edit_breakdown_view(request, slug_text):
    """Breakdown edit view"""
    
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    
    bill_breakdown = BillBreakdown.objects.filter(slug=slug_text)
    
    if bill_breakdown.exists():
        bill_breakdown = bill_breakdown.first()
        
    else:
        raise Http404
    
    if bill_breakdown.author != request.user:
        raise Http404
        
    breakdown_items = BreakdownItem.objects.filter(billbreakdown=bill_breakdown).order_by('created_on')
    
    context = {
        'bill_breakdown':bill_breakdown,
        'breakdown_items':breakdown_items,
        }
    return render(request, 'edit_breakdown_view.html',context)

@login_required
def edit_breakdown_head(request, slug_text):
    """edit breakdown head"""
    
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    
    bill_breakdown = BillBreakdown.objects.get(slug=slug_text)
    
    if bill_breakdown.author != request.user:
        raise Http404
        
    form_class = BillBreakdownForm
    if request.method == 'POST':
        form = BillBreakdownForm(data=request.POST or None, 
                                    files=request.FILES or None, 
                                    instance=bill_breakdown)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes successful")
            return redirect('blog:admin_main')
            
    else:
        # No data, generate blank form
        form = form_class(instance=bill_breakdown)
    
    return render(request,'edit_breakdown_head.html',
                  {'bill_breakdown':bill_breakdown,'form':form})


@login_required
def edit_breakdown_detail(request, slug_text, breakdownitem_id):
    """edit breakdown head""" 
    
    
    
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    
    bill_breakdown = get_object_or_404(BillBreakdown, slug=slug_text)
    breakdown_item = get_object_or_404(BreakdownItem, id=breakdownitem_id)
    form_class = BreakdownItemForm
    ImageFormSet = modelformset_factory(Images,fields=('image',), extra=6, max_num=6)
    
    if bill_breakdown.author != request.user:
        raise Http404
        
    if request.method == 'POST':
        postForm = BreakdownItemForm(request.POST or None,  instance=breakdown_item)
        formset = ImageFormSet(request.POST or None,request.FILES or None)
        
        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()
            data = Images.objects.filter(breakdownitem=breakdown_item)
            
            for index, f in enumerate(formset):
                if f.cleaned_data:
                    if f.cleaned_data['id'] is None:
                        photo = Images(breakdownitem=breakdown_item, 
                                       image=f.cleaned_data.get('image'))
                        photo.save()
                    elif f.cleaned_data['image'] is False:
                        photo = Images.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
                        photo.delete()
                    else:
                        photo = Images(breakdownitem=breakdown_item, 
                                       image=f.cleaned_data.get('image'))
                        d = Images.objects.get(id=data[index].id)
                        d.image = photo.image
                        d.save()
                        
            return redirect('blog:edit_breakdown_view', slug_text=bill_breakdown.slug)
               
                    
    else:
        # No data, generate blank form
        form = form_class(instance=breakdown_item)
        formset = ImageFormSet(queryset=Images.objects.filter(breakdownitem=breakdown_item))
    
    return render(request,'edit_breakdown_detail.html',
                  {'bill_breakdown':bill_breakdown, 
                   'breakdown_item':breakdown_item,
                   'formset':formset,
                   'postForm':form})

# Delete Breakdown Items
@login_required
def delete_breakdown(request, slug_text):
    
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    bill_breakdown = get_object_or_404(BillBreakdown, slug=slug_text)
    
    if bill_breakdown.author != request.user:
        raise Http404
    
    if request.method =='POST':
        bill_breakdown.delete()
        messages.success(request, "Post deleted")
        return redirect('blog:admin_main')
    
    context = {'bill_breakdown':bill_breakdown}
    return render(request, 'breakdown_delete.html', context)
@login_required
def delete_breakdown_detail(request, slug_text, breakdownitem_id):
    """edit breakdown item""" 
    
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    
    bill_breakdown = get_object_or_404(BillBreakdown, slug=slug_text)
    breakdown_item = get_object_or_404(BreakdownItem, id=breakdownitem_id)
    
    if bill_breakdown.author != request.user:
        raise Http404
   
    if request.method == 'POST':
        breakdown_item.delete()
        messages.success(request, "Post deleted")
        return redirect('blog:edit_breakdown_view', slug_text=bill_breakdown.slug)
        
    context = {'bill_breakdown':bill_breakdown,
               'breakdown_item':breakdown_item} 
    return render(request, 'breakdown_item_delete.html', context)


# Weekly Roundup

@login_required
def new_roundup(request):
    """add new roundup"""
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if request.method != 'POST':
        
        form = RoundupForm()
    else:
        
        form = RoundupForm(data=request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Post successfully created")
            return redirect('blog:admin_main')
       
    context = {'form':form}
    return render(request,'new_roundup.html',context)


@login_required
def edit_roundup(request, slug):
    """add new thinkpiece"""
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    
    roundup = Roundup.objects.get(slug=slug)
    if roundup.author != request.user:
        raise Http404
    form_class = RoundupForm
    if request.method == 'POST':
        form = RoundupForm(data=request.POST or None, 
                                    files=request.FILES or None, 
                                    instance=roundup)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes successful")
            return redirect('blog:admin_main')
            
    else:
        
        form = form_class(instance=roundup)
    
    return render(request,'edit_roundup.html',
                  {'roundup':roundup,'form':form})

@login_required        
def delete_roundup(request, slug):
    
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    
    roundup = get_object_or_404(Roundup, slug=slug)
    if roundup.author != request.user:
        raise Http404
    if request.method =='POST':
        roundup.delete()
        messages.success(request, "Post deleted")
        return redirect('blog:admin_main')
    
    context = {
        'roundup':roundup
        }
    return render(request, 'roundup_delete.html', context)
