import sqlite3
import random
from datetime import datetime, timedelta

def generar_base_datos():
    conn = sqlite3.connect('ventas_final.db')
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS pedidos')
    c.execute('DROP TABLE IF EXISTS clientes')

    c.execute('''CREATE TABLE clientes (
                    cliente_id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    sector TEXT)''')

    c.execute('''CREATE TABLE pedidos (
                    pedido_id INTEGER PRIMARY KEY,
                    cliente_id INTEGER,
                    fecha DATE,
                    total DECIMAL(10,2),
                    producto TEXT,
                    categoria TEXT,
                    FOREIGN KEY(cliente_id) REFERENCES clientes(cliente_id))''')

    sectores = ['Tecnología', 'Salud', 'Retail', 'Finanzas', 'Construcción']
    productos = {
        'Hardware': [('Laptop Pro', 1200), ('Servidor Rack', 3000), ('Monitor 4K', 400)],
        'Software': [('Licencia CRM', 500), ('Suscripción Cloud', 150), ('Antivirus Corp', 80)],
        'Servicios': [('Consultoría Hora', 100), ('Soporte Mensual', 800), ('Auditoría', 2500)]
    }

    for i in range(1, 51):
        sector = random.choice(sectores)
        nombre = f"Empresa {sector} {i}"
        c.execute("INSERT INTO clientes (nombre, sector) VALUES (?, ?)", (nombre, sector))

    fecha_inicio = datetime.now() - timedelta(days=730)
    
    for dias in range(730):
        fecha_actual = fecha_inicio + timedelta(days=dias)
        num_ventas = random.randint(0, 5)
        
        for _ in range(num_ventas):
            cliente_id = random.randint(1, 50)
            categoria = random.choice(list(productos.keys()))
            prod_nombre, precio_base = random.choice(productos[categoria])
            
            factor_crecimiento = 1 + (dias / 1000) 
            total = round(precio_base * random.uniform(0.8, 1.2) * factor_crecimiento, 2)
            
            c.execute("INSERT INTO pedidos (cliente_id, fecha, total, producto, categoria) VALUES (?, ?, ?, ?, ?)", 
                      (cliente_id, fecha_actual.strftime('%Y-%m-%d'), total, prod_nombre, categoria))

    conn.commit()
    conn.close()
    print("Base de datos generada exitosamente.")

if __name__ == '__main__':
    generar_base_datos()