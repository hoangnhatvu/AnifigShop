from django.shortcuts import render,redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from account.models import Account
# Create your views here.
def ContactView(request):
    if request.method == 'POST':
        mail_subject = 'Phản hồi từ khách hàng'
        message = render_to_string('contact/contact_mail.html', {
            'name':request.POST.get('name'),
            'email':request.POST.get('email'),
            'phone':request.POST.get('phone'),
            'content': request.POST.get('message')
        })
        send_email = EmailMessage(mail_subject, message, to=['hoangnhatvu350800@gmail.com'])
        send_email.send()
        messages.success(
            request=request,
            message="Cảm ơn bạn đã liên hệ với chúng tôi!"
        )
        return redirect('contact')
    return render(request, 'contact/contact.html')