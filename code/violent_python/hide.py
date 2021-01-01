import mechanize
import sys

def hide():
    br = mechanize.Browser()

    br.set_handle_equiv(True)
    # br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_debug_http(True)
    br.set_debug_redirects(True)
    br.set_debug_responses(True)

    br.addheaders = [('User-agent',' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36')]
    br.set_proxies({'http': '223.71.46.234:3128'})

    r = br.open('https://www.github.com/')
    for f in br.forms():
        print(f)

 #   br.select_form(nr=0)
#br.form['wd'] = ""

#    br.submit()
#    brr = br.response().read()

hide()