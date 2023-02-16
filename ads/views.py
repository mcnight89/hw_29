import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, CreateView

from ads.models import Ad, User, Category, Location
from ads.serializers import CategorySerializer
from djangoProject import settings


# Create your views here.
def start_page(request):
    return HttpResponse('БЕГИТЕ ГЛУПЦЫ')


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = {
            "items": CategorySerializer(self.object_list, many=True).data
        }

        #for c in self.object_list:
           # response.append({
            #    'id': c.id,
            #    'name': c.name
            #})

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)

        category = Category.objects.create(
            name=cat_data['name']
        )

        return JsonResponse({
            'id': category.id,
            'name': category.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            cat = self.get_object()
        except Category.DoesNotExist:
            return JsonResponse({
                'status': 'error'}, status=404)

        return JsonResponse({
            'id': cat.id,
            'name': cat.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        cat_data = json.loads(request.body)

        self.object.name = cat_data['name']

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"DELETED"}, status=200)


# ===========================================================================
# ===========================================================================
@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        ads = []
        for a in page_obj:
            ads.append({
                'id': a.id,
                'name': a.name,
                'author_id': a.author_id.username,
                'price': a.price,
                'description': a.description,
                'is_published': a.is_published,
                'image': a.image.url if a.image else None,
                'category_id': a.category_id.name
            })

        response = {
            "items": ads,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', "author_id", "price", "description", "is_published", "image", "category_id"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        ads = Ad.objects.create(
            name=ad_data['name'],
            author_id=ad_data['author_id'],
            price=ad_data['price'],
            description=ad_data['description'],
            is_published=ad_data['is_published'],
            image=ad_data['image'],
            category_id=ad_data['category_id']
        )

        return JsonResponse({
            'id': ads.id,
            'name': ads.name,
            'author_id': ads.author_id.username,
            'price': ads.price,
            'description': ads.description,
            'is_published': ads.is_published,
            'image': ads.image.url if ads.image else None,
            'category_id': ads.category_id.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Ad.DoesNotExist:
            return JsonResponse({
                'status': 'error'}, status=404)

        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author': ad.author_id.username,
            'price': ad.price,
            'description': ad.description,
            'image': ad.image.url if ad.image else None,
            'is_published': ad.is_published,
            'category_id': ad.category_id.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', "author_id", "price", "description", "is_published", "image", "category_id"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        self.object.name = ad_data['name']
        self.object.author = ad_data['author_id']
        self.object.price = ad_data['price']
        self.object.description = ad_data['description']
        self.object.is_published = ad_data['is_published']
        self.object.image = ad_data['image']
        self.object.category_id = ad_data['category_id']

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author_id.username,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'image': self.image.url if self.object.image else None,
            'category_id': self.object.category_id.name

        })


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        ad = self.get_object()
        ad.image = request.FILES.get('image')
        ad.save()

        response = {
            'id': ad.id,
            'name': ad.name,
            'author': ad.author_id.username,
            'price': ad.price,
            'description': ad.description,
            'image': ad.image.url if ad.image else None,
            'is_published': ad.is_published,
            'category_id': ad.category_id.name
        }

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"DELETED"}, status=200)


# ===========================================================================
# ===========================================================================


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        users = (self.object_list.annotate(ads_published=Count('ad', filter=Q(ad__is_published=True)))
                 .select_related('location'))

        paginator = Paginator(users, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        users_on_page = paginator.get_page(page_number)

        response = {
            "items": [
                {
                    'id': u.id,
                    'first_name': u.first_name,
                    'last_name': u.last_name,
                    'username': u.username,
                    'password': u.password,
                    'role': u.role,
                    'age': u.age,
                    'location_id': u.location.name,
                    'ads_published': u.ads_published
                } for u in users_on_page],
            'total': paginator.count,
            'num_pages': paginator.num_pages
        }

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['first_name', "last_name", "username", "password", "role", "age", "location_id"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            price=user_data['price'],
            password=user_data['password'],
            role=user_data['role'],
            age=user_data['age'],
            location_id=user_data['location_id']
        )

        return JsonResponse({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'price': user.price,
            'password': user.password,
            'role': user.role,
            'age': user.age,
            'location_id': user.location_id
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error'}, status=404)

        return JsonResponse({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'password': user.password,
            'role': user.role,
            'age': user.age,
            'location_id': user.location_id
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['first_name', "last_name", "username", "password", "role", "age", "location_id"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        self.object.first_name = user_data['first_name']
        self.object.last_name = user_data['last_name']
        self.object.username = user_data['username']
        self.object.password = user_data['password']
        self.object.role = user_data['role']
        self.object.age = user_data['age']
        self.object.location_id = user_data['location_id']

        self.object.save()

        return JsonResponse({
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'price': user_data.price,
            'password': user_data.password,
            'role': user_data.role,
            'age': user_data.age,
            'location_id': user_data.location_id

        })


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"DELETED"}, status=200)
