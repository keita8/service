from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import *
from .models import *
from django.db.models import Q
from .forms import *



class BlogSearchListView(ListView):
    model = BlogPost
    template_name = 'layout/blog_search_result.html'
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        context = super(BlogSearchListView, self).get_context_data(**kwargs)
        context["query"] = self.request.GET.get('query')
        print(context)
        if context is not None:
            return context
        return BlogPost.objects.all()
    
    
    def get_queryset(self, *args, **kwargs):
        request = self.request
        print(request.GET)
        
        query = request.GET.get('query', None)
        print(query)
        if query is not None:
            return BlogPost.objects.search(query)
        return BlogPost.objects.all()
    
    


class BlogListView(ListView):
    model = BlogPost
    template_name = 'layout/blog.html'
    context_object_name = 'posts'
    paginate_by = 6
    



    
class BlogDetailView(DetailView):
    # qs = Product.objects.all()
    
    template_name = 'layout/blog-detail.html'
    context_object_name = 'blog_detail'
    slug_url_kwarg = 'slug'
    form = CommentForm

    
    def get_context_data(self, *args, **kwargs):
        request = self.request
        context = super(BlogDetailView, self).get_context_data(*args,**kwargs)
        # try:
        #     context['related_products'] = self.get_object().related
        # except AttributeError:
        #     raise Http404("Aucun article trouvé !")
        return context
        
    
    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = BlogPost.objects.get_by_slug(slug)
        except BlogPost.DoesNotExist:
            raise Http404("Aucun article trouvé !")
        except BlogPost.MultipleObjectsReturned:
            qs = BlogPost.objects.filter(slug=slug, status=1)
            instance = qs.first()
        except:
            raise Http404("Cet article n'existe pas !!!")
        return instance
    
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            # form.instance.name = 
    
    
    
    


class BlogUpdateView(UpdateView):
    template_name = 'layout/blog-update.html'
    model = BlogPost




class BlogDeleteView(DeleteView):
    template_name = 'layout/blog-delete.html'
    model = BlogPost
    
    
    
    





def CategoriesListView(request):
    queryset = Category.objects.all().order_by('-id')
    template_name = 'include/blog-sidebar.html'
    context = {
        'queryset':queryset
    }
    
    return render(request, template_name, context)
    
    


def post_by_categorie(request, id):
    categorie  = get_object_or_404(Category, id=id)
    posts      = BlogPost.objects.filter(category=categorie, status=1)
    template_name = 'layout/blog_post_by_categories.html'
    context  = {
        'posts': posts,
        'categorie': categorie.title
    }
    return render(request, template_name, context)
    
    
    


def addcomment(request):
    if request.method == "POST":
        pass
    return JsonResponse({'data': 'ok'})