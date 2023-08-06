=======
thwterm
=======

thwterm is a simple web shell to connect to thhpc cluster through web 

thwterm used in iframe in django template

detail documentation is in the "docs" directory

Quick start

-----------

1. pip install django-thwterm

2. Add "thwterm" to your INSTALLED_APPS setting like this::

    INSTALL_APPS = [
        ...
        'thwterm',
    ]

3. Include the thwterm URLconf in your project urls.py like this::
    
    from thwterm import urls as thWTermUrls
    urlpatterns = [...] + thWTermUrls.urlpatterns,

4. Add the thwterm in your html tempalte by iframe like this:
    
	1)、add path in project urls like this:
	    path('xterm/', main.xTerm),
	2)、in main views.py:
	    @login_required
        def xTerm(request):
            return render(request,"xterm.html",{})
	3)、write the xterm.html tempalte file like:
	    ...
		<div class="page-row">
            <iframe id="webterminaliframe" src="/thwterm/" frameborder="0" width="100%" height="100vh" style="height: 80vh" scrolling="no"></iframe>
		</div>
		...
		
5. setup thuri appid and appid in settings.py like this；
	TH_WEBTERM_CONFIG = {
        'WTERM_BACKEND_HOST':'{ visual<shell> backend server }',
        'WTERM_BACKEND_APPID':'{appid}',
        'WTERM_BACKEND_APPKEY':'{appkey}'}
	
6. add th user and cluster to session when user login like this:
    request.session["systemUsername"] = "{thsystem user name}"
    request.session["cluster] = "thcluster1"
	
7. Start the development server and visit http://yourhost:port/xterm/ you will see the web term