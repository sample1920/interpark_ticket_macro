# interpark_ticket_macro
인터파크 뮤지컬 티켓 자동 예매 프로그램

## 기본 설정

1. chromedriver 다운로드
  - Chrome 브라우저 version 확인(크롬 브라우저 검색창에 chrome://settings/help 입력)
  - version에 맞는 chrome driver 설치(https://chromedriver.chromium.org/downloads)
  - 다운받은 chromedriver를 main.py와 같은 directory로 옮기기
 
2. package 설치
  ```
  $ pip install -r requirements.txt
  ```

3. settings 파일 설정
  ```
  {
      "userid": 인터파크 아이디,
      "password": 인터파크 비밀번호,
      "reservation_time": 티켓 예매를 수행할 시각 설정. 해당 시간에 예매 동작이 수행됨,
      "ticket_code": 뮤지컬 예매 페이지 갔을때 해당 페이지 URL의 ?GoodsCode={code} 혹은 goods/{code} 의 code값,
      "ticket_date": 티켓 날짜,
      "ticket_type": 좌석 종류(S, R, VIP)
  }
  ```

4. 실행
  ```
  $ python main.py
  ```
  - 정상적으로 수행되면 예약완료 정보가 담긴 scrennshot.png라는 파일이 생성됨
  
## 옵션

* chrome 브라우저 동작하는거 보려면 코드에서 options.headless = False 

## 기타

* CAPTCHA가 있는 뮤지컬의 경우 headless를 True로 하고 직접 입력해주기
