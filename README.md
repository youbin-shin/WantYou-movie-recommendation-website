# `완`t`유`(Wantyou) 최종 프로젝트

## 프로젝트 소개

### 1. 목표

- 영화 정보 기반 추천 서비스 구성
- 커뮤니티 서비스 구성
- HTML, CSS, JavaScript, Vue.js, Django, REST API, DataBase 등을 활용한 실제 서비스 설계
- 서비스 배포 및 관리

### 2. 개발 환경

1. Python Web Framework
   A. Django 2.1.15
     B. Python 3.7+
2. Vue 개발 환경
   A. Node 12.18.X
     B. Vue 2.6+
3. 개발 아키텍처
   A. Django & Vanila JS
4. 서비스 배포 환경
   아래의 옵션 중 하나를 선택하여 구성하시오.
     A. 서버: Ubuntu / Amazon Linux 등
     B. DB: MySQL / SQLite 등3. 프로젝트 수행 정보

## 프로젝트 구조



## 팀원 정보 & 개발 역할 분담

(ppt 표 추가하기)



### 개발 과정

- 프로젝트 이름은 `WantYou` 입니다.

- ~~를 이용하여 받은 JSON 데이터를 사용할 `` app이 있습니다.

  

- **movie community**

  - base.html

  - **accounts**

    - login
      - social login
    - logout
    - signup
    - profile (관심장르 선택 페이지, 좋아요 했던 영화목록)

  - **movies**

    - index.html 
    - 로그인 한 경우 : 추천 서비스 기능 보이기
      - 로그인 안한 경우 : movie list  좋아요 순으로 영화 목록 보이기
    - movie_detail.html
      - 예고편



## WantYou(완t유) 웹 서비스란?

### 핵심 기능

##### 추천 서비스

- 로그인 후에 설정한 장르 
- 좋아요 많은 영화

---

> 모바일 대응을 위한 반응형 웹, Django REST API 서버 및 프론트엔드 프레임워크(Vue.js) 분리 등의 상세 구현 방식은 자유롭게 구성하되, 프로젝트 README.md 상단에 프로젝트 구조에 대한 설명을 반드시 명시해야 합니다.

> 해당 Gitlab 저장소의 최상단에는 반드시 README.md 이 있어야 하며 아래의 내용이 기록되어 있어야 합니다.
> 팀원 정보 및 업무 분담 내역
> 목표 서비스 구현 및 실제 구현 정도
> 데이터베이스 모델링(ERD)
> 필수 기능
> 배포 서버 URL
> 기타(느낀점)

---

### 힘들었던 점(문제 해결 과정 정리)

#### 1. JSON 데이터로 만들기

JSON

**API Key**: 4c1f2b1892e903f71202543b9968a563

- THE MOVIE DB

  key : 4c1f2b1892e903f71202543b9968a563

  > https://developers.themoviedb.org/3/getting-started/json-and-jsonp

- 유튜브 링크로 트레일러 가져오기

  > https://blog.naver.com/cosmosjs/221715332150

  api.themoviedb.org/3/movie/{비디오id}/videos?api_key={Your key}