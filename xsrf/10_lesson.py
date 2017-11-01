#coding=utf-8
import time

import tornado.httpserver                         #tornado.服务器
import tornado.web                                #RequestHandler,Application
import tornado.ioloop                             #tornado.循环
import tornado.options			                  #options解析器
from tornado.options import options,define	      #options端口,define定义
from pycket.session import SessionMixin           #会话库

define('port',default=9000,help='port',type=int)


class BaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self):
        id = self.session.get("user")
        return id if id else None


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def aa(self):
        return u"我是张三"
    def get(self):
        bb = [
            ('http://www.baidu.com', u"百度"),
            ('http://www.sohu.com', u"新浪"),
            ('http://www.163.com', u"网易")
        ]
        self.render(
                    '10_lesson_base.html',
                    name=self.current_user,
                    time=time,
                    bb=bb
                    )



class Jisun(object):
    def sub(self,a,b):
        return a-b

class Index1Handler(BaseHandler):
    @tornado.web.authenticated
    def aa(self):
        return '我是钟老师'
    def get(self):
        self.render('10_lesson_base.html',aa=self.aa,Jisun=Jisun)


class Index2Handler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('10_lesson_base.html',namelist=['111','222','333'])










class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')                           # 跳转登录页面

    def post(self):
        name = self.get_argument("name", '')                # 获取账号
        password = self.get_argument('password', '')        # 获取密码
        if name == '111' and password == '222':             # 若有账号和密码设置cookie
            self.session.set("user",name)
            self.redirect('/index')
        else:
            self.write('登录失败')



#项目入口
if __name__ == '__main__':
    handlers = [                                            # handlers路由映射
        (r'/index',IndexHandler),
        (r'/login',LoginHandler),
        (r'/index1',Index1Handler),
        (r'/index2',Index2Handler),


    ]

    settings = dict(                                        # setting环境配置
        template_path='templates',                          # 模板文件
        static_path='static',                               # 静态文件
        debug=True,
        cookie_secret='aaaa',                               # 设置cookie密钥
        login_url='/login',                                 # @authenticated验证不通过直接跳转定义路由
        xsrf_cookies=True,                                  # 开启xsrf功能
        # pycket的配置信息
        pycket={
            'engine': 'redis',                              # 设置存储器类型
            'storage': {                                    # 储存信息
                'host': 'localhost',                        # 主机
                'port': 6379,                               # 端口号
                'db_sessions': 5,                           # 多少号数据库
                'db_notifications': 11,                     #
                'max_connections': 2 ** 31,                 # 最大连接
            },
            'cookies': {                                    # 设置cookie过期时间
                'expires_days': 30,
                'max_age': 5000,
            },
        },
    )

    tornado.options.parse_command_line()                    #解析命令行,解析define端口号
    app = tornado.web.Application(handlers,**settings)      #请求:响应头handlers, 配置**settings
    http_server = tornado.httpserver.HTTPServer(app)        #启动服务
    http_server.listen(options.port)                        #监听多个端口
    tornado.ioloop.IOLoop.instance().start()                #开启循环