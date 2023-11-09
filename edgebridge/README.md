# Hass.io Add-on: Bridge Server for SmartThings Edge drivers 

![Supports aarch64 Architecture][aarch64-shield] ![Supports amd64 Architecture][amd64-shield] ![Supports armhf Architecture][armhf-shield] ![Supports armv7 Architecture][armv7-shield] ![Supports i386 Architecture][i386-shield]

## About
Bridge Server(이후 '서버'라고 함)는 (1) LAN 외부의 대상으로 HTTP 요청을 보내거나 (2) HTTP 요청을 수신할 수 있어야 하는 SmartThings Edge 드라이버의 동반자로 설계되었습니다. LAN 기반 장치 및 애플리케이션에서 발행된 임시 HTTP 메시지.

서버 자체는 '항상 켜져 있는' Windows/Linux/Mac/Raspberry Pi 컴퓨터에서 실행할 수 있는 단순한 Python 스크립트입니다. 서버는 3.7x Python 소스 스크립트, Windows 실행 프로그램 파일 또는 Raspberry Pi OS 실행 프로그램 파일(32비트 및 64비트)로 제공됩니다. 사용자가 만든 선택적 구성 파일을 읽을 수 있습니다(아래 참조).

## Installation

1. 홈어시스턴트의 Hass.io > ADD-ON STORE에서 Add new repository by URL에 https://github.com/clipman/HomeAssistant 를 입력한 다음 ADD 버튼을 누릅니다.
2. ADD-ON STORE 페이지 하단에서 "Bridge Server" 클릭합니다.
3. "INSTALL" 버튼을 누르면 애드온이 설치됩니다. 최대 약 10분 정도 소요. 
4. INSTALL 버튼위에 설치 애니메이션이 동작하는데 이것이 멈추더라도 REBUILD, START 버튼이 나타나지 않는 경우가 있습니다.
5. 이 애드온은 이미지를 내려받는 것이 아니라 직접 여러분의 Hassio에서 이미지를 만듭니다.
6. INSTALL 버튼을 누른다음 설치 애니메이션이 실행되면 제대로 설치중인 것입니다.
7. share/edgebridge/ 폴더에 있는 edgebridge.cfg 파일을 본인의 환경에 맞게 수정합니다.
8. "START" 버튼으로 애드온을 실행합니다.


[forum]: https://cafe.naver.com/koreassistant
[github]: https://github.com/clipman/addons
[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
