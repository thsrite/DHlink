# DHlink
nas-tools小工具。

扫描规定目录下的视频是否有硬链接。

筛选出创建时间7天以上，且视频文件大于100M的视频文件及路径。可配置发送邮件提醒，默认一天扫描一次。

支持docker部署。

拉取代码后

cd DHlink

docker build -t dhlink .

docker run -d --name dhlink -v /电影目录:/mnt/movies -v /电视剧目录:/mnt/series -v /配置文件目录/config.yaml:/mnt/config.yaml dhlink


配置文件config.yaml

stmp:
  host: smtp.163.com #163邮箱stmp host
  from_addr: 111@163.com #163发件邮箱
  password: 111 #163发件邮箱密码
  to_addr: 111@163.com #接收邮件邮箱

sync:
  time: 86400 #定时扫描，单位秒。
