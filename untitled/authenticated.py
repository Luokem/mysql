#coding=utf-8

import json

import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.options
import base64, uuid
import time
from pycket.session import SessionMixin
from tornado.options import options, define


define('post', default=9000, help='post', type=int)

class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        id = self.session.get('user')
        return id if id else None




class Index(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name ="赖志成"
        classs = [
            ("http://www.baidu.com", u"百度"),
            ("http://www.xiaomi.com",u"小米"),
            ("http://www.jd.com",u"京东")
        ]
        html = u'<a href = "www.baidu.com" > 百度 </a>'
        self.render('lesson.html',name=name, classs=classs,time=time,html = html)


class Login(BaseHandler):
    def get(self):
        print "1111"
        self.render('login.html')

    def post(self):
        name = self.get_argument('name','')
        password = self.get_argument('password','')
        if name == '111' and password =='222':
            self.session.set('user', name)
            self.redirect('/index')
        else:
            self.write('登录失败!')



if __name__ == '__main__':
    handlers = [
        (r'/login',Login),
        (r'/index',Index)
    ]



    settings = dict(
        # 配置文件
        template_path ='templates',
        static_path='static',
        debug=True,
        cookie_secret = 'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',
        login_url ='/login',
        xsrf_cookies =True,
        # pycket 的配置信息
        pycket = {
            'engine': 'redis',
            'storage': {
                'host':'localhost',
                'port': 6379,
                'db_sessions': 5,
                'db_notifications':11,
                'max_connections': 2**31,
            },
            'cookies': {
                'expires_days': 30,

            },
        },

    )


    # settings = {
    #     "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E="
    # }

    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers, **settings)
    hettp_server = tornado.httpserver.HTTPServer(app)
    hettp_server.listen(options.post)
    tornado.ioloop.IOLoop.instance().start()
