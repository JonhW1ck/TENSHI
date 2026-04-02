# self_coder: elemento_chemistry

# Diccionario interno con los primeros 36 elementos de la tabla periódica
elementos = {
    'H': {'nombre': 'Hidrógeno', 'numero_atomico': 1, 'peso_atomico': 1.00794},
    'He': {'nombre': 'Helio', 'numero_atomico': 2, 'peso_atomico': 4.002602},
    'Li': {'nombre': 'Litio', 'numero_atomico': 3, 'peso_atomico': 6.941},
    'Be': {'nombre': 'Berilio', 'numero_atomico': 4, 'peso_atomico': 9.012182},
    'B': {'nombre': 'Boro', 'numero_atomico': 5, 'peso_atomico': 10.811},
    'C': {'nombre': 'Carbono', 'numero_atomico': 6, 'peso_atomico': 12.0107},
    'N': {'nombre': 'Nitrógeno', 'numero_atomico': 7, 'peso_atomico': 14.0067},
    'O': {'nombre': 'Oxígeno', 'numero_atomico': 8, 'peso_atomico': 15.9994},
    'F': {'nombre': 'Fluor', 'numero_atomico': 9, 'peso_atomico': 18.998403163},
    'Ne': {'nombre': 'Neón', 'numero_atomico': 10, 'peso_atomico': 20.1797},
    'Na': {'nombre': 'Sodio', 'numero_atomico': 11, 'peso_atomico': 22.98976928},
    'Mg': {'nombre': 'Magnesio', 'numero_atomico': 12, 'peso_atomico': 24.305},
    'Al': {'nombre': 'Aluminio', 'numero_atomico': 13, 'peso_atomico': 26.9815385},
    'Si': {'nombre': 'Silicio', 'numero_atomico': 14, 'peso_atomico': 28.0855},
    'P': {'nombre': 'Fósforo', 'numero_atomico': 15, 'peso_atomico': 30.973762},
    'S': {'nombre': 'Azufre', 'numero_atomico': 16, 'peso_atomico': 32.065},
    'Cl': {'nombre': 'Cloro', 'numero_atomico': 17, 'peso_atomico': 35.453},
    'Ar': {'nombre': 'Argón', 'numero_atomico': 18, 'peso_atomico': 39.9483},
    'K': {'nombre': 'Potasio', 'numero_atomico': 19, 'peso_atomico': 39.0983},
    'Ca': {'nombre': 'Calcio', 'numero_atomico': 20, 'peso_atomico': 40.078},
    'Sc': {'nombre': 'Escandio', 'numero_atomico': 21, 'peso_atomico': 44.955912},
    'Ti': {'nombre': 'Titanio', 'numero_atomico': 22, 'peso_atomico': 47.867},
    'V': {'nombre': 'Vanadio', 'numero_atomico': 23, 'peso_atomico': 50.9415},
    'Cr': {'nombre': 'Cromo', 'numero_atomico': 24, 'peso_atomico': 51.9961},
    'Mn': {'nombre': 'Manganés', 'numero_atomico': 25, 'peso_atomico': 54.938044},
    'Fe': {'nombre': 'Hierro', 'numero_atomico': 26, 'peso_atomico': 55.847},
    'Co': {'nombre': 'Cobalto', 'numero_atomico': 27, 'peso_atomico': 58.933194},
    'Ni': {'nombre': 'Níquel', 'numero_atomico': 28, 'peso_atomico': 58.6934},
    'Cu': {'nombre': 'Cobre', 'numero_atomico': 29, 'peso_atomico': 63.546},
    'Zn': {'nombre': 'Zinc', 'numero_atomico': 30, 'peso_atomico': 65.38},
    'Ga': {'nombre': 'Galio', 'numero_atomico': 31, 'peso_atomico': 69.723},
    'Ge': {'nombre': 'Germanio', 'numero_atomico': 32, 'peso_atomico': 72.630},
    'As': {'nombre': 'Arsénico', 'numero_atomico': 33, 'peso_atomico': 74.9216},
    'Se': {'nombre': 'Selenio', 'numero_atomico': 34, 'peso_atomico': 78.971},
    'Br': {'nombre': 'Bromuro', 'numero_atomico': 35, 'peso_atomico': 79.904},
    'Kr': {'nombre': 'Kriptón', 'numero_atomico': 36, 'peso_atomico': 83.798}
}

def obtener_elemento(simbolo):
    """
    Obtiene el nombre del elemento, su número atómico y su peso atómico a partir de su símbolo químico.
    
    Args:
        simbolo (str): Símbolo químico del elemento.
    
    Returns:
        dict: Información del elemento (nombre, número atómico, peso atómico).
    """
    try:
        return elementos[simbolo.upper()]
    except KeyError:
        raise ValueError(f"El símbolo '{simbolo}' no es válido.")

def obtener_elementos():
    """
    Obtiene una lista de los primeros 36 elementos de la tabla periódica.
    
    Returns:
        list: Lista de diccionarios con la información de cada elemento.
    """
    return list(elementos.values())

def obtener_elementos_por_nombre(nombre):
    """
    Obtiene una lista de elementos cuyo nombre coincide con el especificado.
    
    Args:
        nombre (str): Nombre del elemento.
    
    Returns:
        list: Lista de diccionarios con la información de cada elemento.
    """
    return [elemento for elemento in elementos.values() if elemento['nombre'].lower() == nombre.lower()]

def obtener_elementos_por_numero_atomico(numero_atomico):
    """
    Obtiene una lista de elementos cuyo número atómico coincide con el especificado.
    
    Args:
        numero_atomico (int): Número atómico del elemento.
    
    Returns:
        list: Lista de diccionarios con la información de cada elemento.
    """
    return [elemento for elemento in elementos.values() if elemento['numero_atomico'] == numero_atomico]

def obtener_elementos_por_peso_atomico(peso_atomico):
    """
    Obtiene una lista de elementos cuyo peso atómico coincide con el especificado.
    
    Args:
        peso_atomico (float): Peso atómico del elemento.
    
    Returns:
        list: Lista de diccionarios con la información de cada elemento.
    """
    return [elemento for elemento in elementos.values() if round(elemento['peso_atomico'], 5) == round(peso_atomico, 5)]