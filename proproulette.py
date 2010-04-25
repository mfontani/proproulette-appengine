import cgi
import os
import random
import logging
import inspect
from xml.dom import minidom
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import memcache

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def get_last_20_props():
    """get_last_20_props()

    Checks the cache to see if the XML has already been fetched.
    If not, fetches it from s1homes.

    Returns:
        XML list of last 20 properties for sale
    """
    last20props = memcache.get("last20props")
    if last20props is not None:
        #logging.info("Got last 20 props in cache!")
        return last20props
    else:
        #logging.info("No cache for last 20 props, fetching")
        last20props = urlfetch.fetch("http://www.s1homes.com/forsale_search_results.cgi?bp=1")
        #last20props = urlfetch.fetch("http://127.0.0.1:81/props.txt")
        if last20props.status_code != 200:
            logging.error("status_code not 200: %s" % last20props.status_code)
            return ""
        if not memcache.add("last20props", last20props.content, 3600):
            logging.error("Memcache set failed")
        return last20props.content

class MainPage(webapp.RequestHandler):
    def get(self):
        username = ''
        if users.get_current_user():
            username = users.get_current_user().nickname()
        last20props = get_last_20_props()
        dom = minidom.parseString(last20props)
        nprop = random.randint(0,9)
        randomurl = getText( dom.getElementsByTagName("link")[ nprop ].childNodes )
        #logging.info("random nprop: %s" % nprop )
        #logging.info("random url: %s" % randomurl )
        template_values = {
                'username': username,
                'randomurl': randomurl,
                }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
        dom.unlink()

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

