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

4. Set IFrame Option in settings.py like this:
    X_FRAME_OPTIONS = 'ALLOWALL'

5. Add the thwterm in your html tempalte by iframe like this:
    
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
		
6. Setup thuri appid and appid in settings.py like this；
	TH_WEBTERM_CONFIG = {
        'WTERM_BACKEND_HOST':'{ visual<shell> backend server }',
        'WTERM_BACKEND_APPID':'{appid}',
        'WTERM_BACKEND_APPKEY':'{appkey}'}
	
7. Add th user and cluster to session when user login like this:
    request.session["systemUsername"] = "{thsystem user name}"
    request.session["cluster] = "thcluster1"

8. Use nginx proxy the porject port like this:
     server {
        listen       80;
        server_name  _;
		
		port_in_redirect off;

        location /visual/ {
            proxy_pass { visualbackend server }

            proxy_http_version 1.1;
            proxy_read_timeout 600s;
            proxy_redirect off;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host:$server_port;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header REMOTE-HOST $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			
        }

        location / {
            proxy_set_header  Host  $host;
            proxy_set_header  X-real-ip $remote_addr;
            proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass { django server:port };
			
        }
	
9. Start the development server and visit http://yourhost:port/xterm/ you will see the web term