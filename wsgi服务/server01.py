from wsgiref.simple_server import make_server
import os

# a = ['content-type','content-length','connection']
# b = ['text/html',14,'keep-alive']
# zip(a,b)
# list(zip(a,b))

def app(env, make_response):
    # 处理业务最核心的函数
    """
    请求路径：PATH_INFO : /favicon.ico
    请求方法：REQUEST_METHOD : GET
    请求查询参数：QUERY_STRING
    客户端地址：REMOTE_ADDR : 192.168.1.103
    请求上传的数据类型：CONTENT_TYPE : text/plain
    客户端的代理（浏览器）: HTTP_USER_AGENT
    读取请求上传的字节数据对象：wsgi.input
    wsgi是否使用了多线程：wsgi.multithread : True
    wsgi是否使用了多进程：wsgi.multiprocess : False
    """
    # for k ,v in env.items():
    #     print(k, ':',v)
    # 定义请求路径
    path = env.get('PATH_INFO')

    headers = [] #响应头，根据响应的数据增加不同的响应头k:v
    body = [] #响应的数据
    #设置静态资源的目录
    static_dir = '../jquery_'
    if path == '/favicon.ico':
        res_path = os.path.join(static_dir,'images/collect01.png')
        headers.append(('cantent-type','image/*'))
    elif path == '/':
        # 主页
        res_path = os.path.join(static_dir,'js.dubo.html')
        headers.append(('cantent-type', 'text/html;charset=utf-8'))
    else:
        #其他资源：css/js/图片/MP4/mp3
        #/js/jquery.min.js
        res_path = os.path.join(static_dir,path[1:])
        if res_path.endswith('.html'):
            headers.append(('cantent-type', 'text/html;charset=utf-8'))
        elif any((res_path.endswith('.png'),
                  res_path.endswith('.jpg'),
                  res_path.endswith('.gif'))):
            headers.append(('content-type','image/*'))
        else:
            # js/css
            headers.append(('content-type','text/*;charset=utf-8'))
    # 生成响应头
    # make_response('200 OK',
    #               [('Content-Type','text/html:charset=utf-8')])
    # return ['<h3>Hi,WSGI</h3>'.encode('utf-8')] # 响应数据结构
    # 判断资源是否存在 res_path
    status_code = 200
    if not os.path.exists(res_path):
        status_code = 404
        body.append('<h1 style="color:red">请求的资源不存在：404</h1>'.encode('GBK'))
    else:
        with open(res_path,'rb') as f:
            body.append(f.read())
    make_response('%s OK' % status_code,headers)
    return body
# 生成web服务进程
host = '0.0.0.0'
port = 8000
httpd = make_server(host, port, app)
print('running http://%s:%s' % (host,port))

# 启动服务，开始监听客户端连接
httpd.serve_forever()