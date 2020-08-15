## Deploy to exe	
```	
conda install -c conda-forge pyinstaller	
conda install -c anaconda pywin32	
pyinstaller --add-binary "C:\Users\cqiu\Desktop\projects\teradata-migration\teradata_trace\automation\env\Lib\site-packages\teradatasql;teradatasql" --onefile --icon=trace_shoe.ico automate_trace.py	

# reducing size by upx
pyinstaller automate_trace.py --upx-dir=.\upx-3.96-win64 -y --onefile
```

## setup env to reduce size

https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

### On macOS and Linux:

```
python3 -m venv env
```
### On Windows:

```
python -m venv env
or
py -m venv env (be careful this might still be using anaconda's python)
```

### On macOS and Linux:
```
source env/bin/activate
```

### On Windows:

```
.\env\Scripts\activate
```

#### You can confirm you’re in the virtual environment by checking the location of your Python interpreter, it should point to the env directory.

### On macOS and Linux:
```
which python
.../env/bin/python
```

### On Windows:

```
where python
.../env/bin/python.exe
```

As long as your virtual environment is activated pip will install packages into that specific environment 
and you’ll be able to import and use packages in your Python application.

### Leaving the virtual environment
If you want to switch projects or otherwise leave your virtual environment, simply run:
```
deactivate```