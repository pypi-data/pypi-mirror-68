from distutils.core import setup
setup(
    name="hefMath", # 对外我们模块的名字
    version="1.0", # 版本号
    description="这是第一个对外发布的模块，测试哦", #描述
    author="huenfeng", # 作者
    author_email="1511715823@qq.com",
    py_modules=["hefMath.demo1","hefMath.demo2"] # 要发布的模块
)