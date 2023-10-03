from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic.edit import FormView
from django.contrib import messages

from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView,
    #DeleteView
)
from .forms import (
    ContactForm,
    VehicleForm,
    #ProspectiveBuyerForm,
    # ProspectiveBuyerFormSet
)

from chapter_3.models import (
    #Seller,
    Vehicle,
    #Engine,
    #VehicleModel
)
from django.conf import settings
# Create your views here.

class FormClassView(FormView):
    '''
    Form View for ContactForm
    '''
    template_name = 'chapter_7/form-class.html'
    form_class = ContactForm
    success_url = '/chapter-7/contact-form-success/'

    #def get_success_url(self, **kwargs):
    #    return reverse('pattern_name', args=(value,))

    def get(self, request, *args, **kwargs):
        '''
        GET Response Method
        '''
        initial = {
            'full_name': 'FirstName LastName',
            'email_1': 'example1@example.com',
            'email_2': 'example2@example.com',
            'email_3': 'example3@example.com',
            'conditional_required': 'My Required Value',
            'multiple_emails': 'example4@example.com,example5@example.com,example6@example.com',
            'message': 'My Message',
        }

        return TemplateResponse(request, self.template_name, {
            'title': 'FormClassView Page',
            'page_id': 'form-class-id',
            'page_class': 'form-class-page',
            'h1_tag': 'This is the FormClassView Page Using ContactForm',
            'form': self.form_class(initial),
        })

    def post(self, request, *args, **kwargs):
        '''
        POST Response Method
        '''
        #return redirect(self.success_url)
        form = self.form_class(request.POST)

        if form.is_valid():
            messages.add_message(
                request,
                messages.SUCCESS,
                'Your contact form submitted successfully',
                extra_tags = 'bold',
                fail_silently = True
            )
            #messages.success(
            #    request,
            #    'Your contact form submitted successfully',
            #    extra_tags = 'bold',
            #    fail_silently = True
            #)
            #messages.add_message(
            #    request,
            #    settings.CRITICAL,
            #    'This is critical!'
            #)

            #return HttpResponseRedirect(self.success_url)

            context = {
                'title': 'FormClassView Page',
                'page_id': 'form-class-id',
                'page_class': 'form-class-page',
                'h1_tag': 'This is the FormClassView Page Using ContactForm',
                'form': form,
            }
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'There was a problem submitting your contact form.<br />Please review the ' \
                    'highlighted fields below.',
                fail_silently = True
            )
            #messages.error(
            #    request,
            #    'There was a problem submitting your contact form.<br />Please review the ' \
            #        'highlighted fields below.',
            #    fail_silently = True
            #)

            context = {
                'title': 'FormClassView Page - Please Correct The Errors Below',
                'page_id': 'form-class-id',
                'page_class': 'form-class-page errors-found',
                'h1_tag': 'This is the FormClassView Page Using ContactForm<br /><small ' \
                    'class="error-msg">Errors Found</small>',
                'form': form,
            }

        #form.send_email(request)
        form.send_email(request)
        return TemplateResponse(request,self.template_name,context)
        #form.generate_pdf(request)

        return TemplateResponse(request, self.template_name, context)
