# API-FastAPI
Intento de Fast API


 ## Version de python
  3.7.2
 # Instalación local  

## 1. Crear un entorno virtual para la instalación de las librerias

~~~bash  
   python -m venv venv
~~~
o bien  

~~~bash  
   python3 -m venv venv
~~~

    
## 2. Ingresar al enntorno virtual:

#### Linux:

~~~bash 
    source venv/bin/activate
~~~

#### Windows:

~~~bash  
    .\venv\Scripts\activate.bat
~~~
 o bien 

~~~bash  
    .\venv\Scripts\activate  
~~~

## 3. Instalar las librerias necesarias que se encuentran en el archivo "requirements.txt"

~~~bash  
     pip install -r requirements.txt
~~~

o bien 

~~~bash  
    pip3 install -r requirements.txt
~~~

En caso de no funcionar se puede instalar las librerias principales:

- `uvicorn`
- `fastapi`
- `python-dotenv`
- `SQLAlchemy`
- `PyMySQL`
- `cryptography`
- `pydantic[email]`
- `Werkzeug`
- `pyjwt`
- `face-recognition`
- `opencv-python`
- `keras`
- `tensorflow`
- `python-multipart`
- `webdriver_manager`


   
## 4. Ejecutar la API

~~~bash  
    uvicorn main:app --reload
~~~


# Crear imagen Docker de con Automation Documents


## Construir la imagen apartir del archivo `Dockerfile`
~~~bash  
   sudo docker build -t automation-documents:0.1 .
~~~

## Verificar que se creó correctamente

~~~bash  
   sudo docker images
~~~

## Correr imagen creada 

~~~bash
    sudo docker run --publish 1001:1001 --detach --name api-automation-documents automation-documents:0.1 
~~~


# En caso de no contar con MySQL instalado

## Creamos un volumen para la persistencia de datos

~~~bash
    sudo docker volume create mysql-db
~~~

## Verificamos que se haya creado el volumen

~~~bash
    sudo docker volume ls
~~~

## Correr imagen de mysql asignando la contraseña

~~~bash
    sudo docker run -d -p 3306:3306 --name mysql-db-container  -e MYSQL_ROOT_PASSWORD=Password.1 --mount src=mysql-db,dst=/var/lib/mysql mysql
~~~

## Ingresar al gestor de base de datos para crear la base de datos

~~~bash
    sudo docker exec -it mysql-db-container  mysql -p
~~~

