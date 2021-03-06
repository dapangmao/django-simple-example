## Pros
- minimal lines of Python
- only need to work with models.py and its corresponding HTML templates
- define the search scope
- resize the images automatically

### Blog example

- use the `streamblock` instead of `richtext` [BaseStreamBlock](https://github.com/wagtail/bakerydemo/blob/master/bakerydemo/base/blocks.py#L53)
    ![demo](https://github.com/dapangmao/django-simple-example/blob/master/images/streamblock.PNG?raw=true)
- the index page will be narrowed by the tag 


```python
from __future__ import unicode_literals

from django.contrib import messages
from django.db import models
from django.shortcuts import redirect, render

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from taggit.models import Tag, TaggedItemBase

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from bakerydemo.base.blocks import BaseStreamBlock


class BlogPeopleRelationship(Orderable, models.Model):
    """
    This defines the relationship between the `People` within the `base`
    app and the BlogPage below. This allows People to be added to a BlogPage.

    We have created a two way relationship between BlogPage and People using
    the ParentalKey and ForeignKey
    """
    page = ParentalKey(
        'BlogPage', related_name='blog_person_relationship'
    )
    people = models.ForeignKey(
        'base.People', related_name='person_blog_relationship'
    )
    panels = [
        SnippetChooserPanel('people')
    ]


class BlogPageTag(TaggedItemBase):
    """
    This model allows us to create a many-to-many relationship between
    the BlogPage object and tags. There's a longer guide on using it at
    http://docs.wagtail.io/en/latest/reference/pages/model_recipes.html#tagging
    """
    content_object = ParentalKey('BlogPage', related_name='tagged_items')


class BlogPage(Page):
    """
    A Blog Page

    We access the People object with an inline panel that references the
    ParentalKey's related_name in BlogPeopleRelationship. More docs:
    http://docs.wagtail.io/en/latest/topics/pages.html#inline-models
    """
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )
    subtitle = models.CharField(blank=True, max_length=255)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    date_published = models.DateField(
        "Date article published", blank=True, null=True
        )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle', classname="full"),
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        FieldPanel('date_published'),
        InlinePanel(
            'blog_person_relationship', label="Author(s)",
            panels=None, min_num=1),
        FieldPanel('tags'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('body'),
    ]

    def authors(self):
        """
        Returns the BlogPage's related People. Again note that we are using
        the ParentalKey's related_name from the BlogPeopleRelationship model
        to access these objects. This allows us to access the People objects
        with a loop on the template. If we tried to access the blog_person_
        relationship directly we'd print `blog.BlogPeopleRelationship.None`
        """
        authors = [
            n.people for n in self.blog_person_relationship.all()
        ]

        return authors

    @property
    def get_tags(self):
        """
        Similar to the authors function above we're returning all the tags that
        are related to the blog post into a list we can access on the template.
        We're additionally adding a URL to access BlogPage objects with that tag
        """
        tags = self.tags.all()
        for tag in tags:
            tag.url = '/'+'/'.join(s.strip('/') for s in [
                self.get_parent().url,
                'tags',
                tag.slug
            ])
        return tags

    # Specifies parent to BlogPage as being BlogIndexPages
    parent_page_types = ['BlogIndexPage']

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    subpage_types = []


class BlogIndexPage(RoutablePageMixin, Page):
    """
    Index page for blogs.
    We need to alter the page model's context to return the child page objects,
    the BlogPage objects, so that it works as an index page

    RoutablePageMixin is used to allow for a custom sub-URL for the tag views
    defined above.
    """
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
    ]

    # Speficies that only BlogPage objects can live under this index page
    subpage_types = ['BlogPage']

    # Defines a method to access the children of the page (e.g. BlogPage
    # objects). On the demo site we use this on the HomePage
    def children(self):
        return self.get_children().specific().live()

    # Overrides the context to list all child items, that are live, by the
    # date that they were published
    # http://docs.wagtail.io/en/latest/getting_started/tutorial.html#overriding-context
    def get_context(self, request):
        context = super(BlogIndexPage, self).get_context(request)
        context['posts'] = BlogPage.objects.descendant_of(
            self).live().order_by(
            '-date_published')
        return context

    # This defines a Custom view that utilizes Tags. This view will return all
    # related BlogPages for a given Tag or redirect back to the BlogIndexPage.
    # More information on RoutablePages is at
    # http://docs.wagtail.io/en/latest/reference/contrib/routablepage.html
    @route('^tags/$', name='tag_archive')
    @route('^tags/(\w+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):

        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no blog posts tagged with "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        posts = self.get_posts(tag=tag)
        context = {
            'tag': tag,
            'posts': posts
        }
        return render(request, 'blog/blog_index_page.html', context)

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)

    # Returns the child BlogPage objects for this BlogPageIndex.
    # If a tag is used then it will filter the posts by tag.
    def get_posts(self, tag=None):
        posts = BlogPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    # Returns the list of Tags for all child posts of this BlogPage.
    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            # Not tags.append() because we don't want a list of lists
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags
```

#### Key templates

- base.html

    - disect the HTML to many smaller `include` parts
    - just use CSS to implement the effects
```
{% load navigation_tags static wagtailuserbar %}

{% block head %}
    {% include "includes/head.html" %}
{% endblock head %}

<body class="{% block body_class %}template-{{ self.get_verbose_name|slugify }}{% endblock %}">
{% wagtailuserbar %}

{% block header %}
    {# Header contains the main_navigation block #}
    {% include "includes/header.html" with parent=site_root calling_page=self %}
{% endblock header %}

{% block head-extra %}
{% endblock head-extra %}

{% block messages %}
    {% include "includes/messages.html" %}
{% endblock messages %}


{% block breadcrumbs %}
{#     breadcrumbs is defined in base/templatetags/navigation_tags.py#}
    {% breadcrumbs %}
{% endblock breadcrumbs %}

<content role="main">
    {% block content %}
    {% endblock content %}
</content>

    <hr>

    <!-- Footer -->
    <footer>
        {% include "includes/footer.html" %}
    </footer>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

</body>

</html>

```


- blog_index_page.html

    - also cover the tag index page as well
    
    
    
```html
{% extends "base.html" %}
{% load wagtailcore_tags navigation_tags wagtailimages_tags %}

{% block content %}
    {% include "base/include/header-index.html" %}

    <div class="container">
        {% if tag %}
            <div class="row">
                <div class="col-md-12">
                    <p>Viewing all blog posts by <span class="outline">{{ tag }}</span></p>
                </div>
            </div>
        {% endif %}

        {% if page.get_child_tags %}
            <ul class="blog-tags tags list-inline">
                {% for tag in page.get_child_tags %}
                    <li><a href="{{ tag.url }}">{{ tag }}</a></li>
                {% endfor %}
            </ul>
        {% endif %}

        <div class="row row-eq-height blog-list">
            {% if posts %}
                {% for blog in posts %}
                    <li class="col-xs-12 col-sm-6 col-md-3 blog-list-item">
                        <a href="{% pageurl blog %}">
                            <div class="image">
                                {% image blog.image fill-850x450-c50 as image %}
                                <img src="{{ image.url }}" width="{{ image.width }}" height="{{ image.height }}" alt="{{ image.alt }}" class="" />
                            </div>
                            <div class="text">
                                <h2 class="blog-list-title">{{ blog.title }}</h2>
                                <p>{{ blog.introduction|truncatewords:15 }}</p>
                            </div>
                            <div class="small footer">
                                {% if blog.date_published %}
                                    {{ blog.date_published }} by 
                                {% endif %}
                                {% for author in blog.authors %}
                                    {{ author }}{% if not forloop.last %}, {% endif %}
                                {% endfor %}
                            </div>
                        </a>
                    </li>
                {% endfor %}
            {% else %}
                <div class="col-md-12">
                    <p>Oh, snap. Looks like we were too busy baking to write any blog posts. Sorry.</p>
                </div>
            {% endif %}
        </div>
    </div>
{% endblock content %}
```

- blog_page.html
```html
{% extends "base.html" %}
{% load navigation_tags wagtailimages_tags %}

{% block content %}

    {% image self.image fill-1920x600 as hero_img %}
        {% include "base/include/header-hero.html" %}

    <div class="container">
        <div class="row">
            <div class="col-md-8">
                {% if page.introduction %}
                    <p class="intro">{{ page.introduction }}</p>
                {% endif %}

                <div class="blog-meta">
                    {% if page.authors %}
                        <div class="blog-avatars">
                            {% for author in page.authors %}
                                <div class="author">{% image author.image fill-50x50-c100 class="blog-avatar" %}
                                    {{ author.first_name }} {{ author.last_name }}</div>
                            {% endfor %}
                        </div>
                    {% endif %}

                    {% if page.date_published %}
                        <div class="blog-byline">
                            {{ page.date_published }}
                        </div>
                    {% endif %}
                </div>

                {{ page.body }}

                {% if page.get_tags %}
                    Tagged with:<br />
                    {% for tag in page.get_tags  %}
                        <a href="{{ tag.url }}" class="btn btn-sm">{{ tag }}</a>
                    {% endfor %}
                {% endif %}
            </div>
        </div>
    </div>
{% endblock content %}
```

- header.html
```html
{% load navigation_tags %}

<div class="header clearfix" role="banner">
    <div class="container">
        <div class="row">
            <div class="col-lg-12">
                <a href="/" class="logo">I am the Wagtail Bakery</a>
                    <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#main-navigation" aria-label="Mobile menu" aria-expanded="false">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>

                <form action="/search" method="get" class="search" _lpchecked="1" role="search">
                    <input name="q" type="text" placeholder="Search the site" id="" aria-label="Search the site" autocomplete="off">
                    <a href="#" class="search-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 451 451"><path d="M447.05 428l-109.6-109.6c29.4-33.8 47.2-77.9 47.2-126.1C384.65 86.2 298.35 0 192.35 0 86.25 0 .05 86.3.05 192.3s86.3 192.3 192.3 192.3c48.2 0 92.3-17.8 126.1-47.2L428.05 447c2.6 2.6 6.1 4 9.5 4s6.9-1.3 9.5-4c5.2-5.2 5.2-13.8 0-19zM26.95 192.3c0-91.2 74.2-165.3 165.3-165.3 91.2 0 165.3 74.2 165.3 165.3s-74.1 165.4-165.3 165.4c-91.1 0-165.3-74.2-165.3-165.4z"></path></svg>
                    </a>
                </form>

                {% block main_navigation %}
                    <nav class="collapse navbar-collapse" id="main-navigation" role="navigation" aria-label="Primary site navigation">
                        <ul class="nav nav-pills">
                            {# main_menu is defined in base/templatetags/navigation_tags.py #}
                            {% get_site_root as site_root %}
                            {% top_menu parent=site_root calling_page=self %}
                        </ul>
                    </nav>
                {% endblock %}
            </div>
        </div>
    </div>
</div>

```
