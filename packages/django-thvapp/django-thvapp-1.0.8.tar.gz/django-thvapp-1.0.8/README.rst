=======
thvapp
=======

thvapp is a remote visual application plugin to th system on novnc  

thvapp used in iframe in django template

detail documentation is in the "docs" directory

Quick start

-----------

1. pip install django-thvapp

2. Add "thvapp" to your INSTALLED_APPS setting like this::

    INSTALL_APPS = [
        ...
        'thvapp',
    ]

3. Include the thvapp URLconf in your project urls.py like this::
    
    from thvapp import urls as thVAppsUrls
    urlpatterns = [...] + thVAppsUrls.urlpatterns,

4. Set IFrame Option in settings.py like this:
    X_FRAME_OPTIONS = 'ALLOWALL'

5. Add the thvapp in your html tempalte by iframe like this:
    
    1)、add path in project urls like this:
        path('vapps/', main.vApps),
    2)、in main views.py:
        @login_required
        def vApps(request):
		
		  return render(request,'vapps.html',{})
    3)、write the xterm.html tempalte file like:
        ...
        <div class="page-row"><iframe id="webthvisual" src="/thva/apps#/applist" frameborder="0" width="100%" style="min-height: 82vh" scrolling="yes"></iframe>
        </div>
        ...

6. Setup thuri appid and appid in settings.py like this；
    THTERMCONF = {
        'server':'{ visual<shell> backend server }',
        'appid':'{appid}',
        'appkey':'{appkey}'
		
    }
    TH_VISUALAPP_CONFIG = {
        
		'VAPP_BACKEND_HOST':'{ visualbackend server }',
		
        'VAPP_BACKEND_APPID':'{ appid }',
		
        'VAPP_BACKEND_APPKEY':'{appkey}',
		
        'VAPP_DEFAULT_IMGAGE_URL':'/media/visual.png', # default image url in front page 
        'FOOTER_HEIGHT':70,  # your iframe's parent page's footer height
        'SCREEN_RATIO':16 / 9,  # if you want to set the remote screen ratio
        'VAPP_ICONS':{
		
            '{thcluster1}':{"app1": {"video": "app1 image url"}, "app2": {"video": "{app2 video url}"}, ...}
        
		} # vapp icons (image or video) you can get th visual applications from THVisual client SDK then config your own icons in settings or database
    
	}
    
7. Add th user 、cluster and visual applications' icons to session when user login like this:
    request.session["systemUsername"] = "{thsystem user name}"
    request.session["cluster] = "{thcluster1}"
    request.session["vapp_icons"] = json.dumps(settings.TH_VISUALAPP_CONFIG.get('VAPP_ICONS'))
	
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
    
9. Start the development server and visit http://yourhost:80/vapps/ you will see the web term