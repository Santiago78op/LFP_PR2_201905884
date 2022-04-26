from flask import Flask, request, Response
from flask import render_template
import pathlib

#app = raiz
app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
def index():
    return '<h1>Hola Mundo!</h1>'


@app.route('/postTablaJornada', methods=['POST'])
def TablaJornada():
    json = request.json

    tabla = json["Jornada"]
    nombre = json["Nombre"]

    JsonImg = {

        'tabla': tabla
    }

    print(JsonImg)
    # Hacer un dict/json que tenga los datos de la tabla a crear

    saveHtmlTablaJornada(nombre, render_template(
        'tabla_jornada.html', **JsonImg))
    return Response()


def saveHtmlTablaJornada(filtro, html):
    pathlib.Path(
        f'Reports/Tables/Jornada').mkdir(parents=True, exist_ok=True)
    with open(f'Reports/Tables/Jornada/{filtro}.html', 'w', encoding="utf-8") as f:
        f.write(html)
        f.close


@app.route('/postTablaTemporada', methods=['POST'])
def tablaTemporada():
    json = request.json

    tabla = json["Temporada"]
    nombre = json["Nombre"]

    JsonImg = {

        'tabla': tabla
    }

    print(JsonImg)
    # Hacer un dict/json que tenga los datos de la tabla a crear

    saveHtmlTablaTemporada(nombre, render_template(
        'tabla_temporada.html', **JsonImg))
    return Response()


def saveHtmlTablaTemporada(filtro, html):
    pathlib.Path(
        f'Reports/Tables/Temporada').mkdir(parents=True, exist_ok=True)
    with open(f'Reports/Tables/Temporada/{filtro}.html', 'w', encoding="utf-8") as f:
        f.write(html)
        f.close


@app.route('/postTemporadaDeUnEquipo', methods=['POST'])
def TemporadaDeUnEquipo():
    json = request.json

    equipo = json["Equipo"]
    tabla = json["Resultado"]
    nombre = json["Nombre"]

    JsonImg = {
        'equipo': equipo,
        'tabla': tabla
    }

    # Hacer un dict/json que tenga los datos de la tabla a crear

    saveHtmlTemporadaDeUnEquipo(nombre, render_template(
        'tabla_temporada_equipo.html', **JsonImg))
    return Response()


def saveHtmlTemporadaDeUnEquipo(filtro, html):
    pathlib.Path(
        f'Reports/Tables/Temporada_Equipo').mkdir(parents=True, exist_ok=True)
    with open(f'Reports/Tables/Temporada_Equipo/{filtro}.html', 'w', encoding="utf-8") as f:
        f.write(html)
        f.close


@app.route('/postErrores', methods=['POST'])
def Errores():

    json = request.json
    lista = json['errores']

    JsonImg = {
        'lista': lista
    }

    # Hacer un dict/json que tenga los datos de la tabla a crear
    saveHtmlErrors('errores', render_template('Errores.html', **JsonImg))

    return Response()


def saveHtmlErrors(filtro, html):
    pathlib.Path(f'Reports/Errors').mkdir(parents=True, exist_ok=True)
    with open(f'Reports/Errors/{filtro}.html', 'w', encoding="utf-8") as f:
        f.write(html)
        f.close


@app.route('/postErroresSic', methods=['POST'])
def ErroresSic():

    json = request.json
    lista = json['erroresSintacticos']

    JsonImg = {
        'lista': lista
    }

    # Hacer un dict/json que tenga los datos de la tabla a crear
    saveHtmlErrors('erroresSic', render_template('ErroresSic.html', **JsonImg))

    return Response()


def saveHtmlErrors(filtro, html):
    pathlib.Path(f'Reports/Errors').mkdir(parents=True, exist_ok=True)
    with open(f'Reports/Errors/{filtro}.html', 'w', encoding="utf-8") as f:
        f.write(html)
        f.close


@app.route('/postTokens', methods=['POST'])
def link():

    json = request.json
    lista = json['tokens']

    JsonImg = {
        'lista': lista
    }

    #Hacer un dict/json que tenga los datos de la tabla a crear
    saveHtmlTokens('tokens', render_template('Tokens.html', **JsonImg))

    return Response()


def saveHtmlTokens(filtro, html):
    pathlib.Path(f'Reports/Tokens').mkdir(parents=True, exist_ok=True)
    with open(f'Reports/Tokens/{filtro}.html', 'w') as f:
        f.write(html)
        f.close
