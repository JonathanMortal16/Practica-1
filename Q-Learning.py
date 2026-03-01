import random

# ==========================================================
# 1) ENTORNO (VIDA DIARIA): GYM (progreso vs fatiga)
# ==========================================================

energias = [0, 1, 2]
fatigas  = [0, 1, 2]

def nombre_estado(e, f):
    return f"E{e}_F{f}"

estados = [nombre_estado(e, f) for e in energias for f in fatigas]

acciones_posibles = {
    s: ["fuerza", "hipertrofia", "cardio", "descanso", "deload"]
    for s in estados
}


def clip(x, lo, hi):
    return max(lo, min(hi, x))


def transicion(estado, accion):
    """
    Devuelve: (nuevo_estado, recompensa, terminado)

    Interpretación:
    - Recompensa = progreso - penalización_por_fatiga - penalización_por_riesgo
    - Si entrenas pesado con fatiga alta, riesgo aumenta.
    - Descanso/deload reducen fatiga y suben energía.
    """
    # Parsear estado "E?_F?"
    e = int(estado.split("_")[0][1])
    f = int(estado.split("_")[1][1])

    progreso = 0
    penal_fatiga = 0
    penal_riesgo = 0

    # Probabilidad de "día malo" (estrés/sueño). Más fatiga => peor.
    prob_dia_malo = 0.05 + 0.10 * f
    dia_malo = (random.random() < prob_dia_malo)

    # -------------------------
    # Dinámica por acción
    # -------------------------
    if accion == "fuerza":
        # Progreso alto si tienes energía suficiente, pero sube fatiga.
        progreso = 8 + 2 * e
        f += 1
        e -= 1

        # Riesgo si ya estabas muy fatigado o si fue día malo
        if f >= 2:
            penal_riesgo += 6
        if dia_malo:
            penal_riesgo += 4

    elif accion == "hipertrofia":
        progreso = 6 + e
        f += 1
        e -= 0  # casi no baja energía (sesión menos demandante que fuerza)
        if f >= 2:
            penal_riesgo += 3
        if dia_malo:
            penal_riesgo += 2

    elif accion == "cardio":
        progreso = 2  # poco progreso fuerza, pero "beneficio" general
        f -= 1        # ayuda a recuperar (ligero)
        e += 0
        if dia_malo:
            penal_riesgo += 1

    elif accion == "descanso":
        progreso = 1  # progreso indirecto por recuperación
        f -= 2
        e += 1

    elif accion == "deload":
        progreso = 4  # mantienes técnica/estímulo ligero
        f -= 2
        e += 0

    # -------------------------
    # Ajuste y penalización
    # -------------------------
    e = clip(e, 0, 2)
    f = clip(f, 0, 2)

    # Penalización por mantener fatiga alta (representa sobreentreno)
    penal_fatiga = 2 * f

    recompensa = progreso - penal_fatiga - penal_riesgo

    # Episodio termina si llegas a un estado "equilibrado" (energía alta y fatiga baja)
    # como si tu semana ya quedó bien y te sientes recuperado
    terminado = (e == 2 and f == 0)

    nuevo_estado = nombre_estado(e, f)
    return nuevo_estado, recompensa, terminado


# ==========================================================
# 2) PARÁMETROS Q-LEARNING (igual que tu ejemplo)
# ==========================================================
Q = {s: {a: 0.0 for a in acciones_posibles[s]} for s in estados}

alpha = 0.4     # tasa de aprendizaje
gamma = 0.9     # factor de descuento
epsilon = 0.25  # exploración
episodios = 200


def elegir_accion(estado):
    acciones = acciones_posibles[estado]
    if random.random() < epsilon:
        return random.choice(acciones)
    return max(acciones, key=lambda a: Q[estado][a])


# ==========================================================
# 3) ENTRENAMIENTO
# ==========================================================
for ep in range(1, episodios + 1):
    # Arrancamos como si fuera "lunes": energía media/alta, fatiga baja/media
    estado = random.choice([nombre_estado(2, 0), nombre_estado(2, 1), nombre_estado(1, 0), nombre_estado(1, 1)])
    terminado = False
    pasos = 0

    while not terminado and pasos < 30:  # límite de pasos para evitar loops raros
        accion = elegir_accion(estado)
        nuevo_estado, recompensa, terminado = transicion(estado, accion)

        max_q_siguiente = 0 if terminado else max(Q[nuevo_estado].values())
        Q[estado][accion] = Q[estado][accion] + alpha * (
            recompensa + gamma * max_q_siguiente - Q[estado][accion]
        )

        estado = nuevo_estado
        pasos += 1

    # Mostrar cada cierto número de episodios para no spamear
    if ep % 25 == 0:
        print(f"\n--- Episodio {ep} ---")
        for s in [nombre_estado(2,0), nombre_estado(2,1), nombre_estado(1,2), nombre_estado(0,2)]:
            mejores = sorted(Q[s].items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"Estado {s} -> top acciones: {mejores}")


# ==========================================================
# 4) POLÍTICA FINAL
# ==========================================================
print("\n====================================")
print("POLÍTICA FINAL APRENDIDA (GYM):")
for e in energias[::-1]:
    for f in fatigas:
        s = nombre_estado(e, f)
        mejor_accion = max(Q[s], key=lambda a: Q[s][a])
        print(f"En estado {s} (energía={e}, fatiga={f}) -> '{mejor_accion}'")
print("====================================")


# ==========================================================
# 5) SIMULACIÓN DE UNA SEMANA (USANDO LA POLÍTICA APRENDIDA)
# ==========================================================
print("\nSIMULACIÓN (7 días) con la política aprendida:")
estado = nombre_estado(2, 1)  # ejemplo: empiezas con energía alta, fatiga media
for dia in range(1, 8):
    accion = max(Q[estado], key=lambda a: Q[estado][a])
    nuevo_estado, recompensa, terminado = transicion(estado, accion)
    print(f"Día {dia}: {estado} -> acción={accion:12s} -> {nuevo_estado} | recompensa={recompensa:.1f}")
    estado = nuevo_estado