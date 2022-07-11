# DHlink
### nas-tools小工具。

>emby或flex、Jellyfin映射的是经过nas-tools同步后的目录。
在emby上删除电影或电视剧之后只会删除同步后目录中的源文件的硬链接，不会删除原文件，长时间会造成很多冗余，
懒得手动查找，便写了个简单的工具帮忙筛选，可扫描规定目录下的视频是否有硬链接。

筛选出创建时间7天以上，且视频文件大于100M的视频文件及路径。可配置发送邮件提醒，默认一天扫描一次。

支持docker部署。

拉取代码后

```
cd DHlink
docker build -t dhlink .
docker run -d --name dhlink -v /电影目录:/mnt/movies -v /电视剧目录:/mnt/series -v /配置文件目录/config.yaml:/mnt/config.yaml dhlink
```

或

```
docker pull thsrite/dhlink:latest
docker run -d --name dhlink -v /电影目录:/mnt/movies -v /电视剧目录:/mnt/series -v /配置文件目录/config.yaml:/mnt/config.yaml dhlink
```
配置文件config.yaml

    stmp:
      host: smtp.163.com #163邮箱stmp host
      from_addr: 111@163.com #163发件邮箱
      password: 111 #163发件邮箱密码
      to_addr: 111@163.com #接收邮件邮箱
    sync:
      time: 86400 #定时扫描，单位秒。
      search_day: 7 #扫描创建时间多少天以上的视频
      search_size: 100 #扫描文件大小多少M以上的视频
      auto_del: false #是否自动删除可删除文件夹及可删除视频，不会删除有关联不建议删除的视频， 默认false。谨慎用true

![不删除仅提醒](https://raw.githubusercontent.com/jiangxd0716/DHlink/master/photo/不删除不提醒.png)

![自动删除且提醒](https://raw.githubusercontent.com/jiangxd0716/DHlink/master/photo/删除.png)

![邮件提醒](https://raw.githubusercontent.com/jiangxd0716/DHlink/master/photo/WechatIMG177.png)

![邮件提醒](https://raw.githubusercontent.com/jiangxd0716/DHlink/master/photo/WechatIMG178.jpeg)