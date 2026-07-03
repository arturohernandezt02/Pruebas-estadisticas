# Calculadora de Pruebas Estadísticas de Independencia (LCG)

Este proyecto es una aplicación de escritorio desarrollada en Python con la biblioteca **CustomTkinter** que implementa un **Generador Congruencial Lineal (LCG)** y evalúa las propiedades estadísticas de las secuencias de números pseudoaleatorios generadas.

La aplicación permite experimentar con diferentes parámetros de generación y realizar pruebas de independencia matemáticas de forma inmediata, facilitando la identificación de combinaciones de parámetros que pasen los criterios estadísticos de aleatoriedad.

---

## Propósito y ¿Para qué sirve?

En el modelado y simulación por computadora (por ejemplo, simulaciones de Monte Carlo), contar con generadores de números pseudoaleatorios ($R_i$) de alta calidad es fundamental. Un mal generador puede sesgar y arruinar los resultados de un experimento complejo.

Esta herramienta sirve para:
1. **Generar números pseudoaleatorios**: Utilizando el algoritmo matemático Congruencial Lineal.
2. **Validar la independencia y uniformidad**: Someter la secuencia a 4 pruebas estadísticas rigurosas y estándar de la industria.
3. **Buscar configuraciones exitosas**: Guardar únicamente aquellas configuraciones de generador ($X_0, a, c, m$) cuyos números aprueben la totalidad de los tests y puedan ser utilizados con seguridad en proyectos de simulación.

---

## Arquitectura y Estructura del Proyecto

El proyecto está diseñado bajo el patrón de arquitectura **Modelo-Vista-Controlador (MVC)** para garantizar una separación limpia de responsabilidades y facilitar su mantenimiento.

```
Pruebas-estadisticas/
│
├── motor_estadistico.py   # [El Modelo] Lógica matemática, algoritmos y las 4 pruebas.
├── gui_app.py            # [La Vista] Interfaz gráfica, paleta de colores y componentes CustomTkinter.
├── main.py               # [El Controlador] Punto de entrada que coordina el modelo y la vista.
└── README.md             # Esta documentación explicativa.
```

### Descripción de Módulos

*   **`motor_estadistico.py` (Modelo)**: Libre de dependencias de interfaces gráficas. Contiene las funciones para calcular e interpretar las pruebas, devolviendo los resultados en variables estructuradas y en textos formateados en monospace.
*   **`gui_app.py` (Vista)**: Define los widgets, grids, estilos visuales retro (paleta vintage de tonos crema, salvia, carbón y ocre) y cuadros de texto scrollables (`CTkTextbox`) que permiten desplazarse y copiar fácilmente los resultados.
*   **`main.py` (Controlador)**: Se encarga de instanciar la vista, vincular los callbacks de los botones, validar que las entradas del usuario sean correctas (enteros no negativos, módulo mayor que 0) y comandar el flujo completo de evaluación y exportación.

---

## Cómo Funciona: Lógica y Pruebas Estadísticas

### 1. Generador Congruencial Lineal (LCG)
Genera la secuencia mediante la ecuación recursiva clásica:
$$X_{i+1} = (a \cdot X_i + c) \pmod m$$
$$R_i = \frac{X_i}{m}$$
Donde:
*   $X_0$ es la **Semilla** (valor inicial).
*   $a$ es la **Constante Multiplicativa**.
*   $c$ es el **Incremento**.
*   $m$ es el **Módulo**.
*   $R_i$ son los números pseudoaleatorios resultantes en el intervalo $[0, 1)$.

La aplicación genera una cantidad máxima de números igual a $m$ (o limitada a 10,000 para preservar el desempeño de la interfaz en módulos gigantes).

### 2. Las 4 Pruebas de Independencia

Cada una de las pruebas utiliza un nivel de significancia del 5% ($\alpha = 0.05$).

*   **Prueba de Promedios**:
    *   *Propósito*: Evaluar si la media aritmética ($\bar{r}$) de los números generados es estadísticamente equivalente a $0.5$ (la media teórica de una distribución uniforme continua $U(0,1)$).
    *   *Estadístico*: $Z_0 = (\bar{r} - 0.5) \sqrt{12N}$
    *   *Criterio*: Pasa si $|Z_0| \le 1.96$ (distribución normal estándar).

*   **Prueba de Frecuencias (Chi-cuadrada)**:
    *   *Propósito*: Determinar si los números están distribuidos uniformemente en todo el intervalo $[0, 1)$.
    *   *Lógica*: Divide el espacio en 10 clases iguales ($[0.0-0.1), [0.1-0.2), \dots, [0.9-1.0)$) y cuenta la frecuencia observada ($O_i$) en cada una, comparándola contra la frecuencia esperada uniforme $E_i = N/10$.
    *   *Estadístico*: $\chi^2_0 = \sum_{i=1}^{10} \frac{(O_i - E_i)^2}{E_i}$
    *   *Criterio*: Pasa si $\chi^2_0 \le 16.919$ (grados de libertad $df = 9$).

*   **Prueba de Póquer**:
    *   *Propósito*: Validar la aleatoriedad analizando los patrones que forman los decimales individuales.
    *   *Lógica*: Toma los primeros 5 decimales de cada número como una "mano" y la clasifica en una de las 7 categorías: *Todos Diferentes (TD)*, *Un Par (1P)*, *Dos Pares (2P)*, *Tercia (T)*, *Full House (FH)*, *Póquer (P)* y *Quintilla (Q)*. Luego, compara las frecuencias reales observadas contra la probabilidad teórica de ocurrencia de cada mano.
    *   *Estadístico*: $\chi^2_0 = \sum \frac{(O_j - E_j)^2}{E_j}$
    *   *Criterio*: Pasa si $\chi^2_0 \le 12.592$ (grados de libertad $df = 6$).

*   **Prueba de Corridas (Arriba y abajo de la media)**:
    *   *Propósito*: Evaluar la ausencia de tendencias sistemáticas u oscilaciones recurrentes en el orden de los datos.
    *   *Lógica*: Compara cada número contra la media de la secuencia para crear una lista de signos $+$ y $-$. Cuenta el número total de rachas continuas de signos idénticos (corridas, $b$).
    *   *Estadístico*: $Z_0 = \frac{b - \mu_b}{\sigma_b}$, donde $\mu_b$ y $\sigma_b^2$ son la media y varianza teóricas del número de corridas.
    *   *Criterio*: Pasa si $|Z_0| \le 1.96$.

---

## Cómo Ejecutar la Aplicación

### Prerrequisitos
Debe contar con Python 3 instalado, así como la biblioteca `customtkinter`:

```bash
pip install customtkinter
```

### Ejecución
Para iniciar el programa, ejecute el controlador `main.py` desde la terminal:

```bash
python main.py
```

---

## Ejemplo de Configuración Exitosa

Debido a la naturaleza del algoritmo congruencial lineal, muchas combinaciones básicas (como la que viene por defecto $X_0=17, a=121, c=0, m=1000$) fallarán debido a que su módulo pequeño limita los dígitos decimales disponibles o produce ciclos repetitivos sumamente cortos.

Para probar la funcionalidad completa del programa y la exportación de archivos, ingrese la siguiente configuración ganadora (que cumple con el teorema de Hull-Dobell para el periodo completo):

*   **Semilla ($X_0$)**: `9432`
*   **Constante ($a$)**: `2241`
*   **Incremento ($c$)**: `23`
*   **Módulo ($m$)**: `10000`

Presione **Generar y Evaluar**. Verá que los cuatro indicadores inferiores se encienden en verde (**PASÓ**), el reporte matemático detallado aparecerá en las pestañas y el botón **Exportar Configuración** se habilitará para guardar el archivo.
