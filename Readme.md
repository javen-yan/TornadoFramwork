# API BACKEND 部署方法

### 系统环境 Python3 + Mysql + Mongo + ES



### 1. 安装python依赖
```
python3 pip install -r requirements.txt # python3
或
python pip install -r requirements.txt  # python3
```

### 2. 生成WASM公钥私钥

```
python -m main -t  # 或生成一对密钥请填写在下面配置中
```


### 3.修改配置文件
```
cp config.template.ini config.ini
vim config.ini # 添加一些配置
```

### 4. 启动服务
```
nohup python3 -m main -runserver -filename=logs/run.log -level=DEBUG &
```
