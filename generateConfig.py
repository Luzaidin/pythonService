import configparser

# CREATE OBJECT
config_file = configparser.ConfigParser()

# LOGGER SECTION AND SETTINGS
config_file["Logger"]={
        "LogFilePath":"./app.log",
        "LogLevel" : "Info",
        "LogFormat": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }

# EMAIL SECTION AND SETTINGS
config_file["Email"]={
        "EmailSubject":"Test",
        "EmailTemplate":"./email.html",
        "EmailLogo":"./img/logo.jpg"
        }

# SAVE CONFIG FILE
with open(r"configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

print("Config file 'configurations.ini' created")

# PRINT FILE CONTENT
read_file = open("configurations.ini", "r")
content = read_file.read()
print("Content of the config file are:\n")
print(content)
read_file.flush()
read_file.close()