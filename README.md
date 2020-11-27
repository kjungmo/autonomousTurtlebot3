# autonomousTurtlebot3
 Turtlebot3 Lane Tracing & Traffic sign classification using openCV and Tensorflow

# 프로젝트 개요
본 프로젝트는 서울산업진흥원 주관 한성대학교 산학협력단의 4개월 과정인 (2020.07.20 - 2020.11.13) 딥러닝 기술을 이용한 영상처리 응용 프로젝트 개발과정에서 진행되었다.  
프로젝트의 목표는 자율주행 구현을 위해 차선 내 자율 주행 및 영상 데이터 프레임의 표지판을 인식하여 라벨에 따라 주행변화를 주고자 하는 것이었다. 
다만 광각카메라, 라이더 및 초음파 센서가 없어 단일 Pi Camera 및 라즈베리 파이 3 B+ 로 간소하게 진행했다.  
하지만 주목해야할 점은 메타 운영체제인 ROS를 사용하고, 지급받은 라즈베리 파이 3 B+의 낮은 컴퓨팅파워로도 두 가지 기능(차선 내 주행 및 이미지 인식)을 수행했다는 점이다. 이는 하드웨어 업그레이드를 통한 기술 정교화의 토대를 마련했다는 점에서 해당 프로젝트에 의미가 있다. 


1-1 배경

딥러닝 영상처리 기술과 자율주행이 4차 산업시대에 걸맞는 기술 트렌드로 주목을 받는 가운데, 둘을 접목시킨 자율주행 시스템에 대하여 효용성이 있음을 판단하고 프로젝트를 진행했다.

1-2 목적

Turtlebot3 Waffle Pi라는 소형 자동차 모듈에 컴퓨터비전과 딥러닝 기술을 이용하여 차선검출, 딥러닝을 이용한 표지판 분류와 같은 기능을 통해 자율주행을 구현하고자 하였다.

파이카메라로 읽은 영상데이터를 기반으로 전처리하고, 전처리된 데이터를 알고리즘을 통해 최종적으로 기기의 움직임을 제어할 수 있도록 한다.

1-3 효용가능성

실제 도로와 유사한 환경의 모형 트랙을 개발하고 테스트를 진행했다. 해당 모델이 적용되는 기기의 크기가 더 커지더라도 그 기기와 기기가 운용되는 상황에 맞게 시스템을 조정하여 사용할 수 있는 토대를 만들었다고 판단된다.

* 주행 동영상 삽입 또는 링크
*  코드 해설? 이거 할까 말까

## 환경 구성
각각에 ROS 1 / Python 2.7 / OpenCV 3.3.1 / Tensorflow 1.8.0
설치
### Remote PC
Virtual Box에 Ubuntu 16.04 LTS 설치
### 라즈베리 파이 3 B+ (Turtlebot 3 Waffle Pi)
Raspbian Stretch OS  설치

### Remote PC 에서 라즈베리 파이로 접속
ssh 접속을 통해  리모트 PC가 터틀봇의 라즈베리 파이 보드에 접속한다. 

코드 구동 순서 
1. REMOTE PC에서 roscore 실행
2. 라즈베리 파이에서 roslaunch turtlebot3_bringup turtlebot3_robot.launch 와  roslaunch turtlebot3_camera turtlebot3_rpicamera.launch 실행
3.
	- 주행을 위해서는 라즈베리 파이에서 lane_drive.py 파일 실행
	- Traffic Sign Classification 을 위해서는 classify.py 파일 실행
---------


2. 개발 환경

2-1 하드웨어 구성

프로젝트를 진행한 모델은 robotis Turtlebot3 Waffle Pi 모델이지만 Burger형태로 개조했다. 구성 스펙은 아래와 같다.

![image](https://github.com/kjungmo/autonomousTurtlebot3/blob/main/1.png)



특징 : 본 프로젝트에서 카메라는 라이다의 앞부분(4층)에 위치해있다. Picamra브라켓의 각도가 90º 이지만, 차선과 표지판을 원활히 검출하기 위해 40º를 줄여서 지면으로부터 50º의 각도로 장착하였다. 기존 90º 에 비해 인식범위의 사각지대가 줄어든 것을 확인 했다.

![image](https://github.com/kjungmo/autonomousTurtlebot3/blob/main/2.png)


Raspberry pi 3 Model B

라즈베리파이는 기기에서 메인 컨트롤 역할을 맡게 되며 컴퓨팅 파워를 담당한다. Open CR, Picamera와 연결이 되어있고 Remote PC와 통신을 통해 각 구성요소들에 명령을 전달한다.

Raspberry Pi camera module V2

본 프로젝트에서는 오로지 컴퓨터 비전을 통해 데이터의 수집 및 전처리를 진행한다. Picamera 로 촬영한 이미지 데이터를 raspberry pi 내에서 사용한다.

Open CR 1.0

구동부인 모터(DYNAMIXEL XM430)와 연결되어 모터에 명령을 전달하는 역할을 한다.


2-2 소프트웨어
Remote PC의 경우 가상환경(Virtual Box)에 Ubuntu 16.04 LTS를 설치  
 라즈베리파이의 경우 Raspbian Stretch OS 를 설치
 Python의 경우 2.7, openCV의 경우 3.3.1, Tensorflow 1.8.0, Keras 2.2.4를 설치 
 메타운영체제인 ROS 는 ROS1을 설치

2-3 ROS

(1)개요

Remote PC, SBC, Open CR 사이에서 통신명령을 전달하는 시스템. msg 방식을 통해 각 노드간의 명령을 전달하며 publisher와 subscriber로 나뉜다.

(2)구조

ROS는 각 구성요소의 OS 위에 얹어지며 다른 이종기기 간 통신의 주체가 된다.

Raspberry pi 에서는 raspbian의 위에, Remote PC에서는 Ubuntu의 위에, OpenCR에서는 바로 보드에 얹어져서 노드를 생성하고 msg통신을 통해 각 기기간 명령 정보를 전달한다.


(3)역할

모터인 dynamixel에 접근을 위해 ros시스템을 호출해줘야한다. velocity publisher를 통해 모터제어 명령을 전달하고 컨트롤 하게된다.

파이 카메라 또한 raspicam_node에서 publisher로서 영상 데이터를 subscriber인 라즈베리 파이 보드로 전송한다.

이는 remote pc에서 전달된 명령이 SBC와 OpenCR을 거쳐 최종적으로 모터 제어에 영향을 끼칠 수 있게 된다.

python 내에서는 rospy 모듈을 통해 .py 파일과의 연결점이 생성되며 python 내에서 ros 의 publisher 와 subscriber를 호출 할 수 있도록 하는 역할을 한다.

실제로 py 파일을 실행 시켰을 때 파일 내의 publisher로 호출한 모터의 파라미터 제어가 실제 구동시에 영향을 끼침을 통해 알 수 있다.

2-4. 트랙 구성

![image](https://github.com/kjungmo/autonomousTurtlebot3/blob/main/3.png)

트랙의 구성은 좌측 황색, 우측 백색의 두 차선으로 구성되어 있으며, 트랙이 계속 이어지는 순환형 형태를 띄고 있다.
긴 직진구간, 코너구간, 짧은 직진구간의 형태를 띄고 있으며 차선 2cm 차선 폭 7cm으로균일한 너비의 트랙이다.


3. 기능구현 – 차선검출 & 주행

3-1. 차선 검출 방법

![image](https://github.com/kjungmo/autonomousTurtlebot3/blob/main/4.png)

HSV 색 공간으로 변환된 이미지에 대해 트랙 차선이 들어오도록 ROI영역을 설정하고 mask를 씌워 이진화

mask는 yellow lane / white lane을 각각 검출하기 위하여 2가지 사용

![image](https://github.com/kjungmo/autonomousTurtlebot3/blob/main/5.png)

ROI영역 안에 라인이 검출된다면 흰색으로 표시되고,
영역 안에 라인이 검출되지 않는다면 검은색으로 표시된다.

이는 openCV의 createLineSegmentDetect()라는 모듈을 통해서 Contour 검출을 하게 된다. 따라서 ROI 영역 안에 이진화된 차선이 검출되면 Contour가 카운팅 되고, 이를 통해 조건문에서 각 조건에 따른 코드를 실행시킨다.

![image](https://github.com/kjungmo/autonomousTurtlebot3/blob/main/6.png)


3-2. 모터제어와 주행

터틀봇의 주행은 linear.x, angular.z 값을 이용한 모터제어를 통해 구현된다

linear.x 값이 + 값일 때 앞으로 주행하고 – 값일 때 뒤로 주행한다.

angular.z값이 + 값일 때 왼쪽으로 회전하고 – 값일 때 오른쪽으로 회전한다.

트랙의 사이즈와 곡률에 맞춰 다양한 시도 끝에 다음과 같이 모터제어 값을 설정하였다.

직진 linear.x : 0.12  angular.z : 0.0

좌회전 linear.x : 0.08  angular.z : 0.25

우회전 linear.x : 0.08  angular.z : -0.25



주행은 3-1에서 검출한 차선의 contour 유.무에 의해 결정된다.


![image](https://github.com/kjungmo/autonomousTurtlebot3/blob/main/7.png)




4. 기능구현 – 딥러닝을 활용한 표지판 인식



4-1. 데이터 수집 및 분석

![image](https://github.com/kjungmo/autonomousTurtlebot3/blob/main/8.png)

실제 주행 중 Pi카메라를 통해 1분13초동안 60fps로 촬영해서 데이터 4068장을 수집했다. 이 중 확실한 corner, straight, stop sign detection에 대해서 각각 500장으로 개수가 줄었다. 그 후 데이터 증강을 통해 총 데이터 수를 45000장으로 증가시켰다.


4-2. 모델 설계 및 채택이유


증강한 데이터에 대해서 레이어 4개짜리 CNN모델을 만들어서 학습시켰다. CNN모델은 컨볼루션 연산을 통해 이미지 특징점을 잡는 방식이고, YOLO의 경우  본 프로젝트의 SBC에서 사용하기에  컴퓨팅 파워가 부족했다. 
그 때문에 표지판 인식을 위해 CNN모델을 사용하게 되었다.



CNN 모델의 경우에 레이어를 늘려가며 정확도를 비교했다. 레이어의 개수가 1, 2, 3, 4일때, 모델 로드 후 예측까지 걸리는 시간은 0.22초 정도로 모두 비슷했지만, 레이어 수가 4개일 때 정확도가 99.54%로 가장 높았기 때문에 4개짜리 레이어 모델을 채택했다.

![image](https://github.com/kjungmo/autonomousTurtlebot3/blob/main/9.png)

결과적으로 다음과 같은 모델을 구현하였다.

![image](https://github.com/kjungmo/autonomousTurtlebot3/blob/main/10.png)

4-3 프로세스

파이카메라에서 받은 이미지 데이터를 CNN모델의 Input data로 사용하고 그 결과 ‘Stop’ , ‘Straight’, ‘Corner’의 세가지로 분류한다. 그에 따라 분류된 라벨 값을 터미널에  출력되도록 했다.



5.한계점 및 향후계획

프로젝트 초기 기능구현 계획은 한 번에 두 기능 실행을 목표로 하였다. 
먼저 알고리즘을 이용하여 라인을 인식해 차선 내 자율주행하는 것이었다.
이와 동시에 표지판을 인식해 표지판을 분류해내고 표지판에 따라 정지, 속도제한, 좌.우회전을 인식하여 주행상태 변화로 이어지는 기능을 구현하는 것이었다.
하지만 라즈베리파이의 제한적인 컴퓨팅파워에 의해 프로젝트 초기 계획했던 기능 구현이 불가능하다는 하드웨어적 한계가 있었다. 이 때문에 각각의 기능을 따로따로 구현하였으나 2개의 라즈베리 파이를 사용하거나 보드 업그레이드를 통해 완성도 높은 결과를 도출할 수 있을 것으로 기대된다. 두 기능을 동시에 구현한 후에는 트랙의 복잡도를 높여 랜덤하게 표지판을 보여주면 그에 따라 다른 방식으로 트랙을 주행하는 터틀봇의 모습 또한 보여줄 수 있다고 생각한다.
