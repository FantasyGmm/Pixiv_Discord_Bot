<h1>Bot仍处于开发版本<p></h1>
目前已实现功能:<p>
ban 封禁用户<p>
   命令使用方法:$ban @用户(unban kick同理)<p>
unban  解封用户<p>
kick 踢人<p>
s_img 根据P站ID搜索图片<p>
  命令使用方法:$s_img PixivId<p>
注:可以搜索GIF图，多图，因为p站防盗链设计所以所有图片均需要缓存到本地再上传，部分图片无法上传是因为discord的原因，附件最大为8MB，超过大小的均无法上传<p>
cleanimg 清理本地img缓存<p>
  命令使用方法:$cleanimg<p>
注:缓存目录位bot.py同级目录下的temp文件夹，如果没有会自动创建，使用clean会删除temp文件夹里的所有文件包括temp文件夹<p>
logout 登出机器人<p>
  命令使用方法:$logout<p>
<p>
IDE:JetBrains PyCharm Community Edition 2019.1.1 x64<p>
这个仓库是用作完整项目备份的，直接下载解压，打开项目会存在问题<p>
你只需要source code里面的东西，虚拟环境需要重新构建<p>
用到的库已经写进了source code里的文本文件了<p>
bot.py需要进行一定的修改才能使用<p>
部分命令带有权限限制，权限限制为仅Bot所有者才能使用，需要在your ID填入你的 名字#id <p>
在bot.py最后结束的位置，需要在bot token 里面填入你自己的bot令牌<p>
