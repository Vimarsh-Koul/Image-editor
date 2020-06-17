import tornado.web
import tornado.ioloop

if(__name__=="__main__"):
    app=tornado.web.Application([
    ("/images/(.*)",tornado.web.StaticFileHandler, {"path":"images"})
    ])

    app.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
