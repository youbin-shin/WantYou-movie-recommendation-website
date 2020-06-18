# `Wan`t`You` 최종 프로젝트

## 프로젝트 구조

- 프로젝트 이름은 `WantYou` 입니다.

- 세가지 앱으로 이루어져있습니다.

  1.  `accounts` 

     사용자의 회원가입, 로그인, 로그아웃, 사용자 마이페이지를 관리하는  application 디렉토리입니다.

  2. `movies`

     메인 기능을 담당하는 앱으로 영화 추천 서비스와 영화 목록을 보고 탐색할 수 있는  application 디렉토리입니다.

  3. `communities`

     영화 후기에 대한 게시글을 통해 공유하며 소통의 역할을 하는  application 디렉토리입니다.

- `The Movie Database(TMDb)`를 이용하여 JSON 데이터를 만들어 `movies` 앱에서 활용했습니다.

```
wantyou/ 
    __init__.py
    settings.py
    urls.py
    wsgi.py
accounts/
	templates/accounts/
		signup.html (회원가입 페이지)
		login.html (로그인, 소셜 로그인 페이지)
		update.html (회원 정보 수정하는 페이지)
		profile.html (마이 페이지, 사용자가 즐겨찾기한 영화&community에 작성한 글 목록 관리 페이지)
    __init__.py
    admin.py
    app.py
    forms.py 
    models.py
    test.py
    urls.py 
    views.py
movies/ 
	fixtures/movies/moviedata.json
	templates/movies/
		home.html (사이트의 설명, 주요 기능 소개 페이지)
		index.html (영화 목록, 영화 추천 서비스, 영화 검색 기능 페이지)
		detail.html (영화 클릭시 예고편, 평점 등 영화 관련 정보 페이지)
		form.html (admin 계정일 경우 영화 추가, 삭제, 수정할 수 있도록 하는 페이지)
    __init__.py
    admin.py
    app.py
    forms.py 
    models.py
    test.py
    urls.py 
    views.py  
communities/ 
    migrations/
    templates/community/
        form.html (영화 감상평을 작성할 수 있는 페이지)
        review_list.html (communities의 주요 페이지, 목록 페이지)
        review_detail.html (게시물의 디테일 페이지, 댓글 가능한 페이지)
    __init__.py
    admin.py
    app.py
    forms.py
    models.py
    test.py
    urls.py 
    views.py   
templates/
	base.html 
.gitignore
manage.py
README.md
requirements.txt
```

---

## 팀 정보

- 팀명 : `WantYou`
- 팀원 : 조완석 **`팀장`**, 신유빈

## 개발 일정 및 업무 분담 내역

![개발 일정 및 진행 과정](https://user-images.githubusercontent.com/60081201/84967212-65b2bf00-b14e-11ea-8042-c77b4196ed21.png)

---

## :computer: ​프로젝트 진행 과정 

### 1. 준비 단계

#### 목표 서비스 설정하기

- 필요한 기능 정하기, 페이지 초안 그리기

  ![초반 설정 정리한 그림](https://user-images.githubusercontent.com/60081201/84975148-ad8e1200-b15f-11ea-9fc5-61a0117bca91.png)

#### 데이터베이스 모델링하기 (ERD)

<img width="782" alt="ERD" src="https://user-images.githubusercontent.com/60081201/84976325-8d138700-b162-11ea-87e0-c791f805136b.png">

### 2. 개발 단계

위의 개발 일정대로 진행하였다.

#### :pencil:문제 해결 과정 정리 

##### [필요한 영화 데이터를 JSON 데이터로 만들기]

`THE MOVIE DB` 의 사이트에서 API Key를 발급받아 필요한 데이터가 담긴 URL를 찾는다.

> `The MOVIE DB` 홈페이지
>
> https://www.themoviedb.org/
>
> - 영화 장르에 대한 정보가 들어있는 페이지
>
>   https://developers.themoviedb.org/3/genres/get-movie-list

아래의 코드를 통해 JSON 데이터를 만들어주었다.

**주의해야할 부분은 형태를 잘 갖춰야 load** 할 수 있다.

처음에는 영화 데이터와 장르 데이터를 각각 받아서 load하려고 했으나 아래의 코드를 통해 영화 데이터를 원하는 형태로 만드는 과정에서 장르 데이터를 이용하여 하나의 데이터를 만들었다.

```python
import requests
import json
genres = [{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 16, "name": "Animation"}, {"id": 35, "name": "Comedy"}, {"id": 80, "name": "Crime"}, {"id": 99, "name": "Documentary"}, {"id": 18, "name": "Drama"}, {"id": 10751, "name": "Family"}, {"id": 14, "name": "Fantasy"}, {"id": 36, "name": "History"}, {"id": 27, "name": "Horror"}, {"id": 10402, "name": "Music"}, {"id": 9648, "name": "Mystery"}, {"id": 10749, "name": "Romance"}, {"id": 878, "name": "Science Fiction"}, {"id": 10770, "name": "TV Movie"}, {"id": 53, "name": "Thriller"}, {"id": 10752, "name": "War"}, {"id": 37, "name": "Western"}]
jsondata = []
for i in range(1, 26): # 500개(1부터 25페이지)의 영화 데이터를 받을 것이다.
  data = requests.get(f'http://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=4c1f2b1892e903f71202543b9968a563&language=ko&page={i}').json()
  data_results = data['results'] # results 안에 필요한 데이터 있다!
  for result in data_results:
    temp = {}
    # 기본 설정해준다.
    temp['model'] = 'movies.movie'
    temp['id'] = result.pop('id')
    # field라는 딕셔너리를 생성하여 필요한 데이터를 저장할 것이다.
    field = {}
    # modelfield : django에서 model.py에서 데이터 필드를 정의한 속성들을 저장한 리스트이다.
    modelfield = ['title', 'original_title', 'release_date', 'popularity', 'vote_count', 'vote_average', 'adult', 'overview', 'original_language', 'poster_path', 'backdrop_path']
    real_genre = [] # 영화 데이터에 들어있는 장르를 저장해줄 리스트를 준비한다.
    for key, value in result.items():
        if key in modelfield:
            field[key] = value # 정의한 속성들은 field 딕셔너리에 저장한다.
        elif key == 'genre_ids':
            genre_nums = value # genre_ids 에 있는 번호들을 리스트에 저장한다.
            for genre_num in range(len(value)):
                for i in range(len(genres)):
                    if genres[i]['id'] == genre_nums[genre_num]: # genres의 리스트를 통해 영화의 장르를 알아낸다.
                        real_genre.append(genres[i]['name']) # 장르를 저장한다.
                        if genre_num == len(genre_nums)-1: # 마지막 장르 번호일 경우 field 딕셔너리에 genres를 저장한다.
                            field['genres'] = real_genre
                        break
                    
    temp['fields'] = field # result.items에서 저장한 필요한 fields를 temp 딕셔너리에 저장한다.
    jsondata.append(temp) # jsondata에 데이터를 추가해나간다.

# 원하는 데이터를 저장한 jsondata를 moviedata.json 파일에 json 데이터로 저장한다.
with open('moviedata.json', 'w', encoding="UTF-8") as make_file:
    json.dump(jsondata, make_file, indent="\t")
```

##### [JSON 데이터에서 value가 리스트 형태인 genres를 django models.py에서 ListField를 통해 저장하기]

- `ListField`
  - mysql 설치가 필요하다. 크기에 대한 정의가 필요하다.
  - 크기 조절 : 장르는 영문자가 20자 넘지않기에 `base_field=models.CharField(max_length=20),` 를 설정한다.
  - 장르의 갯수는 최대 19개이므로 `size=19,` `max_length=(19 * 21) ` 로 기준을 잡았다.

##### [소셜 로그인 구현하기]

> https://django-allauth.readthedocs.io/en/latest/installation.html

- `django all auth`를 통해 소셜 로그인을 구현한다.
- 위의 공식문서를 통해 설치와 settings.py에 필요한 코드를 추가한다.
- 프로젝트 urls.py에서 기존의 accounts 앱 **밑**에 allauth.urls 의 path를 추가해야한다.
- 소셜 로그인 후 원하는 페이지로 돌아가지 않는 문제는 settings.py 맨 밑에 `LOGIN_REDIRECT_URL`을 이용하여 해결할 수 있다.

##### [영화 검색 기능 만들기]

- 검색 기능을 추가할 HTML 페이지에 input 태그를 만들어 준다. 
- input 태그 안에 설정한 name을 기준으로 views.py에서 `request.Get.get('{설정한 name}')`를 이용하여 입력한 데이터를 받는다.
  - filter를 이용하여 영화를 검색해준다.

### 3. 평가 단계

- 동작하는 데 에러 사항없는 지 검토하기
  - 에러 발견시 문제 해결하기

#### 목표 서비스 구현 및 실제 구현 정도

![목표 서비스 구현 정도 표](https://user-images.githubusercontent.com/60081201/84977776-30b26680-b166-11ea-9fd0-40d58351868e.png)

### :honey_pot: Tip

다음을 이용하여 보다 간편하게 프로젝트를 진행할 수 있었다.

- Gitlab을 이용하여 작업 과정을 commit을 통해 기록하고 공유했다.

  - git pull/clone 후 해야할 일 정리

    1. 가상환경을 설정한다.

      ```bash
      $ python -m venv venv
      $ source venv/Scripts/activate
      (venv)
      $ pip list
      ```

    2. 프로젝트에 requirements.txt를 통해 작업환경에 필요한 것을 설치한다.

      ```bash
      $ pip install -r requirements.txt
      ```

    3. migrate를 진행한다.

    4. JSON 데이터를 로드한다.

      ```bash
      $ python manage.py loaddata movies/moviedata.json
      ```

- JSON 데이터를 정렬하거나 형태가 맞는지 판단할 수 있는 사이트를 이용했다.

  > https://jsonformatter.curiousconcept.com/

---

## :star: `WantYou` 에 대한 모든 것!

### Intro

#### 웹 서비스 목표

- 사용자 맞춤으로 영화 추천 서비스를 제공한다.
- community 페이지를 통해 영화 후기, 감상평을 공유할 수 있는 소통 서비스를 제공한다.
- ssafy 1학기 교육 과정을 통해 배운 내용과 역량을 충분히 발휘하여 목표한 서비스를 구현한다.

#### 로고 소개

<img width="472" alt="logo" src="https://user-images.githubusercontent.com/60081201/84667771-c16a2600-af5d-11ea-86a9-65a5a503011f.png">

제작자 조`완`석의 Wan과 신`유`빈의 You를 `+` 더하여 WantYou라는 웹 페이지 이름으로 **당신이 원하는 영화 추천 서비스**를 제공하겠다는 의미를 담고 있다. 

### Django 앱별 핵심 기능 정리

![movies 앱 기능 설명](https://user-images.githubusercontent.com/60081201/84970036-dbba2480-b154-11ea-89ec-0f117217cfa3.JPG)

![accounts, communities 앱 기능 소개](https://user-images.githubusercontent.com/60081201/84970192-2471dd80-b155-11ea-9539-6f09b09af52c.JPG)

### 웹 페이지 화면을 통한 기능 설명

#### Home 페이지

- 웹 페이지에 대한 간략한 소개와 주요 기능에 대해 설명한다.

![Wantyou home페이지](https://user-images.githubusercontent.com/60081201/84973021-08713a80-b15b-11ea-9132-a0ffaeb6287a.png)

#### Movie 페이지 

- 우측 상단 부분에 영화 검색을 가능하도록 하였다.
  - 검색어가 없을 경우와 영화 데이터가 없는 경우 메세지를 통해 사용자에게 알림을 주도록 설정하였다.
  - 검색어를 입력하면 입력한 검색어가 있는 영화수와 영화 목록을 볼 수 있다.
- `오늘의 추천 영화`는 로그인하지 않은 사용자가 들어있을 때만 보여지며 카로젤을 이용하여 영화 인기도를 기준으로 1위 부터 4위, 5위부터 8위, 9위부터 12위 영화를 볼 수 있다.
- **영화 추천 서비스**
  - `즐겨찾기 기능`을 통해 사용자는 사용자 맞춤형 영화를 추천 받을 수 있고 개발자는 사용자가 좋아하는 영화 장르를 파악하여 추천 가능하다.
  - 로그인을 하여 사용자가 관심있는 영화를 즐겨찾기 해놨다면 즐겨찾기한 영화 장르 데이터를 분석하여 사용자 맞춤으로 영화를 추천한다.
    - 첫 카로젤 페이지에서는 사용자가 가장 좋아하는 장르 2가지를 모두 만족하는 인기순 4개의 영화를 보여준다.
    - 두번째 카로젤 페이지에서는 사용자가 가장 좋아하는 장르를 기준으로 인기순 4개의 영화를 보여준다.
    - 세번째 카로젤 페이지에서는 사용자가 두번째로 좋아하는 장르를 기준으로 인기순 4개의 영화를 보여준다.
- 카로젤 밑에는 영화 평점순으로 영화 목록을 제공한다.
- 페이지네이션을 통해 페이지 이동을 원활하게 한다.

![movie 로그인 비교 페이지 화면](https://user-images.githubusercontent.com/60081201/84976645-630e9480-b163-11ea-8a70-53372b4b7849.png)

##### 영화 사진 또는 상세보기 버튼 클릭시 Detail 페이지

- 영화 트레일러와 영화 관련 정보에 대해 볼 수 있는 페이지로  평점을 별로 표시하여 가시성을 높였다. 
- 디테일 페이지를 통해 즐겨찾기가 가능하다.

![디테일 페이지 화면](https://user-images.githubusercontent.com/60081201/84975141-ab2bb800-b15f-11ea-8bd8-4fd461b22b47.png)

#### Community 페이지 

- 작성자, 작성 내용, 댓글 수, 작성 시간을 타임라인 디자인으로 구성했다.
- 자세히 보기 버튼을 누르면 댓글을 작성할 수 있다.

![community 페이지 화면](https://user-images.githubusercontent.com/60081201/84973953-3fe0e680-b15d-11ea-9433-252e223d6e58.png)

#### 마이페이지

마이페이지를 통해 community에 작성한 글 목록과 즐겨찾기한 영화 목록을 볼 수 있다.

![마이페이지 화면](https://user-images.githubusercontent.com/60081201/84974033-6d2d9480-b15d-11ea-97b3-a508869d6dde.JPG)

## :e-mail: 프로젝트를 마치며

- 조완석

  ~~

- 신유빈

  ~~