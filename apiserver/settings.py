from redis import Redis


class Dev:
    ENV = 'development'  # 默认运行环境是production
    SECRET_KEY = 'ddkakda%&akd#@'

    # 配置session
    SESSION_TYPE = 'redis'
    SESSION_REDIS = Redis(host='116.62.193.152',port='6379',db=8)

    # 配置静态资源目录及访问的url
    # STATIC_FOLDER = 'static'
    # STATIC_URL_PATH = '/s'

    # 配置SQLALCHEMY数据库连接及特征
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@116.62.193.152:3306/System'
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 可扩展
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 回收资源时自动关闭
    SQLALCHEMY_ECHO = True  # 显示SQL


class Product:
    ENV = 'production'
    SECRET_KEY = 'ddkak098%&akd#@'
