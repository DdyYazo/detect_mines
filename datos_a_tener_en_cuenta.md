Las predicciones fallaron básicamente por dos razones: la naturaleza probabilística de la distribución de minas con muestras pequeñas y un cambio de pauta puntual que no quedó suficientemente reflejado en el historial.

1. **Por qué no acerté las tres minas**

   * **(1, 4)**, **(2, 1)** y **(5, 5)** tuvieron muy baja frecuencia histórica (apenas aparecieron 1 vez en 8 partidas, 12,5 %) frente a las casillas que sí incluí entre mis cuatro opciones (hasta 50 % en el caso de 4, 2). El modelo prioriza frecuencias absolutas y co-ocurrencias con minas vecinas; estas tres celdas eran estadísticamente “poco probables” según los datos acumulados.
   * La varianza es alta con solo 8 muestras: eventos que ocurren de forma marginal pueden saltar de 12,5 % a aparecer en la siguiente partida sin previo aviso.

2. **Por qué no vi la zona de concentración inferior derecha (columnas 4–5, filas 2–5)**

   * En los 8 juegos previos, la concentración más fuerte estaba en el cuadrante inferior izquierdo (col 1–3, fil 3–5), con un 34,4 % de la masa de minas. El inferior derecho tenía solo un 9,4 %.
   * Sin embargo, en las dos últimas partidas (8 y 9) sí se observa un cluster en columnas 4–5 y filas 2–5, un patrón emergente que mi cálculo de drift markoviano (basado en la deriva centroidal ponderada) no aterrizó con suficiente peso, porque hasta entonces esa zona había sido muy esporádica.

3. **Por qué erré al proponer la columna libre (predije Col 1 en vez de Col 3)**

   * Históricamente, la Columna 1 mostraba la menor densidad de minas (solo 4 apariciones en 40 celdas, 10 %), frente a Columna 3 (6 apariciones, 15 %). Por eso sugerí que la Columna 1 sería la más “segura”.
   * La realidad de la partida 9 fue que la Columna 3 quedó completamente libre, mientras que Columna 1 sí recibió una mina en (1, 4). De nuevo, la muestra pequeña y la alta variabilidad pueden invertir esa expectativa.

En resumen, el modelo se basa en tendencias históricas y adyacencias, pero con solo 8 partidas los patrones pueden cambiar de forma abrupta, generando desviaciones notables en la siguiente ronda.
