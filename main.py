#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import memcache, users

from keys import KEY

CACHE_TIME = 60 * 60 # 1 hour

import cookielib            
import os
import urllib2

class MainHandler(webapp.RequestHandler):
    def get(self):
    
        user = users.get_current_user()
        if not user:
            login_url = users.create_login_url('/')
            self.redirect(login_url)
            return
    
        page = memcache.get("page")
        if page is not None:
            self.response.out.write("<font color='white'>HIT</font>"+page)
        else:               
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
            theurl = KEY
            txdata = None    
            txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'} 
            
            try:
                req = urllib2.Request(theurl, txdata, txheaders)       
                handle = urllib2.urlopen(req)                             
            except IOError, e:
                print 'We failed to open "%s".' % theurl
                if hasattr(e, 'code'):
                    print 'We failed with error code - %s.' % e.code
                elif hasattr(e, 'reason'):
                    print "The error object has the following 'reason' attribute :", e.reason
                    print "This usually means the server doesn't exist, is down, or we don't have an internet connection."
                    sys.exit() 
            else:
                page = handle.read()
                memcache.add("page", page, CACHE_TIME)
                self.response.out.write("<font color='white'>MISS</font>"+page)
            

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
