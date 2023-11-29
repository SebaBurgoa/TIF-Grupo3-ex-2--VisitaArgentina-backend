from flask import Flask, render_template, request, redirect, url_for, jsonify
from controller.controller import *


#Para subir archivo tipo foto al servidor
import os
from werkzeug.utils import secure_filename 


#Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
app = Flask(__name__)
application = app

msg  =''
tipo =''


 
@app.route('/', methods=['GET','POST'])
def inicio():
    return render_template('public/layout.html', miData = listaExcursiones())


#RUTAS
@app.route('/registrar-Excursion', methods=['GET','POST'])
def addExcursion():
    return render_template('public/acciones/add.html')


 

@app.route('/Excursion', methods=['POST'])
def formAddExcursion():
    if request.method == 'POST':
        Nombre              = request.form['Nombre']
        Descripcion         = request.form['Descripcion']
        ano                = request.form['ano']
        if(request.files['foto'] !=''):
            file     = request.files['foto'] #recibiendo el archivo
            nuevoNombreFile = recibeFoto(file) #Llamado la funcion que procesa la imagen
            resultData = registrar(Nombre, Descripcion, ano, nuevoNombreFile)
            if(resultData ==1):
                return render_template('public/layout.html', miData = listaExcursiones(), msg='El Registro fue un éxito', tipo=1)
            else:
                return render_template('public/layout.html', msg = 'Metodo HTTP incorrecto', tipo=1)   
        else:
            return render_template('public/layout.html', msg = 'Debe cargar una foto', tipo=1)
            


@app.route('/form-update-excursion/<string:id>', methods=['GET','POST'])
def formViewUpdate(id):
    if request.method == 'GET':
        resultData = updateExcursion(id)
        if resultData:
            return render_template('public/acciones/update.html',  dataInfo = resultData)
        else:
            return render_template('public/layout.html', miData = listaExcursiones(), msg='No existe la Excursion', tipo= 1)
    else:
        return render_template('public/layout.html', miData = listaExcursiones(), msg = 'Metodo HTTP incorrecto', tipo=1)          
 
   
  
@app.route('/ver-detalles-dela-excursion/<int:idExcursion>', methods=['GET', 'POST'])
def viewDetalleExcursion(idExcursion):
    msg =''
    if request.method == 'GET':
        resultData = detallesdelaExcursion(idExcursion)  
        
        if resultData:
            return render_template('public/acciones/view.html', infoExcursion = resultData, msg='Detalles de la Excursion', tipo=1)
        else:
            return render_template('public/acciones/layout.html', msg='No existe la excursion', tipo=1)
    return redirect(url_for('inicio'))
    

@app.route('/actualizar-excursion/<string:idExcursion>', methods=['POST'])
def  formActualizarExcursion(idExcursion):
    if request.method == 'POST':
        Nombre          = request.form['Nombre']
        Descripcion     = request.form['Descripcion']
        Año             = request.form['ano'] 
        
        #Script para recibir el archivo (foto)
        if(request.files['foto']):
            file     = request.files['foto']
            fotoForm = recibeFoto(file)
            resultData = recibeActualizarExcursion(Nombre, Descripcion,Año,fotoForm, idExcursion)
        else:
            fotoExcursion  ='sin_foto.jpg'
            resultData = recibeActualizarExcursion(Nombre, Descripcion,Año,fotoExcursion, idExcursion)

        if(resultData ==1):
            return render_template('public/layout.html', miData = listaExcursiones(), msg='Datos de la Excursion actualizados', tipo=1)
        else:
            msg ='No se actualizo el registro'
            return render_template('public/layout.html', miData = listaExcursiones(), msg='No se pudo actualizar', tipo=1)



@app.route('/borrar-Excursion', methods=['GET', 'POST'])
def formViewBorrarExcur():
    if request.method == 'POST':
        idExcursion        = request.form['id']
        nombreFoto      = request.form['nombreFoto']
        resultData      = eliminarExcursion(idExcursion, nombreFoto)

        if resultData ==1:
            #Nota: retorno solo un json y no una vista para evitar refescar la vista
            return jsonify([1])
            #return jsonify(["respuesta", 1])
        else: 
            return jsonify([0])




def eliminarExcursion(id='', nombreFoto=''):
        
    conexion_MySQLdb = connectionBD() #Hago instancia a mi conexion desde la funcion
    cur              = conexion_MySQLdb.cursor(dictionary=True)
    
    cur.execute('DELETE FROM excursiones WHERE id=%s', (id,))
    conexion_MySQLdb.commit()
    resultado_eliminar = cur.rowcount #retorna 1 o 0
    #print(resultado_eliminar)
    
    basepath = os.path.dirname (__file__) #C:\xampp\htdocs\localhost\Crud-con-FLASK-PYTHON-y-MySQL\app
    url_File = os.path.join (basepath, 'static/assets/fotos', nombreFoto)
    os.remove(url_File) #Borrar foto desde la carpeta
    #os.unlink(url_File) #Otra forma de borrar archivos en una carpeta
    

    return resultado_eliminar



def recibeFoto(file):
    print(file)
    basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
    filename = secure_filename(file.filename) #Nombre original del archivo

    #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
    extension           = os.path.splitext(filename)[1]
    nuevoNombreFile     = stringAleatorio() + extension
    #print(nuevoNombreFile)
        
    upload_path = os.path.join (basepath, 'static/assets/fotos', nuevoNombreFile) 
    file.save(upload_path)

    return nuevoNombreFile

       
  
  
#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('inicio'))
    
    
    
    
if __name__ == "__main__":
    app.run(debug=True, port=8000)