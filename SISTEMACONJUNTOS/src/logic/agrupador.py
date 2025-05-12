def agrupar_conjuntos(conjuntos):
    num_conjuntos = len(conjuntos)
    grupos = []

    # Agrupación según la cantidad de conjuntos
    while num_conjuntos > 0:
        if num_conjuntos >= 8:
            grupos.append(4)  # Grupos de 4
            num_conjuntos -= 4
        elif num_conjuntos == 7:
            grupos.append(4)
            grupos.append(3)
            break
        elif num_conjuntos == 6:
            grupos.append(3)
            grupos.append(3)
            break
        elif num_conjuntos == 5:
            grupos.append(3)
            grupos.append(2)
            break
        else:
            grupos.append(num_conjuntos)
            break
    return grupos
