#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch, memcache 

from keys import USERNAME, PASSWORD


post_with_params = "username=" + USERNAME + "&password=" + PASSWORD + "&remember=T&submit=L&timezone=-8&nextPage=&browser=Chrome&browserVersion=5,&os=Mac&validation={'validators':[{'name':'username','func':'isNotEmpty','type':'inline','copy':'Please enter your email address.'},{'name':'username','func':'isEmail','type':'inline','copy':'email address must be a valid email.'},{'name':'password','func':'isNotEmpty','type':'inline','copy':'Please enter your password.'}],'validatorn':2}"

def get_money_from_mint():
    money = memcache.get("money")
    if not money:
        money = 10
        header = urlfetch.fetch("https://wwws.mint.com/login.event").headers
        response_after_login = urlfetch.fetch("https://wwws.mint.com/loginUserSubmit.xevent",method='POST', follow_redirects=False, payload=post_with_params, headers=header)
        return str(response_after_login.headers) + "////" + str(response_after_login.content)
#        memcache.set("money", money, 3600)
    return money


class MainHandler(webapp.RequestHandler):
    def get(self):
        money = get_money_from_mint()
        self.response.out.write('Money in the bank:!' + str(money))


def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
