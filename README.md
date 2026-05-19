# 안효민 엔지니어 포트폴리오

소프트웨어, 시스템, 하드웨어, 자동화, 문제 해결 역량을 함께 보여주기 위한 정적 포트폴리오 사이트입니다. 별도의 빌드 과정 없이 HTML, CSS, JavaScript만으로 동작하며 GitHub Pages에 바로 배포할 수 있습니다.

## 파일 구조

- `index.html`: 페이지 구조, 소개 문구, 문제 해결 과정, 프로젝트 카드, 대표 프로젝트, 연락처 정보
- `style.css`: 레이아웃, 색상, 반응형 디자인, 이미지 placeholder 스타일
- `script.js`: 모바일 메뉴, 현재 섹션 표시, 선택 이미지 표시 처리
- `images/`: 프로필 사진과 프로젝트 사진을 넣는 폴더
- `files/`: 이력서 PDF 같은 첨부 파일을 넣는 폴더
- `README.md`: 실행 및 수정 안내

## 실행 방법

별도의 설치나 빌드 과정은 필요하지 않습니다.

1. 이 폴더를 엽니다.
2. `index.html` 파일을 브라우저에서 실행합니다.

VS Code를 사용한다면 Live Server 확장으로 실행해도 됩니다.

## 이미지 넣는 방법

이미지 파일이 없어도 사이트에는 회색 placeholder 박스가 표시됩니다. 아래 파일명으로 이미지를 넣으면 자동으로 실제 이미지가 표시됩니다.

- 프로필 사진: `images/profile.jpg`
- 첫 번째 프로젝트 사진: `images/project-1.jpg`
- 두 번째 프로젝트 사진: `images/project-2.jpg`
- 세 번째 프로젝트 사진: `images/project-3.jpg`

다른 파일명을 사용하려면 `index.html`에서 각 `<img src="...">` 경로를 원하는 파일명으로 바꾸면 됩니다.

## 이력서 넣는 방법

Hero 영역의 `이력서 보기` 버튼은 기본적으로 `files/resume.pdf`를 바라봅니다.

1. `files` 폴더를 만듭니다.
2. 이력서 PDF 파일명을 `resume.pdf`로 저장합니다.
3. 다른 파일명을 쓰고 싶다면 `index.html`에서 `href="files/resume.pdf"` 값을 수정합니다.

## GitHub Pages 배포 방법

1. `index.html`, `style.css`, `script.js`, `README.md`, `images/` 폴더를 GitHub 저장소 루트에 올립니다.
   이력서 PDF를 사용한다면 `files/` 폴더도 함께 올립니다.
2. GitHub 저장소에서 `Settings`로 이동합니다.
3. 왼쪽 메뉴에서 `Pages`를 선택합니다.
4. `Build and deployment`의 `Source`를 `Deploy from a branch`로 설정합니다.
5. Branch는 `main`, 폴더는 `/root`로 선택한 뒤 저장합니다.
6. 잠시 후 GitHub Pages 주소로 접속해 배포 결과를 확인합니다.

## 이름, 이메일, GitHub 주소 수정 위치

- 이름과 직무 문구: `index.html`의 Hero 영역
- 자기소개 문구: `index.html`의 About 영역
- 문제 해결 방식: `index.html`의 Process 영역
- 기술 스택: `index.html`의 Skills 영역
- 프로젝트 내용: `index.html`의 Projects 영역
- 대표 프로젝트 상세 설명: `index.html`의 Featured Project 영역
- 이력서 버튼: `index.html`의 Hero 영역에서 `files/resume.pdf`
- 이메일: `index.html`의 Contact 영역에서 `your-email@example.com`
- GitHub 주소: `index.html`의 Contact 영역에서 `https://github.com/your-github-id`
- 색상과 간격: `style.css`의 `:root` 변수

## 작성 전 체크리스트

이 포트폴리오는 베이스 템플릿이므로 실제 제출 전 아래 항목을 채워 넣는 것을 권장합니다.

- 이름과 직무 문구가 현재 지원 방향과 맞는지 확인
- `your-email@example.com`을 실제 이메일로 변경
- `https://github.com/your-github-id`를 실제 GitHub 주소로 변경
- `files/resume.pdf` 위치에 실제 이력서 PDF 추가
- `images/profile.jpg` 위치에 프로필 사진 추가
- `images/project-1.jpg`, `images/project-2.jpg`, `images/project-3.jpg` 위치에 프로젝트 사진 추가
- 프로젝트 제목과 설명을 실제 경험으로 교체
- 프로젝트 결과 지표를 가능한 숫자로 작성
- Featured Project를 면접에서 설명할 대표 프로젝트 하나로 구체화
- 배포 전 PC와 모바일 화면에서 레이아웃 확인

## 취업용 구성 방향

이 사이트는 학습 기록을 길게 나열하기보다, 채용자가 빠르게 판단할 수 있도록 아래 흐름으로 구성되어 있습니다.

1. Hero에서 이름, 직무, 이력서, 프로젝트 링크를 먼저 보여줍니다.
2. About과 Process에서 문제 정의, 검증, 자동화로 이어지는 해결 방식을 간결하게 설명합니다.
3. Skills에서 소프트웨어/자동화와 시스템/하드웨어 역량을 간결하게 보여줍니다.
4. Projects에서 여러 경험을 짧게 요약합니다.
5. Featured Project에서 대표 프로젝트 하나를 깊게 설명합니다.
6. Contact에서 이메일과 GitHub로 연결합니다.
