# mcp-adobe
Servidor MCP para interactuar con Adobe

# Preparar entorno

### Crear un entorno virtual de python
```sh
python -m venv venv
```

### Visual code studio
    Ctrl + Shift + P
    Buscar "Python: Select Interpreter"
    Seleccionar el que tiene "venv"

### Activar el entorno virtual
```sh
venv\Scripts\activate
```

## Tabajar con el requirements.txt
### Actualizar el requirements.txt
```sh
pip freeze > requirements.txt
```

### Instalar requerimientos
```sh
pip install -r requirements.txt
```