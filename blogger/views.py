from django.shortcuts import render
from .models import Blog, Post
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
# Create your views here.

def get_blog_list(request):
    blogs = Blog.objects.order_by('title')
    # return HttpResponse(
    #     '<ul>'
    #     + ''.join(['<li><a href="/blogger/%s">%s</a></li>' % (b.id, b.title) for b in blogs])
    #     + '</ul>'
    # )
    context = {'blogs' : blogs}
    #template = loader.get_template('blogger/index.html')
    #return HttpResponse(template.render(context, request))

    return render(request, 'blogger/index.html', context)


def blog(request, blog_id):
    if request.method == 'POST':
        return create_post(request, blog_id)
    return render_blog(request, blog_id)


def render_blog(request, blog_id, additional_context={}):

    blog = get_object_or_404(Blog, id=blog_id)
    

    context = {'blog': blog,
                'posts': blog.post_set.order_by('-created_at'),
                **additional_context
                }
    #template = loader.get_template('blogger/blog.html')
    #return HttpResponse(template.render(context, request))

    return render(request, 'blogger/blog.html', context)



def create_post(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    subject = request.POST['subject']
    subject_error = None
    if not subject or subject.isspace():
        subject_error = 'Please provide non-empty subject!'

    text = request.POST['text']
    text_error = None
    if not text or text.isspace():
        text_error = 'Please provide non-empty text!'

    if subject_error or text_error:
        error_context = {
            'subject_error': subject_error,
            'text_error': text_error,
            'subject': subject,
            'text': text
        }
        return render_blog(request, blog_id, error_context)
    else:
        Post(blog_id=blog.id, subject=subject, text=text).save()
        return HttpResponseRedirect(reverse('blog_by_id', kwargs={'blog_id': blog_id}))