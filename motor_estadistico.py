import math

def generar_numeros(x0, a, c, m, max_n=10000):
    """
    Genera números pseudoaleatorios usando un Generador Congruencial Lineal (LCG).
    X_{i+1} = (a * X_i + c) % m
    R_i = X_i / m
    
    Retorna la lista de valores de R_i.
    """
    numeros = []
    x = x0
    # Generamos un número de elementos igual a 'm' pero acotado a 'max_n'
    # para evitar problemas de rendimiento con módulos extremadamente grandes.
    n = min(m, max_n)
    for _ in range(n):
        x = (a * x + c) % m
        numeros.append(x / m)
    return numeros

def prueba_promedios(numeros):
    """
    Prueba de Promedios:
    Verifica si la media muestral es significativamente distinta de 0.5.
    """
    n = len(numeros)
    if n == 0:
        return False, 0.0, 0.0, 1.96, "No hay números para evaluar."
        
    media = sum(numeros) / n
    # Desviación estándar teórica del promedio en U(0,1): 1 / sqrt(12 * n)
    sigma = 1 / math.sqrt(12 * n)
    z0 = (media - 0.5) / sigma
    
    z_critico = 1.96  # Para alpha = 0.05 (confianza 95%)
    paso = abs(z0) <= z_critico
    
    detalle = (
        "=== PRUEBA DE PROMEDIOS ===\n"
        f"Cantidad de datos (N): {n}\n"
        f"Media muestral (r-barra): {media:.6f}\n"
        f"Valor esperado (mu): 0.500000\n"
        f"Estadístico Z0 calculado: {z0:.6f}\n"
        f"Valor crítico Z(alpha/2) [alpha=0.05]: {z_critico}\n"
        f"Resultado: {'PASÓ' if paso else 'FALLÓ'} (Pasa si |Z0| <= {z_critico})\n"
    )
    return paso, media, z0, z_critico, detalle

def prueba_frecuencias(numeros):
    """
    Prueba de Frecuencias (Chi-cuadrada):
    Divide el rango [0, 1) en 10 intervalos y compara las frecuencias
    observadas con las esperadas (N/10).
    """
    n = len(numeros)
    if n == 0:
        return False, 0.0, 16.919, {}, "No hay números para evaluar."
        
    k = 10
    esperada = n / k
    observadas = [0] * k
    
    for x in numeros:
        idx = int(x * k)
        if idx >= k:
            idx = k - 1
        elif idx < 0:
            idx = 0
        observadas[idx] += 1
        
    chi0 = 0.0
    filas_detalle = []
    for i in range(k):
        obs = observadas[i]
        diff_sq_div = ((obs - esperada) ** 2) / esperada if esperada > 0 else 0.0
        chi0 += diff_sq_div
        filas_detalle.append((f"[{i/k:.1f} - {(i+1)/k:.1f})", obs, esperada, diff_sq_div))
        
    chi_critico = 16.919  # Para alpha = 0.05 y grados de libertad df = 9
    paso = chi0 <= chi_critico
    
    detalle = (
        "=== PRUEBA DE FRECUENCIAS (CHI-CUADRADA) ===\n"
        f"Cantidad de datos (N): {n}\n"
        f"Número de intervalos (k): {k}\n"
        f"Frecuencia esperada por intervalo: {esperada:.2f}\n\n"
        f"{'Intervalo':<15} | {'Obs. (O)':<8} | {'Esp. (E)':<8} | {'(O-E)^2/E':<10}\n"
        f"{'-'*50}\n"
    )
    for intervalo, obs, esp, val in filas_detalle:
        detalle += f"{intervalo:<15} | {obs:<8} | {esp:<8.2f} | {val:.6f}\n"
        
    detalle += (
        f"{'-'*50}\n"
        f"Estadístico Chi0^2 calculado: {chi0:.6f}\n"
        f"Valor crítico Chi^2(0.05, 9): {chi_critico}\n"
        f"Resultado: {'PASÓ' if paso else 'FALLÓ'} (Pasa si Chi0^2 <= {chi_critico})\n"
    )
    
    tabla_dict = {f"[{i/10:.1f}-{(i+1)/10:.1f})": o for i, o in enumerate(observadas)}
    return paso, chi0, chi_critico, tabla_dict, detalle

def prueba_poker(numeros):
    """
    Prueba de Póquer (Clasificación de 5 decimales):
    Clasifica las manos de 5 decimales en 7 categorías y evalúa con Chi-cuadrada.
    """
    n = len(numeros)
    if n == 0:
        return False, 0.0, 12.592, {}, "No hay números para evaluar."
        
    # Probabilidades de cada categoría para 5 dígitos independientes
    probs = {
        "TD": 0.30240,  # Todos Diferentes
        "1P": 0.50400,  # Un Par
        "2P": 0.10800,  # Dos Pares
        "T":  0.07200,  # Tercia
        "FH": 0.00900,  # Full House
        "P":  0.00450,  # Póquer (4 iguales)
        "Q":  0.00010   # Quintilla (5 iguales)
    }
    
    nombres_completo = {
        "TD": "Todos Diferentes (TD)",
        "1P": "Un Par (1P)",
        "2P": "Dos Pares (2P)",
        "T":  "Tercia (T)",
        "FH": "Full House (FH)",
        "P":  "Póquer (P)",
        "Q":  "Quintilla (Q)"
    }
    
    observadas = {cat: 0 for cat in probs}
    
    for x in numeros:
        # Extraer los primeros 5 decimales de forma robusta
        s = f"{x:.12f}".split('.')[1][:5]
        
        # Contar ocurrencias de cada dígito
        counts = {}
        for d in s:
            counts[d] = counts.get(d, 0) + 1
        
        val_counts = sorted(list(counts.values()), reverse=True)
        if val_counts == [1, 1, 1, 1, 1]:
            cat = "TD"
        elif val_counts == [2, 1, 1, 1]:
            cat = "1P"
        elif val_counts == [2, 2, 1]:
            cat = "2P"
        elif val_counts == [3, 1, 1]:
            cat = "T"
        elif val_counts == [3, 2]:
            cat = "FH"
        elif val_counts == [4, 1]:
            cat = "P"
        elif val_counts == [5]:
            cat = "Q"
        else:
            cat = "TD"  # Fallback
            
        observadas[cat] += 1
        
    chi0 = 0.0
    filas_detalle = []
    
    for cat in probs:
        obs = observadas[cat]
        esp = n * probs[cat]
        diff_sq_div = ((obs - esp) ** 2) / esp if esp > 0 else 0.0
        chi0 += diff_sq_div
        filas_detalle.append((nombres_completo[cat], obs, esp, diff_sq_div))
        
    chi_critico = 12.592  # Para grados de libertad df = 6 y alpha = 0.05
    paso = chi0 <= chi_critico
    
    detalle = (
        "=== PRUEBA DE PÓQUER ===\n"
        f"Cantidad de datos (N): {n}\n\n"
        f"{'Categoría':<22} | {'Obs. (O)':<8} | {'Esp. (E)':<8} | {'(O-E)^2/E':<10}\n"
        f"{'-'*55}\n"
    )
    for cat_name, obs, esp, val in filas_detalle:
        detalle += f"{cat_name:<22} | {obs:<8} | {esp:<8.2f} | {val:.6f}\n"
        
    detalle += (
        f"{'-'*55}\n"
        f"Estadístico Chi0^2 calculado: {chi0:.6f}\n"
        f"Valor crítico Chi^2(0.05, 6): {chi_critico}\n"
        f"Resultado: {'PASÓ' if paso else 'FALLÓ'} (Pasa si Chi0^2 <= {chi_critico})\n"
    )
    
    return paso, chi0, chi_critico, observadas, detalle

def prueba_corridas(numeros):
    """
    Prueba de Corridas (Arriba y Abajo de la media muestral):
    Evalúa la secuencia de signos comparando cada número con la media.
    """
    n = len(numeros)
    if n == 0:
        return False, 0, 0, 0, 0.0, 0.0, 0.0, 1.96, "No hay números para evaluar."
        
    warning = ""
    if n < 20:
        warning = "\nAdvertencia: N < 20. La aproximación normal Z puede no ser confiable.\n"
        
    # Calculamos la media muestral como el umbral
    media = sum(numeros) / n
    
    secuencia = []
    for x in numeros:
        if x >= media:
            secuencia.append('+')
        else:
            secuencia.append('-')
            
    n1 = secuencia.count('+')
    n2 = secuencia.count('-')
    
    if n1 == 0 or n2 == 0:
        detalle = (
            "=== PRUEBA DE CORRIDAS (ARRIBA Y ABAJO DE LA MEDIA) ===\n"
            f"Cantidad de datos (N): {n}\n"
            "Todos los números están de un solo lado de la media. No es posible evaluar la prueba.\n"
        )
        return False, 1, n1, n2, 1.0, 0.0, 999.0, 1.96, detalle
        
    # Contar corridas (b)
    b = 1
    for i in range(1, len(secuencia)):
        if secuencia[i] != secuencia[i-1]:
            b += 1
            
    # Media esperada
    expected_runs = (2.0 * n1 * n2 / n) + 1.0
    
    # Varianza esperada
    numerador_var = 2.0 * n1 * n2 * (2.0 * n1 * n2 - n)
    denominador_var = (n ** 2) * (n - 1)
    variance = numerador_var / denominador_var
    
    std_dev = math.sqrt(variance)
    if std_dev > 0:
        z0 = (b - expected_runs) / std_dev
    else:
        z0 = 0.0
        
    z_critico = 1.96  # Para alpha = 0.05
    paso = abs(z0) <= z_critico
    
    # Formatear la secuencia de signos para mostrar (primeros 60 caracteres)
    sec_str = "".join(secuencia)
    if len(sec_str) > 60:
        sec_display = sec_str[:57] + "..."
    else:
        sec_display = sec_str
        
    detalle = (
        "=== PRUEBA DE CORRIDAS (ARRIBA Y ABAJO DE LA MEDIA) ===\n"
        f"Cantidad de datos (N): {n}\n"
        f"Umbral de media muestral: {media:.6f}\n"
        f"Secuencia de signos ({n1} '+', {n2} '-'):\n{sec_display}\n\n"
        f"Cantidad de corridas observadas (b): {b}\n"
        f"Media esperada (mu_b): {expected_runs:.6f}\n"
        f"Varianza esperada (sigma_b^2): {variance:.6f}\n"
        f"Estadístico Z0 calculado: {z0:.6f}\n"
        f"Valor crítico Z(alpha/2) [alpha=0.05]: {z_critico}\n"
        f"Resultado: {'PASÓ' if paso else 'FALLÓ'} (Pasa si |Z0| <= {z_critico})\n"
        f"{warning}"
    )
    
    return paso, b, n1, n2, expected_runs, variance, z0, z_critico, detalle
