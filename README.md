<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1 align="center">AIVA 2022 - Grupo D</h1>

  <h3 align="center">
    Control de visitantes de una tienda 
    <br />
  </h3>
</div>

<!-- ABOUT THE PROJECT -->
## Resumen del proyecto

![product-screenshot](./resources/tienda.png)

Un cliente tiene una cámara apuntando a la puerta de su tienda y desea obtener unas estadísticas. Nos pide obtenerlas y para ello vamos a intentar resolver el problema gracias a inteligencia artificial, en concreto visión por computador al trabajar sobre imágenes.

Las estadísticas a obtener son:
* Cuantas personas entran y salen

![product-screenshot](./resources/entran_salen.png)

* Cuantos pasan de largo

![product-screenshot](./resources/pasan.png)

* Cuantos se quedan mirando al escaparate

![Product Name Screen Shot](./resources/escaparate.png)

<p align="right">(<a href="#top">back to top</a>)</p>



### Hecho con

* [OpenCV](https://opencv.org/)
* [PyTorch](https://pytorch.org/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Primeros pasos


### Instalación

1. Clonar el repo
   ```sh
   git clone https://github.com/desertclaw9/AIVA_2022_GrupoD.git
   ```
   
 2. Crear virtual environment (probado sobre python3.8)
    ```sh
    cd AIVA_2022_GrupoD
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
     ```

 3. Instalar requirements
     ```sh
     pip install -r requirements.txt
     ```

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
### Uso
Para usar la aplicación ejecutar el siguiente comando:
```sh
python3 src/Main.py
```
Se empezarán a procesar los videos y mostrar el resultado por pantalla. Para controlar el flujo de archivos,
pulsar 'n' para ir al siguiente video y pulsar 'q' para salir. 

Al terminar cada video se imprimirá por consola las estadísticas requeridas por la aplicación.
<p align="right">(<a href="#top">back to top</a>)</p>

### Testing
Para ejecutar todos los test, ejecutar el siguiente comando:
```sh
python3 -m unittest discover
```
Se recomienda usar un visualizador de unittest como el de pycharm para una visualización más cómoda.

<p align="right">(<a href="#top">back to top</a>)</p>

## Despliegue
Se ha empaquetado la solución para la correcta y simple ejecución por parte del cliente.

1. Descargar la imagen del docker con el siguiente comando desde la consola de comandos (tanto en windows como linux)
```sh
docker pull carlossab/aiva_2022_grupod:latest
```

2. Ejecutar el contenedor (o imagen) y en << path >> poner la carpeta base donde se encuentra el video o videos a procesar.
```sh
docker run --name=ControlVisitantes -v <<path>>:/app/dataset_2 -e PYTHONUNBUFFERED=1 carlossab/aiva_2022_grupod:latest
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] Tarea 1: Requisitos
  - [x] Captura de requisitos
  - [x] Creación de Github
  - [x] Mockup sistema
  - [x] Pruebas Unitarias
- [x] Tarea 2: Piloto
  - [x] Creación primer diseño
  - [x] Documentación
  - [x] Pruebas unitarias
- [x] Tarea 3: Resultados
  - [x] Integración aplicación
  - [x] Despliegue  
  - [x] Documentación 
- [ ] Tarea 4: Presentación
  - [ ] SonarQube

Ver [issues](https://github.com/desertclaw9/AIVA_2022_GrupoD/issues) para una lista de todos los issues. 

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contacto

Ignacio García-Siñeriz Sánchez - i.garciasan.2021@alumnos.urjc.es

Carlos Sabater Nicolás - c.sabater.2021@alumnos.urjc.es

Alonso Cerrato Nieto - a.cerrato.2021@alumnos.urjc.es

Project Link: [https://github.com/desertclaw9/AIVA_2022_GrupoD](https://github.com/desertclaw9/AIVA_2022_GrupoD)

<p align="right">(<a href="#top">back to top</a>)</p>
