# Django-Resident-Management-App
# 大樓管委會系統
提供住戶與管委會交換意見及交流的網站，意圖透過資訊透明化使住戶和諧。
## Getting Started
**python ==3.7 or up and django == 3 or up**
## Installing
open terminal and type 
    
    git clone https://github.com/getroundintheseason/RMWweb.git
    cd RMWweb
    pip3 install -r requirements.txt

### Migrate the database
    python3 manage.py makemigrations
    python3 manage.py migrate
    
### Create admin account
    python3 manage.py createsuperuser

### Run the website!!
    python3 manage.py runserver

## Register User
可以提供使用者註冊及登入帳號

# 功能
- Messege 提供使用者留言
- InfoMessege 提供管理者（管委會）新增公告
- Poll 提供使用者及管理者 *意見連署*
- 管委會權限須由superuser開啟

## Messege 留言 功能
-  MessegeDetail 瀏覽 留言
-  MessegeCreate 新增 留言
-  MessegeUpdate 更新 留言
-  MessegeDelete 刪除 留言

## InfoMessege 公告 功能 (只限manager帳號)
-  InfoMessegeDetail 瀏覽 公告
-  InfoMessegeCreate 新增 公告
-  InfoMessegeUpdate 更新 公告
-  InfoMessegeDelete 刪除 公告

## Poll 公投 功能
-  PollDetail 瀏覽 公投
-  CreatePoll 新增 公投

# Poll 投票 功能 
### CreateVote 瀏覽 投票 
- 一人限投一次
- 在公投的開始日期及結束日期內始能投票
