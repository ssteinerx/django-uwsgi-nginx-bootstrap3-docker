# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.storage import default_storage

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages

from django.http import HttpResponse
from django.shortcuts import render
import requests
import json

from .forms import ContactForm, FilesForm, ContactFormSet


# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, 'dummy.txt')


class HomePageView(TemplateView):
    template_name = 'demo/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, 'hello http://example.com')
        return context


class DefaultFormsetView(FormView):
    template_name = 'demo/formset.html'
    form_class = ContactFormSet


class DefaultFormView(FormView):
    template_name = 'demo/form.html'
    form_class = ContactForm

    def getopenid(request):
        appid= 'wx0ebe45ac16ee690b'
        appsecret= 'd4624c36b6795d1d99dcf0547af5443d'
        code = request.GET['code']
        state = request.GET['state']
        if code:
            url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=' + appid + '&secret=' + appsecret + \
                  '&code='+code + '&grant_type=authorization_code'
            try:
                resp = requests.get(url)
            except:
                return HttpResponse('get access_token failed')
            atdata = json.loads(resp.content)
            at = atdata['access_token']
            oid = atdata['openid']
            return HttpResponse(oid)
        else:
            form = ContactForm()
            return render(request, 'demo/form.html', {'form': form})



    def index(request):
        if request.method == 'POST':# 当提交表单时
            form = ContactForm(request.POST) # form 包含提交的数据

            if form.is_valid():# 如果提交的数据合法
                a = form.cleaned_data['num1']
                b = form.cleaned_data['num2']
                return HttpResponse(str(int(a) + int(b)))
        else:
            form = ContactForm()
            return render(request, 'demo/form.html', {'form': form})



class DefaultFormByFieldView(FormView):
    template_name = 'demo/form_by_field.html'
    form_class = ContactForm


class FormHorizontalView(FormView):
    template_name = 'demo/form_horizontal.html'
    form_class = ContactForm


class FormInlineView(FormView):
    template_name = 'demo/form_inline.html'
    form_class = ContactForm


class FormWithFilesView(FormView):
    template_name = 'demo/form_with_files.html'
    form_class = FilesForm

    def get_context_data(self, **kwargs):
        context = super(FormWithFilesView, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'vertical')
        return context

    def get_initial(self):
        return {
            'file4': fieldfile,
        }


class PaginationView(TemplateView):
    template_name = 'demo/pagination.html'

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        lines = []
        for i in range(200):
            lines.append('Line %s' % (i + 1))
        paginator = Paginator(lines, 10)
        page = self.request.GET.get('page')
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_lines = paginator.page(paginator.num_pages)
        context['lines'] = show_lines
        return context


class MiscView(TemplateView):
    template_name = 'demo/misc.html'
