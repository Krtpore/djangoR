from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import translation
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
import hashlib
import hmac


def page404(request, exception):
    return render(request, 'main/page404.html')

def main(request):
    return render(request, 'main/main.html')

def news(request):
    return render(request, 'main/news.html')

def user(request):
    return render(request, 'main/user.html')

def navbar(request):
    return render(request, 'main/navbar.html')

def about(request):
    return render(request, 'main/about.html')

def base(request):
    return render(request, 'main/base.html')

def news_example(request):
    return render(request, 'main/news_example.html')

def selectlanguage(request):
    #в 25 символов входит корневой катлого + код языка из двух букв + '/'
    url = request.META.get('HTTP_REFERER')[38:]
    # print('URL:',url)
    if request.method =='POST':
        current_language = translation.get_language()
        # print('До:',current_language)
        lang = request.POST.get('language')
        translation.activate(lang)
        # print('После:',translation.get_language())
        response = HttpResponse('')
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        # print('/'+lang+'/'+url)
        return HttpResponseRedirect('/'+lang+'/'+url)

def first_redirect(request):
    return redirect('main')

import git
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
@csrf_exempt
def update_server(request):
    header_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
    verify_signature(request.body,settings.GITHUB_WEBHOOK_KEY,header_signature)
    if request.method == "POST":
        local_dir = '/home/eh0388pe/djangoR'
        repo = git.Repo(local_dir)
        repo.remotes.origin.pull()
        return HttpResponse('server updated')
    else:
        return HttpResponse("Вы попали не туда")

from django.http import HttpResponseServerError
def verify_signature(payload_body, secret_token, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        return HttpResponseServerError("x-hub-signature-256 header is missing!", status_code=403)
    hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        return HttpResponseServerError("Request signatures didn't match!", status_code=403)