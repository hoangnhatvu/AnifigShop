from django.shortcuts import render,redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.models import UserProfile
# Create your views here.

@login_required(login_url='login')
def ContactView(request):
    user_profile = UserProfile.objects.get(user_id=request.user.id)
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
    context = {
            'user_profile': user_profile,
        }
    return render(request, 'contact/contact.html', context=context)