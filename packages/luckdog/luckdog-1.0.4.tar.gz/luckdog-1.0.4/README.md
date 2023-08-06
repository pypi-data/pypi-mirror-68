uckdog  新版本已经出来了

luckdog是类似于postman的接口访问工具。


使用说明：

1） 安装：

    pip install luckdog

2） 执行

    Python -c "from luckdog.main import  Main; Main()" 

## 注： 为方便后期操作方便 

# 可以 把上面的 运行命令放到bat或shell文件中，下次直接双击运行 

#######################################################################

Last update time: 2020-04-20 

By： 8034.com

#######################################################################

更新日志：


#######################################################################

    ## 打包 检查
    python setup.py check 
    ## 打包 生成
    python setup.py sdist
    ## 上传
    twine upload dist/*
    ## 使用
    pip install luckdog 
    ## 更新
    pip install --upgrade luckdog
    ## 卸载
    pip uninstall -y luckdog 
#######################################################################

## MANIFEST.in 

    include pat1 pat2 ...   #include all files matching any of the listed patterns

    exclude pat1 pat2 ...   #exclude all files matching any of the listed patterns

    recursive-include dir pat1 pat2 ...  #include all files under dir matching any of the listed patterns

    recursive-exclude dir pat1 pat2 ... #exclude all files under dir matching any of the listed patterns

    global-include pat1 pat2 ...    #include all files anywhere in the source tree 
    matching — & any of the listed patterns

    global-exclude pat1 pat2 ...    #exclude all files anywhere in the source tree matching — & any of the listed patterns

    prune dir   #exclude all files under dir

    graft dir   #include all files under dir
