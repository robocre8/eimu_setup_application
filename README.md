## The Easy IMU (eimu) Setup Application
this is the source code of the Easy IMU GUI application. The application requires that you have the **`Easy IMU Module`** (i.e **`MPU9250 EIMU MODULE`**) and is connected to your PC via USB serial communication. 

![eimu_app_pic](https://github.com/user-attachments/assets/49298cc7-6ff2-4856-9e1e-e013d26c66fd)

> [!NOTE]  
> Without the module, only the start page can be viewed.

#

### Running the GUI app (Using python virtual environment)

#

#### Prequisites
- This would run on **Linux (Ubuntu)**, **Windows**, and **MAC OS**

> [!NOTE]  
> For Windows and Mac Users, ensure you have the [**`CH340 serial converter`**](https://sparks.gogo.co.nz/ch340.html?srsltid=AfmBOooJ45evOXTZdp96-_eI1A2xCokPqFyJm0e_Ybx6LOwyY0qJ5Uux) driver installed.
>
> For Ubuntu Users - the **CH340** driver is installed by default.

- Ensure you have `python3` installed on your PC and also `pip`

- install python virtual environment
  > ```shell
  > sudo apt install python3-pip   # linux or mac users
  > sudo apt install python3-venv   # linux or mac users
  > ```
  > *OR*
  > ```shell
  > pip install virtualenv   # windows users (ensure you have pip installed)
  > ```
  
- Ensure you have the **`Easy IMU Module`** connected to the PC.

#

#### Run App First Time [ Ubuntu or Mac Users ]
- Download (by clicking on the green Code button above) or clone the repo into your PC using **`git clone`**
  > you can use this command if you want to clone the repo:
  >
  > ```shell
  > git clone https://github.com/robocre8/eimu_setup_application.git
  > ```

- change directory into the root **`eimu_setup_application`** folder
  > ```shell
  > cd eimu_setup_application/
  > ```

- create a python virtual environment named **`.env`** in the root folder
  > ```shell
  > python3 -m venv .env
  > ```

- activate the virtual environment
  > ```shell
  > source .env/bin/activate
  > ```

- you should see now that you are in the **`.env`** virtual environment

- install all required python modules
  > ```shell
  > pip3 install -r requirements.txt
  > ```

- now you can run the app in the virtual environment
  > ```shell
  > python3 app.py
  > ```

- Now follow this tutorial on [how to calibrate and setup the **Easy IMU Module**](https://robocre8.gitbook.io/robocre8/eimu-tutorials/how-to-calibrate-and-setup-the-eimu)
  
- once you are done using the application, just close and dectivate the environment
  ```shell
    deactivate
  ```

#

#### Run App First Time [ Windows ]
- Download (by clicking on the green Code button above) or clone the repo into your PC using **`git clone`**
  > you can use this command if you want to clone the repo:
  >
  > ```shell
  > git clone https://github.com/robocre8/eimu_setup_application.git
  > ```

- change directory into the root **`eimu_setup_application`** folder
  > ```shell
  > cd .\eimu_setup_application\
  > ```

- create a python virtual environment named **`.env`** in the root folder
  > ```shell
  > python -m venv .env
  > ```

- activate the virtual environment
  > ```shell
  > .\.env\Scripts\activate.bat # In CMD
  > .\.env\Scripts\Activate.ps1 # In Powershel
  > ```

- you should see now that you are in the **`.env`** virtual environment

- install all required python modules
  > ```shell
  > pip install -r requirements.txt
  > ```

- now you can run the app in the virtual environment
  > ```shell
  > python app.py
  > ```

- Now follow this tutorial on [how to calibrate and setup the **Easy IMU Module**](https://robocre8.gitbook.io/robocre8/eimu-tutorials/how-to-calibrate-and-setup-the-eimu)
  
- once you are done using the application, just close and dectivate the environment
  > ```shell
  > deactivate
  > ```
  
#

#### Run App - Not As First Time [ Ubuntu or Mac Users ]
- change directory into the root **`eimu_setup_application`** folder
  > ```shell
  > cd eimu_setup_application/
  > ```

- activate the virtual environment
  > ```shell
  > source .env/bin/activate
  > ```

- you should see now that you are in the **`.env`** virtual environment

- now you can run the app in the virtual environment
  > ```shell
  > python3 app.py
  > ```

- Now follow this tutorial on [how to calibrate and setup the **Easy IMU Module**](https://robocre8.gitbook.io/robocre8/eimu-tutorials/how-to-calibrate-and-setup-the-eimu)
  
- once you are done using the application, just close and dectivate the environment
  ```shell
    deactivate
  ```

#

#### Run App - Not As First Time [ Windows ]

- change directory into the root **`eimu_setup_application`** folder
  > ```shell
  > cd .\eimu_setup_application\
  > ```

- activate the virtual environment
  > ```shell
  > .\.env\Scripts\activate.bat # In CMD
  > .\.env\Scripts\Activate.ps1 # In Powershel
  > ```

- you should see now that you are in the **`.env`** virtual environment

- now you can run the app in the virtual environment
  > ```shell
  > python app.py
  > ```

- Now follow this tutorial on [how to calibrate and setup the **Easy IMU Module**](https://robocre8.gitbook.io/robocre8/eimu-tutorials/how-to-calibrate-and-setup-the-eimu)
  
- once you are done using the application, just close and dectivate the environment
  > ```shell
  > deactivate
  > ```

#

#### Build eimu_app with pyinstaller [Linux or Mac]

- change directory into the root **`eimu_setup_application`** folder
  > ```shell
  > cd eimu_setup_application/
  > ```

- activate the virtual environment
  > ```shell
  > source .env/bin/activate
  > ```

- you should see now that you are in the **`.env`** virtual environment

- build the application with pyinstaller:
  > ```shell
  > pyinstaller app.py --onefile --name eimu_app_ubuntu_<OS-version-number> --hidden-import='PIL._tkinter_finder'
  > ```
  > OR
  > ```shell
  > pyinstaller app.py --onefile --name eimu_app_mac_<OS-version-number> --hidden-import='PIL._tkinter_finder'
  > ```

#

#### Build eimu_app with pyinstaller [Windows]

- change directory into the root **`eimu_setup_application`** folder
  > ```shell
  > cd .\eimu_setup_application\
  > ```

- activate the virtual environment
  > ```shell
  > .\.env\Scripts\activate.bat # In CMD
  > .\.env\Scripts\Activate.ps1 # In Powershel
  > ```

- you should see now that you are in the **`.env`** virtual environment

- build the application with pyinstaller:
  > ```shell
  > pyinstaller app.py --onefile --name eimu_app_windows_<OS-version-number> --hidden-import='PIL._tkinter_finder'
  > ```
  
- once you are done, close and dectivate the environment
  > ```shell
  > deactivate
  > ```
