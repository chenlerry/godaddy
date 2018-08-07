## API 接口说明

`修改src/common.py中的api_key及api_secret信息`

```text
通过到GodAddy去获取相关的key和secret
https://developer.godaddy.com/ # 获取API Keys
```


`API启动`

```bash
cd project
python server.py --port=8888 --log_file_prefix=~/god_api.log
```

```text
/api/get_domain # 获取域名列表
/api/get_record # 获取域名的所有A记录
/api/create_record # 创建域名的指定A记录
/api/remove_record # 删除域名的指定A记录
```


* `/api/get_domain`

```bash
curl 'http://127.0.0.1:8888/api/get_domain'
domain: 80ers.com
domain: xinyuanxian.com
domain: yangbanjian.net
domain: zhinang.org
```

* `/api/get_record`

```bash
curl -d 'domain=domain.io' 'http://127.0.0.1:8888/api/get_record'
A                1.1.1.1                test                 3600
A                2.2.2.2             chenliang               3600
```

* `/api/create_record`

```bash
curl -d 'domain=domain.io&short_addr=x.x.x.x&a_record=xx' 'http://127.0.0.1:8888/api/create_record'
True:
{ 'errno': 200, 'result': 0,  'errmsg': '' }

False:
{ 'errno': 500, 'result': 1,  'errmsg': 'Another record with the same attributes already exists' }
```

* `/api/remove_record`

```bash
curl -d 'domain=xxxx&a_record=xxxx' 'http://127.0.0.1:8888/api/remove_record'
{ 'errno': 200, 'result': 0,  'errmsg': '' }
```
