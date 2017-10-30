
- Model and form

``` python

from django.db import models
class Comment(models.Model):
 
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=255)
    notes = models.CharField(max_length=255)
 
    def __str__(self):   # __unicode__ on Python 2
        return self.title

class MyCommentForm(models.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'text', 'notes']
```

- View

```python
from django.core.shortcuts import render, redirect
from django import forms
from django.utils import timezone
from myapp.forms import MyCommentForm
def add_model(request):
 
    if request.method == "POST":
        form = MyCommentForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/')
 
    else:
 
        form = MyCommentForm()
 
        return render(request, "my_template.html", {'form': form})
```

- Template

```
<DOCTYPE html>
<html>
<head>
<title>edit</title>
</head>
<body>
 
<form method="post" >
  {% csrf_token %}
  {{form}}
   
  <button type="submit" class="btn btn-default"&gt;Submit</button>
</form>
</body>
</html>
```
