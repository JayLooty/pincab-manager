<p align="center">
  <img src="resources/img/pincab_manager.png" alt="Pincab Manager" width="480"/>
</p>

# pincab-manager

Project to manage my Pincab

## Packaging

```bash
raw_version=$(head -n 1 CHANGELOG | awk '{print $1}')
version="${raw_version#R}"
pyinstaller --name "pincab-manager-${version}" --onefile --noconsole --icon=resources/img/pincab.ico pincab-manager.py --add-data "libvlccore.dll:." --add-data "libvlc.dll:." --add-data "plugins:plugins" --add-data "resources:resources" --add-data "binaries:binaries" --add-data "CHANGELOG:." ; rm -Rf build ; rm pincab-manager-*.spec
```

## Install

Install :
- **vlc** (necessary to play media)
- **python3**
- **TKINTER** with following commands:
```bash
sudo apt update
sudo apt install python3-tk
```
- **requirements** using **pip3**:
```bash
pip3 install -r requirements
```

## Testing locally

To analyze your code, use  `find . -iname "*.py" -not -path "./.venv/*" | xargs pylint` command.

## Usage

To show the menu, type following command:

```bash
python3 pincab-manager.py
```

Use the arguments -s or --simulated to activate simulation for the application

## To update DOF Config

- Go to the website http://configtool.vpuniverse.com/ 
- Click on **Generate Config**
- Move generated files in **Z:/data/configs/pincab-manager/database/pincab11/common/32 bits/dof/DirectOutput/Config**
- Copy content from **Z:/data/configs/pincab-manager/database/pincab11/common/32 bits/dof/DirectOutput/Config/directoutputconfig8.ini** in **Z:/data/configs/pincab-manager/database/pincab11/common/32 bits/dof/DirectOutput/Config/directoutputconfig.ini** 
- Move generated files in **Z:/data/configs/pincab-manager/database/pincab11/common/64 bits/dof/DirectOutput/Config**
- Copy content from **Z:/data/configs/pincab-manager/database/pincab11/common/64 bits/dof/DirectOutput/Config/directoutputconfig8.ini** in **Z:/data/configs/pincab-manager/database/pincab11/common/64 bits/dof/DirectOutput/Config/directoutputconfig.ini** 
- Update project using **git add**, **git commit** and **git push**
- From the pincab, update the project using **git pull** then install **Configs files / DirectOuput / 32 Bits** and **Configs files / DirectOuput / 64 Bits**
- Execute in **Admin Mode** the executable **C:\DirectOutput\RegisterDirectOutputComObject.exe**

## To add a table for any emulator

- Create a directory **<table_version>** in the folder **Z:/data/tables/<emulator_name>**
- Create a sub directory **emulator** containing the emulator files 
- Create a sub directory **media** containing the media files
- Create a sub directory **PUPVideos** containing the PinUP Popper videos files
- Add a record in the file **Z:/data/configs/pincab-manager/database/<host_name>/<emulator_name>/tables.csv** with following columns:
    - **AVAILABLE**: with the value **YES** if the table has to be visible in PinUP Popper
    - **VERSION**: latest version to import
    - **NAME**: Display name for the table
    - **ID**: Unique ID for the table
    - **ALT_EXE**: Alternative executable to run the table
    - **ALT_RUN_MODE**: Alternative mode to run the table
    - **ROM**: Name for the rom
    - **VIDEOS_PATH**: Path for the PinUP Popper videos
    - **WEBLINK_URL**: First link to retrieve the table
    - **WEBLINK2_URL**: Second link to retrieve the table
- Go to the directory **Z:/data/configs/pincab-manager** then type the command **git pull**
- Install the specific table using the command **python3 pincab-manager.py**
- Save a copy of the CSV files with the commands **git add**, **git commit** and **git push**

**N.B.**: For the emulator **Visual Pinball X**, you can use the command **"<visual_pinball_exe>" -Minimized -ExtractVBS "<vpx_file_path>"** to generate the script where you can extract the rom's name in the variable **cGameName** and the videos path in the variable **cPuPPack** (or **cGameName** if this variable doesn't exist)

For example: **"c:\vPinball\VisualPinball\VPinballX10_7_3_32bit.exe" -Minimized -ExtractVBS "Z:\tables\Visual Pinball X\Gardiens de la galaxie\2.1.0\emulator\Tables\Gardiens de la galaxie.vpx"**

**N.B.**: For the emulator **Future Pinball**:
- the tables containing PuP-Pack are identified by **PinEvent**. **Z:\configs\32 bits\future_pinball\vPinball\FuturePinball** is retrieved from https://vpuniverse.com/files/file/14807-future-pinball-and-bam-essentials-all-in-one-complete/. 
- disable the option use_RayCast_Shadows from the script in the file .fpt to override
- by option Q, set table X and z to 0.0, scale Z to 1.500 and angle rotation to 0.00 deg 