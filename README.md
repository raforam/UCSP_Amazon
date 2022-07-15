# PROYECTO
Para este proyecto se usó: python 3.9.7 pero versiones nuevas funcionan igualmente.

## Pasos para Ejecutar el proyecto
- Crear un entorno virtual
- Después de activar el entorno virtual debe instalar los modulos desde poetry
``` 
poetry update
```
- Debe configurar el puerto, usuario y contraseña de la base de datos en el archivo .env (variables de entorno en desarrollo) Por defecto los datos de .env son 'DATABASE_USER=root', 'DATABASE_PASSWORD=ucspucsp' y 'DATABASE_DB=amazon'
- Opcionalmente, hay un script llamado crear_base.py que le permitira crear las tablas de este proyecto, 
  no olvide que para esto ha tenido que crear su base de datos y especificarla en el archivo .env
- ejecutar:
```
SET FLASK_APP=main.py
flask run
```

# ¡Disfrute del programa!
