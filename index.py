from flask import Flask, Response, app, flash, jsonify, render_template, request, url_for, redirect, session
from flask_mysqldb import MySQL
import hashlib
import pandas as pd
import mysql.connector

conexion1=mysql.connector.connect(host="localhost", 
                                  user="root", 
                                  passwd="ing.dylan1", 
                                  database="playadormida")

"""cursor1=conexion1.cursor()
code='playadormida1379'
salt=code.encode('utf-8')
nombre='playadormidarecepcion'
password=input('ingrese contraseña: ')
clave=password.encode('utf-8')
contraseña=hashlib.sha512(clave+salt).hexdigest()
sql="insert into recepcionistas (nombres,contraseña) VALUES (%s,%s)"
datos=(nombre,contraseña)
cursor1.execute(sql, datos)
conexion1.commit()
conexion1.close()"""


app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='ing.dylan1'
app.config['MYSQL_DB']='playadormida'

mysql=MySQL(app)




app.secret_key='mysecretkey'

code='playadormida1379'
salt=code.encode('utf-8')




#ruta de ingreso login 
@app.route('/', methods=['GET','POST'])
def login():
    if request.method=='POST':
        cedula=request.form['logincedula']
        contra=request.form['loginpassword']
        clave=contra.encode('utf-8')
        contraseña=hashlib.sha512(clave+salt).hexdigest()
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM propietarios WHERE cedula=%s',(cedula,))
        data=cursor.fetchall()
        if data:
            cursor.execute('SELECT * FROM propietarios WHERE contraseña=%s and cedula=%s',(contraseña,cedula,))
            data2=cursor.fetchall()
            if data2 and data:
                session['user']=cedula
                return redirect(url_for('dashboard'))
            else:
                flash('Contraseña incorrecta')
                return render_template('login.html')
        
        cursor.execute('SELECT * FROM administracion WHERE cedula=%s',(cedula,))
        data=cursor.fetchall()
        if data:
            cursor.execute('SELECT * FROM administracion WHERE contraseña=%s and cedula=%s',(contraseña,cedula,))
            data2=cursor.fetchall()
            if data2 and data:
                session['admin']=cedula
                return redirect(url_for('administracion'))
            else:
                flash('Contraseña incorrecta')
                return render_template('login.html')
        
        cursor.execute('SELECT * FROM asistente WHERE nombres=%s',(cedula,))
        data=cursor.fetchall()
        if data:
            cursor.execute('SELECT * FROM asistente WHERE contraseña=%s and nombres=%s',(contraseña,cedula,))
            data2=cursor.fetchall()
            if data2 and data:
                session['asistente']=cedula
                return redirect(url_for('asistente'))
            else:
                flash('Contraseña incorrecta')
                return render_template('login.html')
        
        cursor.execute('SELECT * FROM recepcionistas WHERE nombres=%s',(cedula,))
        data=cursor.fetchall()
        if data:
            cursor.execute('SELECT * FROM recepcionistas WHERE contraseña=%s and nombres=%s',(contraseña,cedula,))
            data2=cursor.fetchall()
            if data2 and data:
                session['recepcion']=cedula
                return redirect(url_for('recepcion'))
            else:
                flash('Contraseña incorrecta')
                return render_template('login.html')
        else: 
            flash('Usuario no encontrado. Si usted es propietario, dirijase al enlace: "¿No tienes una cuenta?" Sino, comuníquese con administración.')
            return render_template('login.html')
    else:
        return render_template('login.html')

#ruta logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('dashboard'))

#ruta dashboard propietario
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('propietarios/dashboard.html')
    else:
        flash('No ha iniciado sesión')
        return redirect(url_for('login'))

#ruta registro
@app.route('/registro')
def registro():
    return render_template('registro.html')




#ruta de registro a tabla propietarios
@app.route('/registrarpropietario', methods=['POST'])
def registrarpropietario():
    if request.method=='POST':
        nombre=request.form['inputnombre']
        apellido=request.form['inputapellido']
        cedula=request.form['inputcedula']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM propietarios WHERE cedula=%s',(cedula,))
        data=cursor.fetchall()
        if data:
            flash('Usuario ya existe')
            return render_template('registro.html')
        else:
            email=request.form['inputemail']
            telefono=request.form['inputtelefono']
            direccion=request.form['inputdireccion']
            torre=request.form['inputtorre']
            apartamento=request.form['inputapartamento']
            password=request.form['inputpassword']
            clave=password.encode('utf-8')
            contraseña=hashlib.sha512(clave+salt).hexdigest()
            cursor.execute('INSERT INTO propietarios (nombre, apellido, cedula, email, telefono, direccion, torre, apartamento, contraseña) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(nombre,apellido,cedula,email,telefono,direccion,torre,apartamento,contraseña))
            mysql.connection.commit()
            flash('usuario registrado correctamente')
            return redirect(url_for('login'))
        

#ruta recuperacion contraseña
@app.route('/contraseña')
def contraseña():
    return render_template('contraseña.html')

#ruta cambio de contraseña
@app.route('/cambiarcontraseña', methods=['POST'])
def cambiarcontraseña():
    if request.method=='POST':
        cedula=request.form['cedulacontra']
        password=request.form['nuevacontra']
        clave=password.encode('utf-8')
        contraseña=hashlib.sha512(clave+salt).hexdigest()
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM propietarios WHERE cedula=%s',(cedula,))
        data=cursor.fetchall()
        if data:
            cursor.execute("""UPDATE propietarios SET contraseña=%s WHERE cedula=%s""",(contraseña,cedula))
            mysql.connection.commit()
            flash('Contraseña actualizada exitosamente')
            return redirect(url_for('login'))
        else:
            flash('Usuario no existe')
            return redirect(url_for('contraseña'))

            
#ruta dashboard admin
@app.route('/administracion')
def administracion():
    if 'admin' in session:
        return render_template('administracion/dashboardadmon.html')
    else: 
        flash('No ha iniciado sesión')
        return redirect(url_for('login'))

#listar todos los visitantes en el modulo de administración
@app.route('/listadovisitantes')
def listadovisitantes():
    if 'admin' in session:
        return render_template('administracion/listadovisitantes_admon.html')
    else: 
        flash('No ha iniciado sesión')
        return redirect(url_for('login'))


#ruta que retorna los visitantes por medio de diccionario, para el search
@app.route('/datos', methods=['GET'])
def datos():
    
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM visitantes')
    data=cursor.fetchall()
    cursor.close()
    lista=[]
    for i in data:
        dic={}
        dic['nombres'] = i[0]
        dic['cedula'] = i[1]
        dic['email'] = i[2]
        dic['torre'] = i[3]
        dic['apartamento'] = i[4]
        dic['parentesco'] = i[5]
        dic['fecha_ingreso'] = i[6]
        dic['fecha_salida'] = i[7]
        if i[8]=='#868686':
            dic['color_manilla'] = 'gris'
        elif i[8]=='#FF0000':
            dic['color_manilla'] = 'roja'
        elif i[8]=='#03C6F3':
            dic['color_manilla'] = 'azul'
        elif i[8]=='#E9F303':
            dic['color_manilla'] = 'amarilla'
        elif i[8]=='#2CF303':
            dic['color_manilla'] = 'verde'
        elif i[8]=='#FFFFFF':
            dic['color_manilla'] = 'ninguna'
        else:
            dic['color_manilla'] = i[8]
        dic['pago'] = i[9]
        lista.append(dic)
    return jsonify({"datos":lista})    

    
#listar visitantes para editar
@app.route('/editar_admin')
def editar_admin():
    if 'admin' in session:
        cursor=mysql.connection.cursor()
        numero=cursor.execute('SELECT * FROM visitantes ORDER BY fecha_ingreso ASC')
        data=cursor.fetchall()
        return render_template('administracion/editar_admin.html',visitantes=data,conteo=numero)
    else:
        flash('No ha iniciado sesión')
        return redirect(url_for('login'))

#listar datos del admin para color de manilla
@app.route('/colordemanilla/<string:cedula>')
def colormanilla(cedula):
    if 'admin' in session:
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM visitantes WHERE cedula={0}'.format(cedula))
        data=cursor.fetchall()
        return render_template('administracion/colordemanilla.html', visitantes=data[0])
    else:
        flash('No ha iniciado sesión')
        return redirect(url_for('login'))

#ruta del admin para actualizar el color de manilla
@app.route('/actualizarmanilla/<cedula2>', methods=['POST'])
def actualizarmanilla(cedula2):
    if request.method=='POST':
        color=request.form['visitantemanilla']
        cursor=mysql.connection.cursor()
        if color=='gris'or color=='GRIS' or color=='Gris' or color=='#868686':
            colormanilla='#868686'
            cursor.execute("""UPDATE visitantes SET color_manilla=%s WHERE cedula=%s""",(colormanilla,cedula2))
            mysql.connection.commit()
            flash('Color de manilla registrado exitosamente')
            return redirect(url_for('editar_admin'))
        elif color=='roja'or color=='ROJA' or color=='Roja' or color=='#FF0000':
            colormanilla='#FF0000'
            cursor.execute("""UPDATE visitantes SET color_manilla=%s WHERE cedula=%s""",(colormanilla,cedula2))
            mysql.connection.commit()
            flash('Color de manilla registrado exitosamente')
            return redirect(url_for('editar_admin'))
        elif color=='azul'or color=='AZUL' or color=='Azul' or color=='#03C6F3':
            colormanilla='#03C6F3'
            cursor.execute("""UPDATE visitantes SET color_manilla=%s WHERE cedula=%s""",(colormanilla,cedula2))
            mysql.connection.commit()
            flash('Color de manilla registrado exitosamente')
            return redirect(url_for('editar_admin'))
        elif color=='amarilla'or color=='AMARILLA' or color=='Amarilla' or color=='#E9F303':
            colormanilla='#E9F303'
            cursor.execute("""UPDATE visitantes SET color_manilla=%s WHERE cedula=%s""",(colormanilla,cedula2))
            mysql.connection.commit()
            flash('Color de manilla registrado exitosamente')
            return redirect(url_for('editar_admin'))
        elif color=='verde'or color=='VERDE' or color=='Verde' or color=='#2CF303':
            colormanilla='#2CF303'
            cursor.execute("""UPDATE visitantes SET color_manilla=%s WHERE cedula=%s""",(colormanilla,cedula2))
            mysql.connection.commit()
            flash('Color de manilla registrado exitosamente')
            return redirect(url_for('editar_admin'))
        elif color=='ninguna' or color=='#FFFFFF':
            colormanilla='#FFFFFF'
            cursor.execute("""UPDATE visitantes SET color_manilla=%s WHERE cedula=%s""",(colormanilla,cedula2))
            mysql.connection.commit()
            flash('Color de manilla registrado exitosamente')
            return redirect(url_for('editar_admin'))
        else:
            cursor.execute("""UPDATE visitantes SET color_manilla=%s WHERE cedula=%s""",(color,cedula2))
            mysql.connection.commit()
            flash('Color de manilla registrado con color diferente a los especificados normalmente: Gris, Roja, Azul, Amarilla, Verde.')
            return redirect(url_for('editar_admin'))
            


    

#listar datos del admin para registrar pago
@app.route('/pago/<cedula>')
def pagos(cedula):
    if 'admin' in session:
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM visitantes WHERE cedula={0}'.format(cedula))
        data=cursor.fetchall()
        return render_template('administracion/pago.html',visitantes=data[0])
    else:
        flash('No ha iniciado sesión')
        return redirect(url_for('login'))



#ruta del admin para actualizar el valor a pagar
@app.route('/actualizarpago/<cedula2>', methods=['POST'])
def actualizarpago(cedula2):
    if request.method=='POST':
        valor=request.form['visitantepagoact']
        cursor=mysql.connection.cursor()
        cursor.execute("""UPDATE visitantes SET pago=%s WHERE cedula=%s""",(valor,cedula2))
        mysql.connection.commit()
        flash('Pago registrado exitosamente')
        return redirect(url_for('editar_admin'))

#ruta editar visitante admin
@app.route('/editarvisitante/<cedula>')
def editarvisitante(cedula):
    if 'admin' in session:
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM visitantes WHERE cedula={0}'.format(cedula))
        data=cursor.fetchall()
        return render_template('administracion/editarvisitante.html',visitantes=data[0])
    else:
        flash('No ha iniciado sesión')
        return redirect(url_for('login'))

#ruta actualizar visitante admin
@app.route('/actualizarvisitante/<cedula2>', methods=['POST'])
def actualizarvisitante(cedula2):
    if request.method=='POST':
        nombre=request.form['visitantenombreact']
        cedula=request.form['visitantecedulaact']
        email=request.form['visitanteemailact']
        torre=request.form['visitantetorreact']
        apartamento=request.form['visitanteapartamentoact']
        parentesco=request.form['visitanteparentescoact']
        fechaingreso=request.form['visitanteingresoact']
        fechasalida=request.form['visitantesalidaact']
        cursor=mysql.connection.cursor()
        cursor.execute("""UPDATE visitantes SET nombres=%s,cedula=%s,email=%s,torre=%s,apartamento=%s, parentesco=%s,fecha_ingreso=%s,fecha_salida=%s WHERE cedula=%s""",(nombre,cedula,email,torre,apartamento,parentesco,fechaingreso,fechasalida,cedula2))
        mysql.connection.commit()
        flash('Visitante actualizado exitosamente')
        return redirect(url_for('editar_admin'))


#ruta eliminar visitante
@app.route('/eliminarvisitante/<string:cedula>')
def eliminarvisitante(cedula):
    if 'admin' in session:
        cursor=mysql.connection.cursor()
        cursor.execute('DELETE FROM visitantes WHERE cedula={0}'.format(cedula))
        mysql.connection.commit()
        flash('Visitante eliminado exitosamente')
        return redirect(url_for('editar_admin'))
    elif 'user' in session:
        cursor=mysql.connection.cursor()
        cursor.execute('DELETE FROM visitantes WHERE cedula={0}'.format(cedula))
        mysql.connection.commit()
        flash('Visitante eliminado exitosamente')
        return redirect(url_for('registrovisitantes'))
    else:
        flash('No ha iniciado sesión')
        return redirect(url_for('login'))


#ruta dashboard asistente
@app.route('/asistente')
def asistente():
    if 'asistente' in session:
        return render_template('asistente/asistentedashboard.html')
    else: 
        flash('No ha iniciado sesión')
        return redirect(url_for('login'))

#listado de visitantes para el asistente
@app.route('/listadovisitantes_asis')
def listado_asis():
    if 'asistente' in session:
        return render_template('asistente/listadovisitantes_asis.html')
    else: 
        flash('No ha iniciado sesión')
        return redirect(url_for('login'))

#ruta registro para visitantes y listar datos almacenados por el propietario
@app.route('/registrovisitantes')
def registrovisitantes():
    if 'user' in session:
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM visitantes')
        data=cursor.fetchall()
        numero=cursor.execute('SELECT * FROM visitantes')
        cursor.close()
        return render_template('propietarios/registrovisitantes.html', conteo=numero, visitantes=data)
    else:
        flash('No ha inciado sesión')
        return redirect(url_for('login')) 

#ruta para agregar visitantes
@app.route('/agregarvisitantes', methods=['POST'])
def agregarvisitantes():
    if request.method=='POST':
        cursor=mysql.connection.cursor()
        cedula=request.form['visitantecedula']
        cursor.execute('SELECT * FROM visitantes WHERE cedula=%s',(cedula,))
        data=cursor.fetchall()
        if data:
            flash('Visitante ya tiene un ingreso existente. para volver a registrarlo tiene que terminar la fecha del primer registro, editarlo o eliminarlo. En caso de dudas comuniquese con Administración')
            return redirect(url_for('registrovisitantes'))
        else:
            nombre=request.form['visitantenombre']
            email=request.form['visitanteemail']
            torre=request.form['visitantetorre']
            apartamento=request.form['visitanteapartamento']
            parentesco=request.form['visitanteparentesco']
            fechaingreso=request.form['visitanteingreso']
            fechasalida=request.form['visitantesalida']
            colormanilla='#FFFFFF'
            cursor.execute("INSERT INTO visitantes (nombres, cedula, email, torre, apartamento, parentesco, fecha_ingreso, fecha_salida,color_manilla) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
            (nombre,cedula,email,torre,apartamento,parentesco,fechaingreso,fechasalida,colormanilla))
            mysql.connection.commit()
            flash('Visitante registrado exitosamente')
            return redirect(url_for('registrovisitantes'))

#ruta para listar visitantes del propietario
@app.route('/listarvisitantes_propietario', methods=['POST'])
def listarpropietario():
    if request.method=='POST':
        cedula=request.form['listadocedula']
        if cedula==session['user']:
            cursor=mysql.connection.cursor()
            cursor.execute('SELECT * FROM propietarios WHERE cedula=%s',(cedula,))
            data=cursor.fetchall()
            for i in data:
                torre=i[6]
                apartamento=i[7]
            cursor.execute('SELECT * FROM visitantes WHERE torre=%s and apartamento=%s ORDER BY fecha_ingreso ASC ',(torre,apartamento,))
            data2=cursor.fetchall()
            print(data2)
            return render_template('propietarios/registrovisitantes.html',mivisitante=data2)
        else:
            flash('Esta no es su cédula')
            return redirect(url_for('registrovisitantes'))

#ruta editar visitante propietario
@app.route('/editarvisitante_propietario/<cedula>')
def editarvisitante_propietario(cedula):
    if 'user' in session:
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM visitantes WHERE cedula={0}'.format(cedula))
        data=cursor.fetchall()
        return render_template('propietarios/editarvisitante_propietario.html',visitantes=data[0])
    else:
        flash('No ha iniciado sesión')
        return redirect(url_for('login'))

#ruta actualizar visitante propietario
@app.route('/actualizarvisitante_propietario/<cedula2>', methods=['POST'])
def actualizarvisitante_propietario(cedula2):
    if request.method=='POST':
        nombre=request.form['visitantenombreact']
        cedula=request.form['visitantecedulaact']
        email=request.form['visitanteemailact']
        torre=request.form['visitantetorreact']
        apartamento=request.form['visitanteapartamentoact']
        parentesco=request.form['visitanteparentescoact']
        fechaingreso=request.form['visitanteingresoact']
        fechasalida=request.form['visitantesalidaact']
        cursor=mysql.connection.cursor()
        cursor.execute("""UPDATE visitantes SET nombres=%s,cedula=%s,email=%s,torre=%s,apartamento=%s, parentesco=%s,fecha_ingreso=%s,fecha_salida=%s WHERE cedula=%s""",(nombre,cedula,email,torre,apartamento,parentesco,fechaingreso,fechasalida,cedula2))
        mysql.connection.commit()
        cedula=session['user']
        flash('Visitante actualizado exitosamente')
        return redirect(url_for('registrovisitantes'))


#ruta dashboard recepcion
@app.route('/recepcion')
def recepcion():
    if 'recepcion' in session:
        return render_template('recepcion/recepcionista.html')
    else:
        flash('No ha iniciado sesión')
        return redirect(url_for('login'))

#listado de visitantes para el recepcionista
@app.route('/listadovisitantes_recep')
def listado_recep():
    if 'recepcion' in session:
        return render_template('recepcion/listadovisitantes_recep.html')
    else: 
        flash('No ha iniciado sesión')
        return redirect(url_for('login'))

#descargar listado de visitantes
@app.route('/descargar_reporte')
def descargar_reporte():
    if 'admin' or 'asistente' in session:
        query="SELECT * FROM visitantes"
        df=pd.read_sql_query(query,con=conexion1)
        df.set_index('cedula',inplace=True)

        return Response(df.to_csv(),mimetype="text/csv",headers={"Content-Disposition":"attachment;filename=reporte_personas.csv"})
    else:
       flash('No ha iniciado sesión')
       return redirect(url_for('login')) 


# Iniciar el servidor
if __name__=='__main__':
    app.run(debug=True)