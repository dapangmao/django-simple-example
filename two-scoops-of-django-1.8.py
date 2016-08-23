#------------chapter_01_example_1.py--------------

from __future__ import absolute_import

from math import sqrt

from os.path import abspath



# Core Django imports

from django.db import models

from django.utils.translation import ugettext_lazy as _



# Third-party app imports

from django_extensions.db.models import TimeStampedModel



# Imports from your apps

from splits.models import BananaSplit

#------------chapter_01_example_2.py--------------

from __future__ import absolute_import

from django.views.generic import CreateView



# Relative imports of the 'cones' package

from .models import WaffleCone

from .forms import WaffleConeForm

from core.views import FoodMixin



class WaffleConeCreateView(FoodMixin, CreateView):

    model = WaffleCone

    form_class = WaffleConeForm 

#------------chapter_01_example_3.py--------------

from django.db import models

#------------chapter_01_example_4.py--------------

    url(regex='^add/$',

        view=views.add_topping,

        name='add_topping'),

    ]

#------------chapter_05_example_14.py--------------

import os

SOME_SECRET_KEY = os.environ["SOME_SECRET_KEY"]

#------------chapter_05_example_15.py--------------

import os



# Normally you should not import ANYTHING from Django directly

# into your settings, but ImproperlyConfigured is an exception.

from django.core.exceptions import ImproperlyConfigured



def get_env_variable(var_name):

    """Get the environment variable or return exception."""

    try:

        return os.environ[var_name]

    except KeyError:

        error_msg = "Set the {} environment variable".format(var_name)

        raise ImproperlyConfigured(error_msg)

#------------chapter_05_example_19.py--------------



import json



# Normally you should not import ANYTHING from Django directly

# into your settings, but ImproperlyConfigured is an exception.

from django.core.exceptions import ImproperlyConfigured



# JSON-based secrets module

with open("secrets.json") as f:

    secrets = json.loads(f.read())



def get_secret(setting, secrets=secrets):

    """Get the secret variable or return explicit exception."""

    try:

        return secrets[setting]

    except KeyError:

        error_msg = "Set the {0} environment variable".format(setting)

        raise ImproperlyConfigured(error_msg)



SECRET_KEY = get_secret("SECRET_KEY")

#------------chapter_05_example_27.py--------------

from unipath import Path



BASE_DIR = Path(__file__).ancestor(3)

MEDIA_ROOT = BASE_DIR.child("media")

STATIC_ROOT = BASE_DIR.child("static")

STATICFILES_DIRS = (

    BASE_DIR.child("assets"),

)

TEMPLATES = [

    {

        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        DIRS = (BASE_DIR.child("templates"),)

    },

]

#------------chapter_05_example_28.py--------------

from os.path import join, abspath, dirname



here = lambda *dirs: join(abspath(dirname(__file__)), *dirs)

BASE_DIR = here("..", "..")

root = lambda *dirs: join(abspath(BASE_DIR), *dirs)



# Configuring MEDIA_ROOT

MEDIA_ROOT = root("media")



# Configuring STATIC_ROOT

STATIC_ROOT = root("collected_static")



# Additional locations of static files

STATICFILES_DIRS = (

    root("assets"),

)



# Configuring TEMPLATE_DIRS

TEMPLATES = [

    {

        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        DIRS = (root("templates"),)

    },

]

#------------chapter_05_example_4.py--------------

from .base import *



DEBUG = True



EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



DATABASES = {

    "default": {

        "ENGINE": "django.db.backends.postgresql_psycopg2",

        "NAME": "twoscoops",

        "USER": "",

        "PASSWORD": "",

        "HOST": "localhost",

        "PORT": "",

    }

}



INSTALLED_APPS += ("debug_toolbar", )

#------------chapter_05_example_6.py--------------

from .local import *



# Set short cache timeout 

CACHE_TIMEOUT = 30

#------------chapter_06_example_1.py--------------

from django.db import models



class TimeStampedModel(models.Model):

    """

    An abstract base class model that provides self-

    updating ``created`` and ``modified`` fields.

    """

    created = models.DateTimeField(auto_now_add=True)

    modified = models.DateTimeField(auto_now=True)



    class Meta:

        abstract = True

#------------chapter_06_example_2.py--------------

    abstract = True

#------------chapter_06_example_3.py--------------

from django.db import models



from core.models import TimeStampedModel



class Flavor(TimeStampedModel):

    title = models.CharField(max_length=200)

#------------chapter_06_example_4.py--------------

from django.utils import timezone



class PublishedManager(models.Manager):



    use_for_related_fields = True



    def published(self, **kwargs):

        return self.filter(pub_date__lte=timezone.now(), **kwargs)



class FlavorReview(models.Model):

    review = models.CharField(max_length=255)

    pub_date = models.DateTimeField()



    # add our custom model manager

    objects = PublishedManager()

#------------chapter_07_example_1.py--------------



from flavors.models import Flavor

from store.exceptions import OutOfStock



def list_flavor_line_item(sku):

    try:

        return Flavor.objects.get(sku=sku, quantity__gt=0)

    except Flavor.DoesNotExist:

        msg = "We are out of {0}".format(sku)

        raise OutOfStock(msg)



def list_any_line_item(model, sku):

    try:

        return model.objects.get(sku=sku, quantity__gt=0)

    except ObjectDoesNotExist:

        msg = "We are out of {0}".format(sku)

        raise OutOfStock(msg)

#------------chapter_07_example_2.py--------------

from store.exceptions import OutOfStock, CorruptedDatabase



def list_flavor_line_item(sku):

    try:

        return Flavor.objects.get(sku=sku, quantity__gt=0)

    except Flavor.DoesNotExist:

        msg = "We are out of {}".format(sku)

        raise OutOfStock(msg)

    except Flavor.MultipleObjectsReturned:

        msg = "Multiple items have SKU {}. Please fix!".format(sku)

        raise CorruptedDatabase(msg)

#------------chapter_07_example_3.py--------------

from django.models import Q



from promos.models import Promo



def fun_function(**kwargs):

    """Find working ice cream promo"""

    results = Promo.objects.active()

    results = results.filter(

                Q(name__startswith=name) |

                Q(description__icontains=name)

            )

    results = results.exclude(status='melted')

    results = results.select_related('flavors')

    return results

#------------chapter_07_example_4.py--------------



from models.customers import Customer



customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))

#------------chapter_07_example_6.py--------------



DATABASES = {

    'default': {

        # ...

        'ATOMIC_REQUESTS': True,

    },

}

#------------chapter_07_example_7.py--------------



from django.db import transaction

from django.http import HttpResponse

from django.shortcuts import get_object_or_404

from django.utils import timezone



from .models import Flavor



@transaction.non_atomic_requests

def posting_flavor_status(request, pk, status):

    flavor = get_object_or_404(Flavor, pk=pk)



    # This will execute in autocommit mode (Django's default).

    flavor.latest_status_change_attempt = timezone.now()

    flavor.save()



    with transaction.atomic():

        # This code executes inside a transaction.

        flavor.status = status

        flavor.latest_status_change_success = timezone.now()

        flavor.save()

        return HttpResponse("Hooray")



    # If the transaction fails, return the appropriate status

    return HttpResponse("Sadness", status_code=400)

#------------chapter_08_example_1.py--------------

from django.views.generic import ListView, DetailView, UpdateView

from django.core.urlresolvers import reverse



from .models import Tasting



class TasteListView(ListView):

    model = Tasting



class TasteDetailView(DetailView):

    model = Tasting



class TasteResultsView(TasteDetailView):

    template_name = "tastings/results.html"



class TasteUpdateView(UpdateView):

    model = Tasting



    def get_success_url(self):

        return reverse("tastings:detail",

            kwargs={"pk": self.object.pk})

#------------chapter_08_example_10.py--------------

from django.http import HttpResponse

from django.views.generic import View



# The simplest FBV

def simplest_view(request):

    # Business logic goes here

    return HttpResponse("FBV")



# The simplest CBV

class SimplestView(View):

    def get(self, request, *args, **kwargs):

        # Business logic goes here

        return HttpResponse("CBV")

#------------chapter_08_example_11.py--------------

    return render(request, 'melted_ice_cream_report.html', dict{

        'store': get_object_or_404(Store, id=store_id),

        'now': timezone.now()

    })

#------------chapter_08_example_2.py--------------

from django.conf.urls import url



from . import views



urlpatterns = [

    url(

        regex=r"^$",

        view=views.TasteListView.as_view(),

        name="list"

    ),

    url(

        regex=r"^(?P<pk>\d+)/$",

        view=views.TasteDetailView.as_view(),

        name="detail"

    ),

    url(

        regex=r"^(?P<pk>\d+)/results/$",

        view=views.TasteResultsView.as_view(),

        name="results"

    ),

    url(

        regex=r"^(?P<pk>\d+)/update/$",

        view=views.TasteUpdateView.as_view(),

        name="update"

    )

]

#------------chapter_08_example_3.py--------------

urlpatterns += [

    url(r'^tastings/', include('tastings.urls', namespace='tastings')),

]

#------------chapter_08_example_4.py--------------

class TasteUpdateView(UpdateView):

    model = Tasting



    def get_success_url(self):

        return reverse("tastings:detail", 

            kwargs={"pk": self.object.pk})

#------------chapter_08_example_6.py--------------

urlpatterns += [

    url(r'^contact/', include('contactmonger.urls',

                                        namespace='contactmonger')),

    url(r'^report-problem/', include('contactapp.urls',

                                            namespace='contactapp')),

]

#------------chapter_08_example_8.py--------------

from django.conf.urls import url



from . import views



urlpatterns = [

    # Defining the views explicitly

    url(r'^$', views.index, name='index'),

]

#------------chapter_08_example_9.py--------------

HttpResponse = view(HttpRequest)



# Deciphered into basic math (remember functions from algebra?)

y = f(x)



# ... and then translated into a CBV example

HttpResponse = View.as_view()(HttpRequest)



#------------chapter_09_example_1.py--------------



from django.core.exceptions import PermissionDenied



def check_sprinkle_rights(request):

    if request.user.can_sprinkle or request.user.is_staff:

        return request



    # Return a HTTP 403 back to the user

    raise PermissionDenied 

#------------chapter_09_example_2.py--------------



from django.core.exceptions import PermissionDenied



def check_sprinkles(request):

    if request.user.can_sprinkle or request.user.is_staff:

        # By adding this value here it means our display templates

        #   can be more generic. We don't need to have

        #   {% if request.user.can_sprinkle or request.user.is_staff %}

        #   instead just using

        #   {% if request.can_sprinkle %}

        request.can_sprinkle = True

        return request



    # Return a HTTP 403 back to the user

    raise PermissionDenied

#------------chapter_09_example_3.py--------------



from django.shortcuts import get_object_or_404

from django.shortcuts import render



from .utils import check_sprinkles

from .models import Sprinkle



def sprinkle_list(request):

    """Standard list view"""



    request = check_sprinkles(request)



    return render(request,

        "sprinkles/sprinkle_list.html",

        {"sprinkles": Sprinkle.objects.all()})



def sprinkle_detail(request, pk):

    """Standard detail view"""



    request = check_sprinkles(request)



    sprinkle = get_object_or_404(Sprinkle, pk=pk)



    return render(request, "sprinkles/sprinkle_detail.html",

        {"sprinkle": sprinkle})



def sprinkle_preview(request):

    """"preview of new sprinkle, but without the

            check_sprinkles function being used.

    """

    sprinkle = Sprinkle.objects.all()

    return render(request,

        "sprinkles/sprinkle_preview.html",

        {"sprinkle": sprinkle})

#------------chapter_09_example_4.py--------------

from django.views.generic import DetailView



from .utils import check_sprinkles

from .models import Sprinkle



class SprinkleDetail(DetailView):

    """Standard detail view"""



    model = Sprinkle



    def dispatch(self, request, *args, **kwargs):

        request = check_sprinkles(request)

        return super(SprinkleDetail, self).dispatch(

                                request, *args, **kwargs)



#------------chapter_09_example_5.py--------------

import functools



def decorator(view_func):

    @functools.wraps(view_func)

    def new_view_func(request, *args, **kwargs):

        # You can modify the request (HttpRequest) object here.

        response = view_func(request, *args, **kwargs)

        # You can modify the response (HttpResponse) object here.

        return response

    return new_view_func

#------------chapter_09_example_6.py--------------

from functools import wraps



from . import utils



# based off the decorator template from Example 8.5

def check_sprinkles(view_func):

    """Check if a user can add sprinkles"""

    @wraps(view_func)

    def new_view_func(request, *args, **kwargs):

        # Act on the request object with utils.can_sprinkle()

        request = utils.can_sprinkle(request)



        # Call the view function

        response = view_func(request, *args, **kwargs)



        # Return the HttpResponse object

        return response

    return new_view_func

#------------chapter_09_example_7.py--------------

from django.shortcuts import get_object_or_404, render



from .decorators import check_sprinkles

from .models import Sprinkle



# Attach the decorator to the view

@check_sprinkles

def sprinkle_detail(request, pk):

    """Standard detail view"""



    sprinkle = get_object_or_404(Sprinkle, pk=pk)



    return render(request, "sprinkles/sprinkle_detail.html",

        {"sprinkle": sprinkle})

#------------chapter_10_example_1.py--------------



class FreshFruitMixin(object):



    def get_context_data(self, **kwargs):

        context = super(FreshFruitMixin,

                    self).get_context_data(**kwargs)

        context["has_fresh_fruit"] = True

        return context



class FruityFlavorView(FreshFruitMixin, TemplateView):

    template_name = "fruity_flavor.html"

#------------chapter_10_example_11.py--------------



from .models import Flavor



class FlavorListView(ListView):

    model = Flavor



    def get_queryset(self):

        # Fetch the queryset from the parent get_queryset

        queryset = super(FlavorListView, self).get_queryset()



        # Get the q GET parameter

        q = self.request.GET.get("q")

        if q:

            # Return a filtered queryset

            return queryset.filter(title__icontains=q)

        # Return the base queryset

        return queryset



#------------chapter_10_example_13.py--------------

from django.shortcuts import render, redirect

from django.views.generic import View



from braces.views import LoginRequiredMixin



from .forms import FlavorForm

from .models import Flavor



class FlavorView(LoginRequiredMixin, View):



    def get(self, request, *args, **kwargs):

        # Handles display of the Flavor object

        flavor = get_object_or_404(Flavor, slug=kwargs['slug'])

        return render(request,

            "flavors/flavor_detail.html",

                {"flavor": flavor}

            )



    def post(self, request, *args, **kwargs):

        # Handles updates of the Flavor object

        flavor = get_object_or_404(Flavor, slug=kwargs['slug'])

        form = FlavorForm(request.POST)

        if form.is_valid():

            form.save()

        return redirect("flavors:detail", flavor.slug)



#------------chapter_10_example_14.py--------------

from django.shortcuts import get_object_or_404

from django.views.generic import View



from braces.views import LoginRequiredMixin



from .models import Flavor

from .reports import make_flavor_pdf



class PDFFlavorView(LoginRequiredMixin, View):



    def get(self, request, *args, **kwargs):

        # Get the flavor

        flavor = get_object_or_404(Flavor, slug=kwargs['slug'])



        # create the response

        response = HttpResponse(content_type='application/pdf')



        # generate the PDF stream and attach to the response

        response = make_flavor_pdf(response, flavor)



        return response



#------------chapter_10_example_2.py--------------

from django.views.generic import DetailView



from braces.views import LoginRequiredMixin



from .models import Flavor



class FlavorDetailView(LoginRequiredMixin, DetailView):

    model = Flavor

#------------chapter_10_example_3.py--------------



from braces.views import LoginRequiredMixin



from .models import Flavor



class FlavorCreateView(LoginRequiredMixin, CreateView):

    model = Flavor

    fields = ('title', 'slug', 'scoops_remaining')



    def form_valid(self, form):

        # Do custom logic here

        return super(FlavorCreateView, self).form_valid(form)

#------------chapter_10_example_4.py--------------



from braces.views import LoginRequiredMixin



from .models import Flavor



class FlavorCreateView(LoginRequiredMixin, CreateView):

    model = Flavor



    def form_invalid(self, form):

        # Do custom logic here

        return super(FlavorCreateView, self).form_invalid(form)

#------------chapter_10_example_5.py--------------

from django.views.generic import UpdateView, TemplateView



from braces.views import LoginRequiredMixin



from .models import Flavor

from .tasks import update_users_who_favorited



class FavoriteMixin(object):



    @cached_property

    def likes_and_favorites(self):

        """Returns a dictionary of likes and favorites"""

        likes = self.object.likes()

        favorites = self.object.favorites()

        return {

            "likes": likes,

            "favorites": favorites,

            "favorites_count": favorites.count(),



        }



class FlavorUpdateView(LoginRequiredMixin, FavoriteMixin, UpdateView):

    model = Flavor

    fields = ('title', 'slug', 'scoops_remaining')



    def form_valid(self, form):

        update_users_who_favorited(

            instance=self.object,

            favorites=self.likes_and_favorites['favorites']

        )

        return super(FlavorCreateView, self).form_valid(form)



class FlavorDetailView(LoginRequiredMixin, FavoriteMixin, TemplateView):

    model = Flavor

#------------chapter_10_example_7.py--------------

from django.core.urlresolvers import reverse

from django.db import models



STATUS = (

    (0, "zero"),

    (1, "one"),

)



class Flavor(models.Model):

    title = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)

    scoops_remaining = models.IntegerField(default=0, choices=STATUS)



    def get_absolute_url(self):

        return reverse("flavors:detail", kwargs={"slug": self.slug})

#------------chapter_10_example_8.py--------------

from django.views.generic import CreateView, UpdateView, DetailView



from braces.views import LoginRequiredMixin



from .models import Flavor



class FlavorCreateView(LoginRequiredMixin, CreateView):

    model = Flavor

    fields = ('title', 'slug', 'scoops_remaining')



class FlavorUpdateView(LoginRequiredMixin, UpdateView):

    model = Flavor

    fields = ('title', 'slug', 'scoops_remaining')



class FlavorDetailView(DetailView):

    model = Flavor

#------------chapter_10_example_9.py--------------



from django.contrib import messages

from django.views.generic import CreateView, UpdateView, DetailView



from braces.views import LoginRequiredMixin



from .models import Flavor



class FlavorActionMixin(object):



    fields = ('title', 'slug', 'scoops_remaining')



    @property

    def success_msg(self):

        return NotImplemented



    def form_valid(self, form):

        messages.info(self.request, self.success_msg)

        return super(FlavorActionMixin, self).form_valid(form)



class FlavorCreateView(LoginRequiredMixin, FlavorActionMixin,

                        CreateView):

    model = Flavor

    success_msg = "Flavor created!"



class FlavorUpdateView(LoginRequiredMixin, FlavorActionMixin,

                        UpdateView):

    model = Flavor

    success_msg = "Flavor updated!"



class FlavorDetailView(DetailView):

    model = Flavor

#------------chapter_11_example_1.py--------------

import StringIO



from django import forms



from .models import Purchase, Seller



class PurchaseForm(forms.ModelForm):



    class Meta:

        model = Purchase



    def clean_seller(self):

        seller = self.cleaned_data["seller"]

        try:

            Seller.objects.get(name=seller)

        except Seller.DoesNotExist:

            msg = "{0} does not exist in purchase #{1}.".format(

                seller,

                self.cleaned_data["purchase_number"]

            )

            raise forms.ValidationError(msg)

        return seller



def add_csv_purchases(rows):



    rows = StringIO.StringIO(rows)



    records_added = 0

    errors = []

    # Generate a dict per row, with the first CSV row being the keys.

    for row in csv.DictReader(rows, delimiter=","):



        # Bind the row data to the PurchaseForm.

        form = PurchaseForm(row)

        # Check to see if the row data is valid.

        if form.is_valid():

            # Row data is valid so save the record.

            form.save()

            records_added += 1

        else:

            errors.append(form.errors)



    return records_added, errors



#------------chapter_11_example_2.py--------------

#------------chapter_11_example_4.py--------------



from .models import Taster



class TasterForm(forms.ModelForm):



    class Meta:

        model = Taster



    def __init__(self, *args, **kwargs):

        # set the user as an attribute of the form

        self.user = kwargs.pop('user')

        super(TasterForm, self).__init__(*args, **kwargs)

#------------chapter_11_example_5.py--------------



from braces.views import LoginRequiredMixin



from .forms import TasterForm

from .models import Taster



class TasterUpdateView(LoginRequiredMixin, UpdateView):

    model = Taster

    form_class = TasterForm

    success_url = "/someplace/"



    def get_form_kwargs(self):

        """This method is what injects forms with their keyword arguments."""

        # grab the current set of form #kwargs

        kwargs = super(TasterUpdateView, self).get_form_kwargs()

        # Update the kwargs with the user_id

        kwargs['user'] = self.request.user

        return kwargs

#------------chapter_11_example_6.py--------------

from django.db import models



class ModelFormFailureHistory(models.Model):

    form_data = models.TextField()

    model_data = models.TextField()

#------------chapter_11_example_7.py--------------

import json



from django.contrib import messages

from django.core import serializers



from core.models import ModelFormFailureHistory



class FlavorActionMixin(object):



    @property

    def success_msg(self):

        return NotImplemented



    def form_valid(self, form):

        messages.info(self.request, self.success_msg)

        return super(FlavorActionMixin, self).form_valid(form)



    def form_invalid(self, form):

        """Save invalid form and model data for later reference."""

        form_data = json.dumps(form.cleaned_data)

        model_data = serializers.serialize("json",

                    [form.instance])[1:-1]

        ModelFormFailureHistory.objects.create(

            form_data=form_data,

            model_data=model_data

        )

        return super(FlavorActionMixin,

                    self).form_invalid(form)



#------------chapter_11_example_8.py--------------



class IceCreamReviewForm(forms.Form):

    # Rest of tester form goes here

    ...



    def clean(self):

        cleaned_data = super(TasterForm, self).clean()

        flavor = cleaned_data.get("flavor")

        age = cleaned_data.get("age")



        if flavor == 'coffee' and age < 3:

            # Record errors that will be displayed later.

            msg = u"Coffee Ice Cream is not for Babies."

            self.add_error('flavor', msg)

            self.add_error('age', msg)



        # Always return the full collection of cleaned data.

        return cleaned_data

#------------chapter_12_example_1.py--------------

from django.views.generic import CreateView, UpdateView



from braces.views import LoginRequiredMixin



from .models import Flavor



class FlavorCreateView(LoginRequiredMixin, CreateView):

    model = Flavor

    fields = ('title', 'slug', 'scoops_remaining')



class FlavorUpdateView(LoginRequiredMixin, UpdateView):

    model = Flavor

    fields = ('title', 'slug', 'scoops_remaining')

#------------chapter_12_example_10.py--------------

# Call phone and description from the self.fields dict-like object

from django import forms



from .models import IceCreamStore



class IceCreamStoreUpdateForm(forms.ModelForm):



    class Meta:

        model = IceCreamStore



    def __init__(self, *args, **kwargs):

        # Call the original __init__ method before assigning

        # field overloads

        super(IceCreamStoreUpdateForm, self).__init__(*args,

                            **kwargs)

        self.fields["phone"].required = True

        self.fields["description"].required = True

#------------chapter_12_example_11.py--------------

from django import forms



from .models import IceCreamStore



class IceCreamStoreCreateForm(forms.ModelForm):



    class Meta:

        model = IceCreamStore

        fields = ("title", "block_address", )



class IceCreamStoreUpdateForm(IceCreamStoreCreateForm):



    def __init__(self, *args, **kwargs):

        super(IceCreamStoreUpdateForm,

                self).__init__(*args, **kwargs)

        self.fields["phone"].required = True

        self.fields["description"].required = True



    class Meta(IceCreamStoreCreateForm.Meta):

        # show all the fields!

        fields = ("title", "block_address", "phone",

                "description", )

#------------chapter_12_example_12.py--------------

from django.views.generic import CreateView, UpdateView



from .forms import IceCreamStoreCreateForm

from .forms import IceCreamStoreUpdateForm

from .models import IceCreamStore



class IceCreamCreateView(CreateView):

    model = IceCreamStore

    form_class = IceCreamStoreCreateForm



class IceCreamUpdateView(UpdateView):

    model = IceCreamStore

    form_class = IceCreamStoreUpdateForm

#------------chapter_12_example_13.py--------------

class TitleSearchMixin(object):



    def get_queryset(self):

        # Fetch the queryset from the parent's get_queryset

        queryset = super(TitleSearchMixin, self).get_queryset()



        # Get the q GET parameter

        q = self.request.GET.get("q")

        if q:

            # return a filtered queryset

            return queryset.filter(title__icontains=q)

        # No q is specified so we return queryset

        return queryset



#------------chapter_12_example_14.py--------------

from django.views.generic import ListView



from core.views import TitleSearchMixin

from .models import Flavor



class FlavorListView(TitleSearchMixin, ListView):

    model = Flavor

#------------chapter_12_example_15.py--------------

from django.views.generic import ListView



from core.views import TitleSearchMixin

from .models import Store



class IceCreamStoreListView(TitleSearchMixin, ListView):

    model = Store

#------------chapter_12_example_2.py--------------

from django.core.exceptions import ValidationError



def validate_tasty(value):

    """Raise a ValidationError if the value doesn't start with the

        word 'Tasty'.

    """

    if not value.startswith(u"Tasty"):

        msg = u"Must start with Tasty"

        raise ValidationError(msg)



#------------chapter_12_example_3.py--------------

from django.db import models



from .validators import validate_tasty



class TastyTitleAbstractModel(models.Model):



    title = models.CharField(max_length=255, validators=[validate_tasty])



    class Meta:

        abstract = True



#------------chapter_12_example_4.py--------------

from django.core.urlresolvers import reverse

from django.db import models



from core.models import TastyTitleAbstractModel



class Flavor(TastyTitleAbstractModel):

    slug = models.SlugField()

    scoops_remaining = models.IntegerField(default=0)



    def get_absolute_url(self):

        return reverse("flavors:detail", kwargs={"slug": self.slug})



#------------chapter_12_example_5.py--------------

from django import forms



from core.validators import validate_tasty

from .models import Flavor



class FlavorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(FlavorForm, self).__init__(*args, **kwargs)

        self.fields["title"].validators.append(validate_tasty)

        self.fields["slug"].validators.append(validate_tasty)



    class Meta:

        model = Flavor

#------------chapter_12_example_6.py--------------

from django.contrib import messages

from django.views.generic import CreateView, UpdateView, DetailView



from braces.views import LoginRequiredMixin



from .models import Flavor

from .forms import FlavorForm



class FlavorActionMixin(object):



    model = Flavor

    fields = ('title', 'slug', 'scoops_remaining')



    @property

    def success_msg(self):

        return NotImplemented



    def form_valid(self, form):

        messages.info(self.request, self.success_msg)

        return super(FlavorActionMixin, self).form_valid(form)



class FlavorCreateView(LoginRequiredMixin, FlavorActionMixin,

                            CreateView):

    success_msg = "created"

    # Explicitly attach the FlavorForm class

    form_class = FlavorForm



class FlavorUpdateView(LoginRequiredMixin, FlavorActionMixin,

                            UpdateView):

    success_msg = "updated"

    # Explicitly attach the FlavorForm class

    form_class = FlavorForm



class FlavorDetailView(DetailView):

    model = Flavor

#------------chapter_12_example_7.py--------------

from django import forms

from flavors.models import Flavor



class IceCreamOrderForm(forms.Form):

    """Normally done with forms.ModelForm. But we use forms.Form here

        to demonstrate that these sorts of techniques work on every

        type of form.

    """



    slug = forms.ChoiceField("Flavor")

    toppings = forms.CharField()



    def __init__(self, *args, **kwargs):

        super(IceCreamOrderForm, self).__init__(*args,

                    **kwargs)

        # We dynamically set the choices here rather than

        # in the flavor field definition. Setting them in

        # the field definition means status updates won't

        # be reflected in the form without server restarts.

        self.fields["slug"].choices = [

            (x.slug, x.title) for x in Flavor.objects.all()

        ]

        # NOTE: We could filter by whether or not a flavor

        #       has any scoops, but this is an example of

        #       how to use clean_slug, not filter().



    def clean_slug(self):

        slug = self.cleaned_data["slug"]

        if Flavor.objects.get(slug=slug).scoops_remaining <= 0:

            msg = u"Sorry, we are out of that flavor."

            raise forms.ValidationError(msg)

        return slug

#------------chapter_12_example_8.py--------------

    def clean(self):

        cleaned_data = super(IceCreamOrderForm, self).clean()

        slug = cleaned_data.get("slug", "")

        toppings = cleaned_data.get("toppings", "")



        # Silly "too much chocolate" validation example

        if u"chocolate" in slug.lower() and \

               u"chocolate" in toppings.lower():

            msg = u"Your order has too much chocolate."

            raise forms.ValidationError(msg)

        return cleaned_data

#------------chapter_12_example_9.py--------------

from django.core.urlresolvers import reverse

from django.db import models



class IceCreamStore(models.Model):

    title = models.CharField(max_length=100)

    block_address = models.TextField()

    phone = models.CharField(max_length=20, blank=True)

    description = models.TextField(blank=True)



    def get_absolute_url(self):

        return reverse("store_detail", kwargs={"pk": self.pk})

#------------chapter_13_example_19.py--------------

TEMPLATES = [

    {

        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'APP_DIRS': True,

        'OPTIONS':

            'string_if_invalid': 'INVALID EXPRESSION: %s'

    },

]

#------------chapter_13_example_4.py--------------

from django.core.urlresolvers import reverse

from django.db import models

from .managers import VoucherManager



class Voucher(models.Model):

    """Vouchers for free pints of ice cream."""

    name = models.CharField(max_length=100)

    email = models.EmailField()

    address = models.TextField()

    birth_date = models.DateField(blank=True)

    sent = models.BooleanField(default=False)

    redeemed = models.BooleanField(default=False)



    objects = VoucherManager()

#------------chapter_13_example_6.py--------------

from django.utils import timezone



from dateutil.relativedelta import relativedelta



from django.db import models



class VoucherManager(models.Manager):

    def age_breakdown(self):

        """Returns a dict of age brackets/counts."""

        age_brackets = []

        now = timezone.now()



        delta = now - relativedelta(years=18)

        count = self.model.objects.filter(birth_date__gt=delta).count()

        age_brackets.append(

            {"title": "0-17", "count": count}

        )

        count = self.model.objects.filter(birth_date__lte=delta).count()

        age_brackets.append(

            {"title": "18+", "count": count}

        )

        return age_brackets

#------------chapter_13_example_7.py--------------

from django.views.generic import TemplateView



from .models import Voucher



class GreenfeldRoyView(TemplateView):

    template_name = "vouchers/views_conditional.html"



    def get_context_data(self, **kwargs):

        context = super(GreenfeldRoyView, self).get_context_data(**kwargs)

        context["greenfelds"] = \

                Voucher.objects.filter(name__icontains="greenfeld")

        context["roys"] = Voucher.objects.filter(name__icontains="roy")

        return context

#------------chapter_15_example_10.py--------------

from __future__ import absolute_import # Python 2 only

from jinja2 import Environment



import random



def environment(**options):

    env = Environment(**options)

    env.globals.update({

        # Runs only on the first template load! The three displays below

        #   will all present the same number.

        #   {{ random }} {{ random }} {{ random }}

        'random_once': random.randint(1, 5)

        # Can be called repeated as a function in templates. Each call 

        #   returns a random number:

        #   {{ random() }} {{ random() }} {{ random() }}

        'random': lambda: random.randint(1, 5),

    })

    return env

#------------chapter_15_example_2.py--------------

from __future__ import absolute_import  # Python 2 only



from django.contrib.staticfiles.storage import staticfiles_storage

from django.core.urlresolvers import reverse

from django.template import defaultfilters



from jinja2 import Environment



def environment(**options):

    env = Environment(**options)

    env.globals.update({

        'static': staticfiles_storage.url,

        'url': reverse,

        'dj': defaultfilters

    })

    return env

#------------chapter_15_example_4.py--------------

from django.template import defaultfilters



class DjFilterMixin(object):

    dj = defaultfilters

#------------chapter_15_example_6.py--------------

import random



from advertisements.models import Advertisement as Ad



def advertisements(request):

    count = Advertisement.objects.filter(subject='ice-cream').count()

    ads = Advertisement.objects.filter(subject='ice-cream')

    return {'ad': ads[random.randrange(0, count)]}

#------------chapter_15_example_8.py--------------

import random



from advertisements.models import Advertisement as Ad



def AdvertisementMiddleware(object):



    def process_request(request):

        count = Advertisement.objects.filter(subject='ice-cream').count()

        ads = Advertisement.objects.filter(subject='ice-cream')

        # If necessary, add a context variable to the request object.

        if not hasattr(request, 'context'):

            request.context = {}

        # Don't overwrite the context, instead we build on it.

        request.context.update({'ad': ads[random.randrange(0, count)]})

#------------chapter_16_example_1.py--------------

from django.core.urlresolvers import reverse

from django.db import models



class Flavor(models.Model):

    title = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)

    scoops_remaining = models.IntegerField(default=0)



    def get_absolute_url(self):

        return reverse("flavors:detail", kwargs={"slug": self.slug})

#------------chapter_16_example_2.py--------------



from .models import flavor



class FlavorSerializer(serializers.ModelSerializer):

    class Meta:

        model = flavor

        fields = ('title', 'slug', 'scoops_remaining')

#------------chapter_16_example_3.py--------------

from rest_framework.generics import ListCreateAPIView

from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import Flavor

from .serializers import FlavorSerializer



class FlavorCreateReadView(ListCreateAPIView):

    queryset = Flavor.objects.all()

    serializer_class = FlavorSerializer

    lookup_field = 'slug'



class FlavorReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):

    queryset = Flavor.objects.all()

    serializer_class = FlavorSerializer

    lookup_field = 'slug'

#------------chapter_16_example_4.py--------------

from django.conf.urls import url



from flavors import views



urlpatterns = [

    url(

        regex=r"^api/$",

        view=views.FlavorCreateReadView.as_view(),

        name="flavor_rest_api"

    ),

    url(

        regex=r"^api/(?P<slug>[-\w]+)/$",

        view=views.FlavorReadUpdateDeleteView.as_view(),

        name="flavor_rest_api"

    )

]



#------------chapter_16_example_7.py--------------

"""Called from the project root's urls.py URLConf thus:

        url(r"^api/", include("core.api", namespace="api")),

"""

from django.conf.urls import url



from flavors import views as flavor_views

from users import views as user_views



urlpatterns = [

    # {% url "api:flavors" %}

    url(

        regex=r"^flavors/$",

        view=flavor_views.FlavorCreateReadView.as_view(),

        name="flavors"

    ),

    # {% url "api:flavors" flavor.slug %}

    url(

        regex=r"^flavors/(?P<slug>[-\w]+)/$",

        view=flavor_views.FlavorReadUpdateDeleteView.as_view(),

        name="flavors"

    ),

    # {% url "api:users" %}

    url(

        regex=r"^users/$",

        view=user_views.UserCreateReadView.as_view(),

        name="users"

    ),

    # {% url "api:users" user.slug %}

    url(

        regex=r"^users/(?P<slug>[-\w]+)/$",

        view=user_views.UserReadUpdateDeleteView.as_view(),

        name="users"

    ),

]



#------------chapter_16_example_8.py--------------

from django.http import HttpResponseGone



apiv1_gone_msg = """APIv1 was removed on April 2, 2015. Please switch to APIv3:

<ul>

    <li>

        <a href="https://www.example.com/api/v3/">APIv3 Endpoint</a>

    </li>

    <li>

        <a href="https://example.com/apiv3_docs/">APIv3 Documentation</a>

    </li>

    <li>

        <a href="http://example.com/apiv1_shutdown/">APIv1 shut down notice</a>

    </li>

</ul>

"""



def apiv1_gone(request):

    return HttpResponseGone(apiv1_gone_msg)

#------------chapter_17_example_1.py--------------

from __future__ import absolute_import



from django.views.generic import TemplateView



from .flavors.models import Flavor



class SiteMapView(TemplateView):

    template_name = "sitemap.xml"



    def flavors(self):

        return Flavor.objects.all() 

#------------chapter_19_example_1.py--------------

from django.utils.encoding import python_2_unicode_compatible



@python_2_unicode_compatible  # For Python 3.4 and 2.7

class IceCreamBar(models.Model):

    name = models.CharField(max_length=100)

    shell = models.CharField(max_length=100)

    filling = models.CharField(max_length=100)

    has_stick = models.BooleanField(default=True)



    def __str__(self):

        return self.name

#------------chapter_19_example_3.py--------------



from .models import IceCreamBar



class IceCreamBarAdmin(admin.ModelAdmin):

    list_display = ("name", "shell", "filling",)



admin.site.register(IceCreamBar, IceCreamBarAdmin)

#------------chapter_19_example_4.py--------------

from django.core.urlresolvers import reverse

from django.utils.html import format_html



from icecreambars.models import IceCreamBar



class IceCreamBarAdmin(admin.ModelAdmin):



    list_display = ("name", "shell", "filling",)

    readonly_fields = ("show_url",)



    def show_url(self, instance):

        url = reverse("ice_cream_bar_detail",

                    kwargs={"pk": instance.pk})

        response = format_html("""<a href="{0}">{1}</a>""", url, url)

        return response



    show_url.short_description = "Ice Cream Bar URL"

    # Displays HTML tags

    # Never set allow_tags to True against user submitted data!!!

    show_url.allow_tags = True



admin.site.register(IceCreamBar, IceCreamBarAdmin)

#------------chapter_20_example_2.py--------------

from django.db import models



class IceCreamStore(models.Model):



    owner = models.OneToOneField(settings.AUTH_USER_MODEL)

    title = models.CharField(max_length=255)

#------------chapter_20_example_3.py--------------

from django.contrib.auth.models import AbstractUser

from django.db import models

from django.utils.translation import ugettext_lazy as _



class KarmaUser(AbstractUser):

    karma = models.PositiveIntegerField(verbose_name=_("karma"),

                                            default=0,

                                            blank=True)

#------------chapter_20_example_4.py--------------

#------------chapter_20_example_5.py--------------



from django.conf import settings

from django.db import models



from flavors.models import Flavor



class EaterProfile(models.Model):



    # Default user profile

    # If you do this you need to either have a post_save signal or

    #     redirect to a profile_edit view on initial login.

    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    favorite_ice_cream = models.ForeignKey(Flavor, null=True, blank=True)



class ScooperProfile(models.Model):



    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    scoops_scooped = models.IntegerField(default=0)



class InventorProfile(models.Model):



    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    flavors_invented = models.ManyToManyField(Flavor, null=True, blank=True)





#------------chapter_22_example_12.py--------------

from pytest import raises



from cones.models import Cone



def test_good_choice():

    assert Cone.objects.filter(type='sugar').count() == 1



def test_bad_cone_choice():

    with raises(Cone.DoesNotExist):

        Cone.objects.get(type='spaghetti')

#------------chapter_22_example_2.py--------------

import json



from django.core.urlresolvers import reverse

from django.test import TestCase



from flavors.models import Flavor



class FlavorAPITests(TestCase):



    def setUp(self):

        Flavor.objects.get_or_create(title="A Title", slug="a-slug")



    def test_list(self):

        url = reverse("flavor_object_api")

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(len(data), 1)

#------------chapter_22_example_3.py--------------

import json



from django.core.urlresolvers import reverse

from django.test import TestCase



from flavors.models import Flavor



class DjangoRestFrameworkTests(TestCase):



    def setUp(self):

        Flavor.objects.get_or_create(title="title1", slug="slug1")

        Flavor.objects.get_or_create(title="title2", slug="slug2")



        self.create_read_url = reverse("flavor_rest_api")

        self.read_update_delete_url = \

            reverse("flavor_rest_api", kwargs={"slug": "slug1"})



    def test_list(self):

        response = self.client.get(self.create_read_url)



        # Are both titles in the content?

        self.assertContains(response, "title1")

        self.assertContains(response, "title2")



    def test_detail(self):

        response = self.client.get(self.read_update_delete_url)

        data = json.loads(response.content)

        content = {"id": 1, "title": "title1", "slug": "slug1",

                                            "scoops_remaining": 0}

        self.assertEquals(data, content)



    def test_create(self):

        post = {"title": "title3", "slug": "slug3"}

        response = self.client.post(self.create_read_url, post)

        data = json.loads(response.content)

        self.assertEquals(response.status_code, 201)

        content = {"id": 3, "title": "title3", "slug": "slug3",

                                            "scoops_remaining": 0}

        self.assertEquals(data, content)

        self.assertEquals(Flavor.objects.count(), 3)



    def test_delete(self):

        response = self.client.delete(self.read_update_delete_url)

        self.assertEquals(response.status_code, 204)

        self.assertEquals(Flavor.objects.count(), 1)

#------------chapter_22_example_4.py--------------

from django.contrib.sessions.middleware import SessionMiddleware

from django.test import TestCase, RequestFactory



from .views import cheese_flavors



def add_middleware_to_request(request, middleware_class):

    middleware = middleware_class()

    middleware.process_request(request)

    return request



def add_middleware_to_response(request, middleware_class):

    middleware = middleware_class()

    middleware.process_request(request)

    return request



class SavoryIceCreamTest(TestCase):

    def setUp(self):

        # Every test needs access to the request factory.

        self.factory = RequestFactory()



    def test_cheese_flavors(self):

        request = self.factory.get('/cheesy/broccoli/')

        request.user = AnonymousUser()



        # Annotate the request object with a session

        request = add_middleware_to_request(request, SessionMiddleware)

        request.session.save()



        # process and test the request

        response = cheese_flavors(request)

        self.assertContains(response, "bleah!")

#------------chapter_22_example_5.py--------------

import unittest



import icecreamapi



from flavors.exceptions import CantListFlavors

from flavors.utils import list_flavors_sorted



class TestIceCreamSorting(unittest.TestCase):



    # Set up monkeypatch of icecreamapi.get_flavors()

    @mock.patch.object(icecreamapi, "get_flavors")

    def test_flavor_sort(self, get_flavors):

        # Instructs icecreamapi.get_flavors() to return an unordered list.

        get_flavors.return_value = ['chocolate', 'vanilla', 'strawberry', ]



        # list_flavors_sorted() calls the icecreamapi.get_flavors()

        #   function. Since we've monkeypatched the function,  it will always

        #   return ['chocolate', 'strawberry', 'vanilla', ]. Which the.

        #   list_flavors_sorted() will sort alphabetically

        flavors = list_flavors_sorted()



        self.assertEqual(

            flavors,

            ['chocolate', 'strawberry', 'vanilla', ]



        )

#------------chapter_22_example_6.py--------------

    def test_flavor_sort_failure(self, get_flavors):

        # Instructs icecreamapi.get_flavors() to throw a FlavorError.

        get_flavors.side_effect = icecreamapi.FlavorError()



        # list_flavors_sorted() catches the icecreamapi.FlavorError()

        #   and passes on a CantListFlavors exception.

        with self.assertRaises(CantListFlavors):

            list_flavors_sorted()

#------------chapter_22_example_7.py--------------

    def test_request_failure(self, get)

        """Test if the target site is innaccessible."""

        get.side_effect = requests.exception.ConnectionError()



        with self.assertRaises(CantListFlavors):

            list_flavors_sorted()



    @mock.patch.object(requests, "get")

    def test_request_failure(self, get)

        """Test if we can handle SSL problems elegantly."""

        get.side_effect = requests.exception.SSLError()



        with self.assertRaises(CantListFlavors):

            list_flavors_sorted()

#------------chapter_22_example_8.py--------------

    allow us to run our test suite

    locally.."""



from .base import *



########## TEST SETTINGS

TEST_RUNNER = "discover_runner.DiscoverRunner"

TEST_DISCOVER_TOP_LEVEL = PROJECT_ROOT

TEST_DISCOVER_ROOT = PROJECT_ROOT

TEST_DISCOVER_PATTERN = "test_*"



########## IN-MEMORY TEST DATABASE

DATABASES = {

    "default": {

        "ENGINE": "django.db.backends.sqlite3",

        "NAME": ":memory:",

        "USER": "",

        "PASSWORD": "",

        "HOST": "",

        "PORT": "",

    },

}

#------------chapter_23_example_2.py--------------

import subprocess

import sys



if sys.argv[-1] == 'md2rst':

    subprocess.call('pandoc README.md -o README.rst', shell=True)

...

#------------chapter_26_example_1.py--------------

CSRF_COOKIE_SECURE = True

#------------chapter_26_example_10.py--------------

>>> payment = IceCreamPayment()

>>> IceCreamPayment.objects.get(id=payment.id)

<IceCreamPayment: 1>

>>> payment.uuid

UUID('0b0fb68e-5b06-44af-845a-01b6df5e0967')

>>> IceCreamPayment.objects.get(uuid=payment.uuid)

<IceCreamPayment: 1>

#------------chapter_26_example_3.py--------------



class SpecialForm(forms.Form):

    my_secret = forms.CharField(

            widget=forms.TextInput(attrs={'autocomplete': 'off'}))

#------------chapter_26_example_4.py--------------



class SecretInPublicForm(forms.Form):



    my_secret = forms.CharField(widget=forms.PasswordInput())

#------------chapter_26_example_5.py--------------

from django.conf import settings

from django.db import models



class Store(models.Model):

    title = models.CharField(max_length=255)

    slug = models.SlugField()

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    # Assume 10 more fields that cover address and contact info.

#------------chapter_26_example_6.py--------------



from .models import Store



class StoreForm(forms.ModelForm):



    class Meta:

        model = Store

        # Explicitly specifying the fields we want

        fields = (

            "title", "address_1", "address_2", "email",

            "usstate", "postal_code", "city",

        )

#------------chapter_26_example_7.py--------------

from django.conf import settings

from django.db import models



class Store(models.Model):

    title = models.CharField(max_length=255)

    slug = models.SlugField()

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    co_owners = models.ManyToManyField(settings.AUTH_USER_MODEL)

    # Assume 10 more fields that cover address and contact info.

#------------chapter_26_example_9.py--------------

from django.db import models

from django.utils.encoding import python_2_unicode_compatible



@python_2_unicode_compatible

class IceCreamPayment(models.Model):

    uuid = models.UUIDField(

        db_index=True,

        default=uuid_lib.uuid4,

        editable=False)



    def __str__(self):

        return str(self.pk)

#------------chapter_27_example_1.py--------------

# Used here to illustrate an example only, so don't

# copy this into your project.

logger.error("Internal Server Error: %s", request.path,

    exc_info=exc_info,

    extra={

        "status_code": 500,

        "request": request

    }

)

#------------chapter_27_example_2.py--------------

# Used here to illustrate an example only, so don't

# copy this into your project.

logger.warning("Forbidden (%s): %s",

               REASON_NO_CSRF_COOKIE, request.path,

    extra={

        "status_code": 403,

        "request": request,

    }

)

#------------chapter_27_example_3.py--------------



from django.views.generic import TemplateView



from .helpers import pint_counter



logger = logging.getLogger(__name__)



class PintView(TemplateView):



    def get_context_data(self, *args, **kwargs):

        context = super(PintView, self).get_context_data(**kwargs)

        pints_remaining = pint_counter()

        logger.debug("Only %d pints of ice cream left." % pints_remaining)

        return context

#------------chapter_27_example_4.py--------------

import requests



logger = logging.getLogger(__name__)



def get_additional_data():

    try:

        r = requests.get("http://example.com/something-optional/")

    except requests.HTTPError as e:

        logger.exception(e)

        logger.debug("Could not get additional data", exc_info=True)

        return None

    return r

#------------chapter_27_example_5.py--------------

# of models.py, views.py, or any other

# file where you need to log.

import logging



logger = logging.getLogger(__name__)

#------------chapter_28_example_1.py--------------

from django.db import models



class EventManager(models.Manager):



    def create_event(self, title, start, end, creator):

        event = self.model(title=title,

                            start=start,

                            end=end,

                            creator=creator)

        event.save()

        event.notify_admins()

        return event





#------------chapter_28_example_2.py--------------

from django.conf import settings

from django.core.mail import mail_admins

from django.db import models



from model_utils.models import TimeStampedModel



from .managers import EventManager



class Event(TimeStampedModel):



    STATUS_UNREVIEWED, STATUS_REVIEWED = (0, 1)

    STATUS_CHOICES = (

        (STATUS_UNREVIEWED, "Unreviewed"),

        (STATUS_REVIEWED, "Reviewed"),

    )



    title = models.CharField(max_length=100)

    start = models.DateTimeField()

    end = models.DateTimeField()

    status = models.IntegerField(choices=STATUS_CHOICES,

                                    default=STATUS_UNREVIEWED)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL)



    objects = EventManager()



    def notify_admins(self):

        # create the subject and message

        subject = "{user} submitted a new event!".format(

                        user=self.creator.get_full_name())

        message = """TITLE: {title}

START: {start}

END: {end}""".format(title=self.title, start=self.start,

                        end=self.end)



        # Send to the admins!

        mail_admins(subject=subject,

            message=message,

            fail_silently=False)

#------------chapter_29_example_10.py--------------

from django.core.serializers import get_serializer



from favorites.models import Favorite



favs = Favorite.objects.filter()[:5]



# Get and instantiate the serializer class

# The 'json' can be replaced with 'python' or 'xml'.

# If you have pyyaml installed, you can replace it with

#   'pyyaml'

JSONSerializer = get_serializer("json")

serializer = JSONSerializer()



# open the serialized data file

with open("data.txt") as f:

    serialized_data = f.read()



# deserialize model data into a generator object

#   we'll call 'python data'

python_data = serializer.deserialize(serialized_data)



# iterate through the python_data

for element in python_data:

    # Prints 'django.core.serializers.base.DeserializedObject'

    print(type(element))



    # Elements have an 'object' that are literally instantiated

    #   model instances (in this case, favorites.models.Favorite)

    print(

        element.object.pk,

        element.object.created

    )



#------------chapter_29_example_11.py--------------

import json



from django.core.serializers.json import DjangoJSONEncoder

from django.utils import timezone



data = {"date": timezone.now()}



# If you don't add the DjangoJSONEncoder class then

# the json library will throw a TypeError.

json_data = json.dumps(data, cls=DjangoJSONEncoder)



print(json_data)

#------------chapter_29_example_2.py--------------

from core.views import IceCreamMixin

#------------chapter_29_example_3.py--------------

>>> slugify(u"straße") # German

u"strae"

#------------chapter_29_example_4.py--------------

>>> slugify(u"straße") # Again with German

u"straße"

#------------chapter_29_example_5.py--------------

from django.core.exceptions import ObjectDoesNotExist



class BorkedObject(object):

    loaded = False



def generic_load_tool(model, pk):

    try:

        instance = model.objects.get(pk=pk)

    except ObjectDoesNotExist:

        return BorkedObject()

    instance.loaded = True

    return instance

#------------chapter_29_example_6.py--------------

from django.core.exceptions import MultipleObjectsReturned

from django.core.exceptions import ObjectDoesNotExist

from django.core.exceptions import PermissionDenied



def get_object_or_403(model, **kwargs):

    try:

        return model.objects.get(**kwargs)

    except ObjectDoesNotExist:

        raise PermissionDenied

    except MultipleObjectsReturned:

        raise PermissionDenied

#------------chapter_29_example_7.py--------------



def finance_data_adjudication(store, sales, issues):



    if store.something_not_right:

        msg = "Something is not right. Please contact the support team."

        raise PermissionDenied(msg)



    # Continue on to perform other logic.

#------------chapter_29_example_8.py--------------



# This demonstrates the use of a custom permission denied view. The default

# view is django.views.defaults.permission_denied

handler403 = 'core.views.permission_denied_view'

#------------chapter_29_example_9.py--------------

from django.core.serializers import get_serializer



from favorites.models import Favorite



# Get and instantiate the serializer class

# The 'json' can be replaced with 'python' or 'xml'.

# If you have pyyaml installed, you can replace it with

#   'pyyaml'

JSONSerializer = get_serializer("json")

serializer = JSONSerializer()



favs = Favorite.objects.filter()[:5]



# Serialize model data

serialized_data = serializer.serialize(favs)



# save the serialized data for use in the next example

with open("data.json", "w") as f:

    f.write(serialized_data)



#------------chapter_33_example_2.py--------------

#------------chapter_33_example_4.py--------------



from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import View



from stores.forms import UploadFileForm

from stores.models import Store



def upload_file(request, pk):

    """Simple FBV example"""

    store = get_object_or_404(Store, pk=pk)

    if request.method == 'POST':

        # Don't forget to add request.FILES!

        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():

            store.handle_uploaded_file(request.FILES['file'])

            return redirect(store)

    else:

        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form, 'store': store})

#------------chapter_33_example_5.py--------------



from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import View



from stores.forms import UploadFileForm

from stores.models import Store



class UploadFile(View):

    """Simple CBV example"""

    def get_object(self):

        return get_object_or_404(Store, pk=self.kwargs['pk'])



    def post(self, request, *args, **kwargs):

        store = self.get_object()

        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():

            store.handle_uploaded_file(request.FILES['file'])

            return redirect(store)

        return redirect('stores:file_upload', pk=pk)



    def get(self, request, *args, **kwargs):

        store = self.get_object()

        form = UploadFileForm()

        return render(request, 'upload.html', {'form': form, 'store': store})

#------------chapter_33_example_6.py--------------

import sys



from django.views.debug import technical_500_response



class UserBasedExceptionMiddleware(object):

    def process_exception(self, request, exception):

        if request.user.is_superuser:

            return technical_500_response(request, *sys.exc_info())

#------------chapter_33_example_7.py--------------

ALLOWED_HOSTS = [

    '.djangopackages.com',

    'localhost',  # Ensures we can run DEBUG = False locally

    '127.0.0.1'  # Ensures we can run DEBUG = False locally

]

