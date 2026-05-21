# Kiwoom REST API 자동매매 준비

맥에서 키움 REST API로 실전 프로그램매매를 시작하기 위한 최소 프로젝트입니다.

> 본 프로젝트는 학습 및 개인 자동화 실험용입니다. 실거래 사용에 따른 손실과 책임은 사용자 본인에게 있습니다.

## 1. 키움 포털에서 먼저 할 일

1. 키움 REST API 사이트에서 API 사용신청
2. 실전투자 App Key와 App Secret 발급
3. 사용할 공인 IP 등록
4. 계좌 등록 및 SMS 인증

공식 안내: https://openapi.kiwoom.com/intro/serviceInfo

## 2. 로컬 설정

```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`.env`에 실전투자용 `KIWOOM_APP_KEY`, `KIWOOM_SECRET_KEY`를 넣습니다.
실전 서버를 쓰려면 `KIWOOM_ENV=real`이어야 합니다.

## 3. 토큰 발급 확인

```bash
python -m kiwoom_bot token
```

성공하면 `.kiwoom_token.json`에 토큰이 저장됩니다. 토큰은 보통 24시간 단위로 갱신해야 합니다.

## 4. 실전 주문 안전장치

이 프로젝트는 기본적으로 주문을 막아둡니다.

```bash
KIWOOM_ALLOW_ORDERS=false
```

토큰 발급, 계좌조회, 잔고조회, 미체결조회, 체결 이벤트까지 확인한 뒤에만 아래처럼 바꾸세요.

```bash
KIWOOM_ALLOW_ORDERS=true
```

## 5. GitHub 연결

GitHub에서 빈 저장소를 만든 뒤, 아래 명령으로 연결합니다.

```bash
git remote add origin https://github.com/YOUR_ID/YOUR_REPOSITORY.git
git add .gitignore .env.example README.md requirements.txt kiwoom_bot
git commit -m "Set up Kiwoom REST API starter"
git push -u origin main
```

`.env`와 `.kiwoom_token.json`은 민감정보라 `.gitignore`에 포함되어 있습니다. GitHub에 올리지 마세요.
