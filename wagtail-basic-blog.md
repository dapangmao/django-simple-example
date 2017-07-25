- Issue #1: tag will be a blog page nested under the blog-index-page
- Issue #2: use Wagtail models directly
![demo](https://github.com/dapangmao/django-simple-example/blob/master/images/Screen%20Shot%202017-07-25%20at%2010.27.23%20AM.png?raw=true)

- 5 models

```python
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel('intro', classname="full")]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey("BlogPage", related_name="tagged_items")


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        return None

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body")
    ]

    content_panels = Page.content_panels + [

        MultiFieldPanel([
            FieldPanel("date"),
            FieldPanel("tags"),

        ], heading="Blog information"),

        FieldPanel("intro"),
        FieldPanel("body", classname="full"),
        InlinePanel("gallery_images", label="Gallery images"),
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, related_name="gallery_images")
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name="+")
    caption = models.CharField(blank=True, max_length=250)

    panels = [ImageChooserPanel('image'), FieldPanel('caption')]


class BlogTagIndexPage(Page):
    def get_context(self, request, *args, **kwargs):
        tag = request.GET.get("tag")
        blogpages = BlogPage.objects.filter(tags__name=tag)
        context = super(BlogTagIndexPage, self).get_context(request)
        context["blogpages"] = blogpages
        return context

```

- 3 templates


    - blog_index_page
    ```
    {%  extends "base.html" %}

    {% load wagtailcore_tags wagtailimages_tags %}


    {%  block content %}
        <h1> {{ page.title }}</h1>

        <div class="intro"> {{ page.intro| richtext }}</div>
        {% for post in page.get_children %}
            {% with post=post.specific %}
                <h2><a href="{% pageurl post %}">{{ post.title }}</a></h2>

                {% with post.main_image as main_image %}
                    {% if main_image %}{% image main_image fill-160x100 %}{% endif %}
                {% endwith %}

                <p>{{ post.intro }}</p>
            {% endwith %}
        {% endfor %}

    {% endblock %}
    ```
    
    - blog_page
    ```
    {% extends "base.html" %}

    {% load wagtailcore_tags wagtailimages_tags%}

    {% block content %}

        <h1>{{ page.title }}</h1>
        <p class="meta">{{ page.date }}</p>

        {% if page.tags.all.count %}
            <div class="tags">
                <h3>Tags</h3>
                {% for tag in page.tags.all %}
                    <a href="{% slugurl 'tags' %}?tag={{ tag }}">
                        <button type="button">{{ tag }}</button>
                    </a>
                {% endfor %}
            </div>
        {% endif %}

        <div class="intro">{{ page.intro }}</div>

        {{ page.body|richtext }}

        {% for item in page.gallery_images.all %}
            <div style="float: left; margin: 10px;">
                {% image item.image fill-320x240%}
                <p>{{ item.caption }}</p>

            </div>
        {% endfor %}

        <p><a href="{{ page.get_parent.url }}">Return to blog</a></p>

    {% endblock %}
    ```
    
    - blog_tag_index_page
    ```
    {% extends "base.html" %}

    {% load wagtailcore_tags %}

    {% block content %}

        {% if request.GET.tag %}
            <h4>Showing pages tagged " {{ request.GET.tag }} "</h4>
        {% endif %}

        {% for blogpage in blogpages %}
            <p>
                <strong><a href="{% pageurl blogpage %}">
                    {{ blogpage.title }}

                </a> </strong>
                <br/>

                <small>Revised:
                    {{ blogpage.date }}
                </small>

                {% if blogpage.author %}
                    <br/>
                    {% if blogpage.author %}
                        <p>
                            By {{ blogpage.author.profile }}

                        </p>
                    {% endif %}
                {% endif %}

            </p>
        {% endfor %}
    {% endblock %}
    ```
