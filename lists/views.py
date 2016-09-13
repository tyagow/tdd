from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views.generic import CreateView, FormView
from django.views.generic.detail import SingleObjectMixin


from lists.forms import ExistingListItemForm, ItemForm
from lists.models import Item, List


# Create your views here
class HomePageView(FormView):
    template_name = 'home.html'
    form_class = ItemForm


class ViewAndAddToList(CreateView, SingleObjectMixin):
    model = List
    template_name = 'list.html'
    form_class = ExistingListItemForm

    def get_form(self, form_class):
        self.object = self.get_object()
        return form_class(for_list=self.object, data=self.request.POST)


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)

    return render(request, 'list.html', {'list': list_, 'form': form})

class NewListView(CreateView, HomePageView):

    def form_valid(self, form):
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})

    #try:
    #    item.full_clean()
    #    item.save()
    #except ValidationError:
    #    list_.delete()
    #    error = "You can't have an empty list item"
    #   return render(request, 'home.html', {"error":error})
    #return redirect(list_)

