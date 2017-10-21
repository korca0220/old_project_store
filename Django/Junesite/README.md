# **Django - Junesite(게시판 사이트)**

---
### 기본 개발스택(AWS)
- Elastic Beanstalk - 가상환경 Setting, Version Environment
- RDS(MySql) - 데이터베이스 서버로 이용
- S3 - static/media 파일 저장 및 서빙
- EC2 - 웹 서버 - 장고 애플리케이션 구동

### 라이브러리 파일 - reqs
- common.txt - 공통 pip list
- dev.txt - 개발용 pip list
- prod_aws_eb.txt - 아마존 aws - elastic beanstalk 서비스 이용 pip list

현 소스는 개발 pip list를 모두 common에다가 넣은 상태.

### Setting 파일 - settings directory
- common.py - 공통 세팅 파일
- dev.py - 개발 전용 세팅 파일(debug-toolbar 설정이 포함되어 있음)
- prod_aws_eb.py - 배포용 세팅파일 (DEBUG=False, ALLOWED_HOST= 가 변경된게 핵심)

### 환경 변수

- set DJANGO_SETTINGS_MODULE=Junesite.settings.prod_aws_eb
- set DB_HOST=
- set DB_NAME=
- set DB_PASSWORD=
- set DB_PORT=3306
- set DB_USER=
- set AWS_ACCESS_KEY_ID=
- set AWS_S3_REGION_NAME=
- set AWS_SECRET_ACCESS_KEY=
- set AWS_STORAGE_BUCKET_NAME=

#### 각각의 환경변수를 AWS-EB 내 환경변수로 적용시켜줘야 AWS로 배포 가능.
#### * NAVER_CLIENT_ID는 예외로 common.py내의 세팅파일에서 추가시켜 줘야 합니다.

### Login

- 회원가입을 통한 login ID 생성 가능
- Facebook, Google, Kakao 아이디를 통한 social ID로 로그인 가능
- staff or superuser가 아닌이상 admin 페이지 접근 불가능
- social ID로 로그인한 경우 profile에서 본인 사진 노출

## Blog(Post), Photo 페이지

- Blog 게시판에서 Post 작성 시 네이버 맵을 이용해 현재 위치 지정 가능
- Blog 게시판에서는 그림 삽입 불가
- Photo 페이지에서 내용을 제외하고 사진 삽입을 통해 사진을 주제로 함
