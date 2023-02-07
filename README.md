# IDM2040-7A-EW2022
The demo applications running on IDM2040-7A for Embedded World 2022 exibition    

![image](https://user-images.githubusercontent.com/13127756/217126707-f9b40f28-f8c2-4580-a13f-614e46b0eaf0.png)


1. The IDM2040-7A is an intelligent display module : see https://brtchip.com/product/idm2040-7a/ for more details

2. LDS SDK firmware: It is a customized circuitPython 7.1.0 run-time built with LDS driver, which shall be the base to run any circuitPython code. It is here:  
      https://github.com/Bridgetek/IDM2040-7A-EW2022/tree/main/LDS_Demo/IDM2040_LDS_SDK_Firmware  
   
   * LDS stands for Long Distance Sensors Bus from Bridgetek, see https://brtsys.com/ldsbus/
   
3. User shall program flash image ["EVE_Flash/BT81X_Flash.bin"](https://github.com/Bridgetek/IDM2040-7A-EW2022/tree/main/EVE_Flash)  into EVE's connected flash with [Eve Asset Builder (EAB)](https://brtchip.com/ic-module/toolchains/).   
4. These example projects depend on the pico-brtEve library   
   https://github.com/Bridgetek/pico-brteve/tree/main/circuitPython/lib/brteve.   
   User shall download it to the folder "lib\brtEve" of ciruitPython drive on your PC when IDM2040 is connected. 
   
5. The following applications are included in this repo: 

![image](https://user-images.githubusercontent.com/13127756/217127490-fb3c0547-5352-4143-9ff9-14cd7b867e6c.png)

