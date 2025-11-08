import pyodbc, os
from datetime import datetime


def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    while True:
        limpiar()
        OP = input("""
    1) Crear usuario
    2) iniciar sesion
    3) Salir
> """)

        if OP == '1':
            Creacion_de_usuario()
        elif OP == '2':
            Iniciar_sesion()
        elif OP == '3':
            print("Saliendo del programa...")
            break
        else:
            input("Opcion no valida. Presiona ENTER para continuar...")

def Creacion_de_usuario():
    limpiar()
    while True:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios")

        Nombre = input("Introduzca su nombre (ENTER para volver): ")
        if Nombre == '':
            return
        
        Apellido = input("Introduzca su apellido: ")
        Correo = input("Introduzca su correo: ")
        Contrasena = input("Introduzca una contraseña: ")

        # Insertar el nuevo usuario
        sql = """
        INSERT INTO usuarios (nombre, apellido, correo, contrasena)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql, (Nombre, Apellido, Correo, Contrasena))
        conn.commit()

        cursor.close()
        conn.close()
        print("\n✅ Usuario creado con éxito\n")

        op = input("¿Desea crear otro usuario? (s/n): ")
        if op.lower() != 's':
            break
        limpiar()



def Iniciar_sesion():
    limpiar()
    while True:
        c = 0  # ✅ inicializada al principio
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Usuarios")

        NombreU = input("Introduzca su nombre de usuario: ")
        Contraseña = input("Introduzca su contraseña: ")
        for x in cursor:
            if NombreU == x.NombreU and Contraseña == x.Contraseña:
                input(f"Bienvenido {NombreU}")
                c = 1
                limpiar()
                break
        if c == 1:
            break
        elif c == 0:
            input("Nombre o contraseña incorrectos, intente otra vez")
            limpiar()

            break
        if c == 1:
            break
        elif c == 0:
            input("Nombre o contraseña incorrectos, intente otra vez")
            limpiar()


    while True:
        limpiar()
        op = input("""
    1) Ver perfil
    2) Ver publicaciones
    3) Buscar usuario
    4) Cerrar sesion
    """)
        if op == '1':
            Perfil(NombreU)
        elif op == '2':
            Publicaciones(NombreU)
        elif op == '3':
            Busqueda(NombreU)
        elif op == '4':
            break
        else:
            input("Opcion no valida")
            limpiar()


def Busqueda(NombreU):
    while True:
        limpiar()
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        NombreB = input("¿A quién buscas? (ENTER para volver) ")
        if NombreB == '':
            return
        else:
            cursor.execute(f"""
                SELECT *
                FROM Usuarios u
                INNER JOIN Publicaciones p ON p.ID_usuario = u.ID_usuario
                WHERE NombreU = ?
                ORDER BY Fecha ASC;
            """, (NombreB,))
            
            encontrado = False
            for x in cursor:
                if NombreB == x.NombreU:
                    print(f"\nUsuario encontrado: {x.NombreU}\n")
                    encontrado = True
                    break

            if not encontrado:
                print("No se encontró al usuario.")
                input("Presiona ENTER para continuar...")
                continue

            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Contenido, Fecha
                FROM Usuarios u
                INNER JOIN Publicaciones p ON p.ID_usuario = u.ID_usuario
                WHERE NombreU = ?;
            """, (NombreB,))
            
            print("Publicaciones:\n")
            for x in cursor:
                print(f"- {x.Contenido} ({x.Fecha})")

            op = input(f"""\n¿Quieres agregar a {NombreB} como amigo?
1) Sí
2) No
> """)

        if op == '1':
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()

            cursor.execute("SELECT ID_usuario FROM Usuarios WHERE NombreU = ?", (NombreU,))
            usuario = cursor.fetchone()

            cursor.execute("SELECT ID_usuario FROM Usuarios WHERE NombreU = ?", (NombreB,))
            amigo = cursor.fetchone()

            if usuario and amigo:
                sql = """
                    INSERT INTO Amigos (ID_usuario, ID_amigo)
                    VALUES (?, ?)
                """
                cursor.execute(sql, (usuario.ID_usuario, amigo.ID_usuario))
                conn.commit()
                print(f"\n{NombreB} fue agregado como amigo de {NombreU}.")
            else:
                print("Error: No se pudo encontrar alguno de los usuarios.")

            cursor.close()
            conn.close()
            input("Presiona ENTER para continuar...")
        elif op == '2':
            break
        else:
            input("Opcion no valida")
            limpiar()
            

def Publicaciones(NombreU):
    limpiar()
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM Usuarios u
        INNER JOIN Publicaciones p ON p.ID_usuario = u.ID_usuario
        ORDER BY Fecha DESC ;
    """)

    for x in cursor:
        print(f"""
{x.NombreU}
{x.Contenido} - {x.Fecha}
""")
        op = input("(ENTER para cambiar de publicacion, 1 para crear una publicacion y 2 para volver) ")

        if op == '1':
            limpiar()
            while True:
                conn = pyodbc.connect(connection_string)
                cursor = conn.cursor()

                cursor.execute("SELECT ID_usuario FROM Usuarios WHERE NombreU = ?", (NombreU,))
                usuario = cursor.fetchone()

                Contenido = input("(ENTER para volver) ¿Qué hiciste hoy?: ")
                if Contenido == '':
                    return
                else:
                    sql = """
                        INSERT INTO Publicaciones (Contenido, Fecha, ID_usuario)
                        VALUES (?, ?, ?)
                    """
                    Fecha = datetime.now()
                    cursor.execute(sql, (Contenido, Fecha, usuario.ID_usuario ))
                    conn.commit()
                    cursor.close()
                    conn.close()

                    op = input("""Publicación creada con éxito
1) Ver publicaciones
2) Hacer otra publicación
""")

                if op == '1':
                    Perfil(NombreU)
                    continue
                elif op == '2':
                    continue

        elif op == '2':
            break



def Perfil(NombreU):
    while True:
        op = input(f"""Perfil de {NombreU}:
    1)Ver lista de amigos
    2)Ver publicaciones
    3)Volver
    """)
        if op == '1':
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()

            cursor.execute("SELECT ID_usuario FROM Usuarios WHERE NombreU = ?", (NombreU,))
            usuario = cursor.fetchone()

            if not usuario:
                print("Usuario no encontrado.")
                input("Presiona ENTER para continuar...")
                return

            ID_usuario = usuario.ID_usuario

            cursor.execute("""
                SELECT u.NombreU
                
                FROM Amigos a
                INNER JOIN Usuarios u ON a.ID_amigo = u.ID_usuario
                WHERE a.ID_usuario = ?
            """, (ID_usuario,))

            amigos = cursor.fetchall()

            print(f"\nLista de amigos de {NombreU}:\n")
            if amigos:
                for amigo in amigos:
                    print(f"- {amigo.NombreU}")
            else:
                print("No tienes amigos agregados aún")

            cursor.close()
            conn.close()
            input("\nPresiona ENTER para volver...")
        elif op == '2':
            limpiar()
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()

            cursor.execute(f"""
                SELECT *
                FROM Usuarios u
                INNER JOIN Publicaciones p ON p.ID_usuario = u.ID_usuario
                where NombreU = '{NombreU}'
                ORDER BY Fecha ASC;
            """)
            for x in cursor:
                print(f"""{x.Contenido} - {x.Fecha}""")
            OP = input("""
1)Crear nueva publicacion
2)Volver
""")
            if OP == '1':
                limpiar()
                while True:
                    conn = pyodbc.connect(connection_string)
                    cursor = conn.cursor()

                    cursor.execute("SELECT ID_usuario FROM Usuarios WHERE NombreU = ?", (NombreU,))
                    usuario = cursor.fetchone()

                    Contenido = input("(ENTER para volver) ¿Qué hiciste hoy?: ")
                    if Contenido == '':
                        return
                    else:
                        sql = """
                            INSERT INTO Publicaciones (Contenido, Fecha, ID_usuario)
                            VALUES (?, ?, ?)
                        """
                        Fecha = datetime.now()
                        cursor.execute(sql, (Contenido, Fecha, usuario.ID_usuario ))
                        conn.commit()
                        cursor.close()
                        conn.close()

                        op = input("""Publicación creada con éxito
1) Ver publicaciones
2) Hacer otra publicación
    """)

                    if op == '1':
                        break
                    elif op == '2':
                        continue
                    else:
                        input("opcion no valida")
                        limpiar()

        elif op == '3':
            break
        else:
            input("Opcion no valida")

    
                
connection_string = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=DESKTOP-8EM4IC1\SQLEXPRESS;"
    r"DATABASE=red_social;"
    r"Trusted_Connection=yes;"
)



menu()
