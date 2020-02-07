from django.shortcuts import render
from django.http import StreamingHttpResponse
from mylib.joe_rogan import joe_rogan

from django.template import Template, Context

# template = Template(
#     '''
#     {% extends "django_project/base.html" %}
#     {% block content %}
#     <ul>
#       <li>{{ quote }}</li>
#     </ul>
#     {% endblock content %}
#     '''
# )

template = Template(
    '''
    <ul>
      <li>{{ quote }}</li>
    </ul>
    '''
)


def home(request):
    def quote_generator():
        for quote in joe_rogan.joe_rogan_quote_generator():
            c = Context({'quote': quote})
            yield template.render(c)
            
            # yield render(request, 'joe_rogan/home.html', context=c.flatten())

    return StreamingHttpResponse(quote_generator())
