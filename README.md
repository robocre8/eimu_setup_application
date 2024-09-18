# Easy IMU (eimu) Setup Application
this is the source code of the Easy IMU GUI application. The application requires that you have the **`MPU9250 EIMU Module`** (i.e the **Easy IMU Module**) and is connected to your PC via USB serial communication. 

>> **NOTE**: Without the module, only the start page can be viewed.

## Running the GUI app (Using python virtual environment)
### Prequisite
- This would run on linux (ubuntu), windows, and MAC

- For Windows and Mac Users, ensure that you have the **`CH340 serial converter`** or the **`FTDI`** driver installed. (depending on the module you are using)

- Ensure you have `python3` installed on your PC and also `pip`

- install python virtual environment
  ```shell
    pip3 install virtualenv   //linux or mac
  ```
  ```shell
    pip install virtualenv   //windows
  ```
- Ensure you have the **`Easy IMU Module`** connected to the PC.


### Run App First Time [ linux or mac ]
- Download (by clicking on the green Code button above) or clone the repo into your PC using **`git clone`**

- change directory into the root **`eimu_setup_application`** folder

- create a python virtual environment named **`.env`** in the root folder 
	```shell
    python3 -m venv .env
  ```
- activate the virtual environment
  ```shell
    source .env/bin/activate
  ```
- you should see now that you are in the **`.env`** virtual environment

- install all required python modules
  ```shell
    pip3 install -r requirements.txt
  ```
- now you can run the app [follow the [blog tutorial]() on how to calibrate and setup the **Easy IMU Module**]
  ```shell
    python3 app.py 
  ```
- once you are done using the application, just close and dectivate the environment
  ```shell
    deactivate
  ```

### Run App [ linux or mac ]
- change directory into the root **`eimu_setup_application`** folder

- activate the virtual environment
  ```shell
    source .env/bin/activate
  ```
- you should see now that you are in the **`.env`** virtual environment

- now you can run the app [follow the [blog tutorial]() on how to calibrate and setup the **Easy IMU Module**]
  ```shell
    python3 app.py 
  ```
- once you are done using the application, just close and dectivate the environment
  ```shell
    deactivate
  ```

### Run App First Time [ Windows ]
- Download (by clicking on the green Code button above) or clone the repo into your PC using **`git clone`**

- change directory into the root **`eimu_setup_application`** folder

- create a python virtual environment named **`.env`** in the root folder 
	```shell
    python3 -m venv .env
  ```
- activate the virtual environment
  ```shell
    env/Scripts/activate.bat //In CMD  or
    env/Scripts/Activate.ps1 //In Powershel
  ```
- you should see now that you are in the **`.env`** virtual environment

- install all required python modules
  ```shell
    pip install -r requirements.txt
  ```
- now you can run the app [follow the [blog tutorial]() on how to calibrate and setup the **Easy IMU Module**]
  ```shell
    python app.py 
  ```
- once you are done using the application, just close and dectivate the environment
  ```shell
    deactivate
  ```

### Run App [ Windows ]
- change directory into the root folder **`eimu_setup_application`**

- activate the virtual environment
  ```shell
    env/Scripts/activate.bat //In CMD   or
    env/Scripts/Activate.ps1 //In Powershel
  ```
- you should see now that you are in the **`.env`** virtual environment

- now you can run the app [follow the [blog tutorial]() on how to calibrate and setup the **`Easy IMU Module`**]
  ```shell
    python app.py 
  ```
- once you are done using the application, just close and dectivate the environment
  ```shell
    deactivate
  ```