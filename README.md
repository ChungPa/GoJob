# GoJob
고졸 취업 정보 모음 사이트.



# Develop Enhancement Proposals
## Branch System
사용하는 브랜치 목록은 아래와 같습니다.
- Master  
    > 실질적으로 배포가 이루어지는 코드가 담기는 브랜치.
    >> Push branch: HotFix, Develop
    
- Develop  
    > 개발 중인 코드가 담기는 브랜치.  
    >> Push branch: Functions, HotFix
    
- HotFix  
    > Pull request 에서 검출되지 않은 에러가 나왔을 경우, 응급 패치용으로 사용하는 브랜치.  
    `[Commit_ID]-HotFix` 형태로 사용
    >> Push branch: None
    
- Functions  
    > 실질적인 기능구현이 이루어 지는 브랜치.  
    구현하는 기능과 관련된 이름을 사용.  
    모든 Functions 브랜치 앞에는 만든 개발자 이름을 적음  
    예. 사람인 사이트 크롤러 개발의 경우) `[Developer]-saramin-crawler`  
    >> Push branch: None

## Pull Request Naming Rule
사용하는 헤더들은 아래 목록을 사용합니다.
사용 예시) `[MRG] Fix Saramin crawler error`

- MRG  
    Merge를 원하는 Pull request 일 경우 사용  
    이 상태일 경우, Reviewer 가 리뷰
    
- WIP  
    작업 중일 경우 사용  

- RVW  
    1차 리뷰를 받고 수정 후 다시 리뷰를 요청하는 상태일 경우 사용  

## Merge Rule
- Master, Develop  
    모든 Reviewer 에게 Approve.  
    (단, From HotFix 일 때는 그냥 머지 ㄲ)
    
- HotFix, Functions
    리뷰 없이 Push 가능

## Deploy System (DevOps?)
- Circle CI (testing, deploy) --> 사실 이거 밖에 안써봄 (테스트부터 배포까지)  
- Jenkins  
- ETC..  