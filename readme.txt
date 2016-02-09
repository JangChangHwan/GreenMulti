GreenMulti

목적 : 시각장애인들이 더이상 텔넷에 접속할 필요가 없도록 넓은마을과 아이프리 웹페이지를 자동화를 하는 것.

개발도구 : 
python 2.7.11 
3rd 패키지 및 모듈
wxpython-phoenix
MultipartPostHandler
BeautifulSoup4

* 각 파일의 용도
- PageInfo.Dat : 
트리 메뉴를 구성하기 위한 페이지 정보 파일 
각 줄의 의미
페이지코드, 부모페이지코드, 제목, 주소(혹은 '|'로 구분된 코드모음)
각 요소는 탭으로 구별이 되어야 합니다.
