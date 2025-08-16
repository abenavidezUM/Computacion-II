# Sistema Concurrente de Análisis Biométrico con Blockchain

**Trabajo Práctico 1 - Computación II**  
**Universidad de Mendoza - Facultad de Ingeniería**

## 📋 Descripción

Este proyecto implementa un sistema distribuido que simula el monitoreo biométrico en tiempo real de una prueba de esfuerzo, procesando señales de manera concurrente y almacenando los resultados en una blockchain local para garantizar la integridad de los datos.

### 🏗️ Arquitectura del Sistema

```
┌─────────────────────────┐                     
│  Proceso Principal      │  1 dato/seg         
│  (generador)            │─────────────┐       
└─────────────────────────┘             │       
        │ pipe/fifo                     │       
        ▼                               ▼       
┌────────────┐  ┌────────────┐  ┌────────────┐
│ Proc A     │  │ Proc B     │  │ Proc C     │
│ Frecuencia │  │ Presión    │  │ Oxígeno    │
└─────┬──────┘  └─────┬──────┘  └─────┬──────┘
      │ queue         │ queue         │ queue  
      └───────┬────────┴────────┬──────┘       
              ▼                 ▼              
         ┌─────────────────────────┐           
         │  Proceso Verificador    │           
         └────────┬────────────────┘           
                  │ escribe bloque             
                  ▼                           
         ┌─────────────────────────┐           
         │  Cadena de Bloques      │           
         └─────────────────────────┘           
```

## 🔧 Requisitos Técnicos

- **Python ≥ 3.9** (probado con Python 3.13.3)
- **Librerías utilizadas:** 
  - `multiprocessing` - Comunicación entre procesos
  - `hashlib` - Funciones de hash SHA-256
  - `json` - Manejo de archivos JSON
  - `datetime` - Manejo de timestamps
  - `random` - Generación de datos simulados
  - `collections` - Estructuras de datos eficientes

## 📁 Estructura de Archivos

```
TP1_desarrollo/
├── main.py                 # Programa principal del sistema
├── verificar_cadena.py     # Script de verificación independiente
├── README.md              # Este archivo
├── blockchain.json        # Blockchain generada (después de ejecución)
└── reporte.txt           # Reporte estadístico (después de verificación)
```

## 🚀 Instrucciones de Ejecución

### 1. Ejecutar el Sistema Principal

```bash
python3 main.py
```

**¿Qué hace este comando?**
- Inicia el proceso generador de datos biométricos
- Lanza 3 procesos analizadores (frecuencia, presión, oxígeno)
- Ejecuta el proceso verificador de blockchain
- Genera 60 muestras (1 por segundo) durante 1 minuto
- Crea el archivo `blockchain.json` con la cadena de bloques

**Salida esperada:**
```
🏥 Sistema de Análisis Biométrico con Blockchain
==================================================
🔄 Iniciando generación de datos biométricos...
📊 Generando 60 muestras (1 por segundo)
🔬 Analizador de frecuencia iniciado
🔬 Analizador de presion iniciado
🔬 Analizador de oxigeno iniciado
🔐 Verificador de blockchain iniciado
📈 Muestra  1/60: FC=120 bpm, PA=140/85 mmHg, O2=98%
📊 Frecuencia: ventana=1 muestras, media=120.00, std=0.00
📊 Presion: ventana=1 muestras, media=140.00, std=0.00
📊 Oxigeno: ventana=1 muestras, media=98.00, std=0.00
🔗 Bloque  1: a7f3e8d92b... ✅ Normal
...
```

### 2. Verificar la Integridad de la Blockchain

```bash
python3 verificar_cadena.py
```

**¿Qué hace este comando?**
- Lee el archivo `blockchain.json` generado
- Recalcula todos los hashes SHA-256
- Verifica el encadenamiento correcto
- Detecta bloques corruptos (si los hay)
- Genera el archivo `reporte.txt` con estadísticas

**Salida esperada:**
```
🔍 Verificador de Integridad de Blockchain
Trabajo Práctico 1 - Computación II
=============================================
✅ Blockchain cargada: 60 bloques

🔍 Verificando integridad de la blockchain...
==================================================
✅ Bloque  0: a7f3e8d92b... - Válido
✅ Bloque  1: b8e4f9e03c... - Válido
...
==================================================
🎉 ¡Blockchain íntegra! Todos los bloques son válidos.

📊 Generando reporte estadístico...
✅ Reporte guardado en: reporte.txt
```

### 3. Revisar los Resultados

#### Archivo `blockchain.json`
Contiene la cadena de bloques completa con la estructura:
```json
[
  {
    "timestamp": "2025-01-08T14:30:01",
    "datos": {
      "frecuencia": {"media": 120.5, "desv": 8.2},
      "presion": {"media": 145.3, "desv": 12.1},
      "oxigeno": {"media": 97.8, "desv": 1.4}
    },
    "alerta": false,
    "prev_hash": "",
    "hash": "a7f3e8d92b4c5f6e8d9a0b1c2d3e4f5g6h7i8j9k0l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5"
  }
]
```

#### Archivo `reporte.txt`
Contiene estadísticas completas:
```
REPORTE DE ANÁLISIS BIOMÉTRICO CON BLOCKCHAIN
==================================================

📈 ESTADÍSTICAS GENERALES
-------------------------
Total de bloques procesados: 60
Bloques con alertas médicas: 8
Porcentaje de alertas: 13.3%
Integridad de la cadena: 100%

🏥 PROMEDIOS BIOMÉTRICOS
-------------------------
Frecuencia cardíaca promedio: 125.4 bpm
Presión arterial promedio: 142.8 mmHg
Oxígeno en sangre promedio: 95.6%

🔐 VERIFICACIÓN DE INTEGRIDAD
------------------------------
✅ Blockchain íntegra - Sin bloques corruptos
```

## 🔍 Funcionalidades Implementadas

### ✅ Tarea 1 - Generación y Análisis Concurrente (30%)
- [x] Proceso principal que genera datos cada segundo
- [x] Formato exacto de datos biométricos
- [x] Comunicación IPC mediante Pipes
- [x] 3 procesos analizadores independientes
- [x] Ventana móvil temporal de 30 segundos
- [x] Cálculo de media y desviación estándar
- [x] Sin condiciones de carrera

### ✅ Tarea 2 - Verificación y Construcción de Bloques (35%)
- [x] Sincronización de resultados por timestamp
- [x] Validación de rangos médicos
- [x] Detección de alertas automática
- [x] Construcción correcta de bloques
- [x] Hash SHA-256 según especificación
- [x] Encadenamiento íntegro
- [x] Persistencia en `blockchain.json`
- [x] Output informativo en pantalla

### ✅ Tarea 3 - Verificación de Integridad y Reporte (35%)
- [x] Script independiente `verificar_cadena.py`
- [x] Recálculo y verificación de hashes
- [x] Detección de bloques corruptos
- [x] Generación de `reporte.txt`
- [x] Estadísticas completas

### ✅ Bonus - Código Limpio y Documentación (+10%)
- [x] Estilo PEP 8
- [x] Documentación completa
- [x] README detallado
- [x] Manejo de excepciones
- [x] Comentarios explicativos

## ⚠️ Consideraciones Importantes

### Gestión de Procesos
- El sistema maneja automáticamente la creación y terminación de procesos
- Utiliza `process.join()` para evitar procesos zombie
- Manejo de `KeyboardInterrupt` para terminación limpia

### Sincronización Temporal
- Los analizadores mantienen ventanas móviles de exactamente 30 segundos
- El verificador espera los 3 resultados del mismo timestamp antes de crear bloques
- Utilización de timeouts para evitar bloqueos

### Validaciones Médicas
- **Frecuencia cardíaca:** Alerta si ≥ 200 bpm
- **Oxígeno en sangre:** Alerta si < 90% o > 100%
- **Presión sistólica:** Alerta si ≥ 200 mmHg

### Algoritmo de Hash
```python
# Fórmula exacta utilizada:
hash = sha256(prev_hash + str(datos) + timestamp)
```

## 🐛 Solución de Problemas

### Error: "No se encontró el archivo blockchain.json"
**Solución:** Ejecutar primero `python3 main.py` para generar la blockchain.

### Error: "ModuleNotFoundError"
**Solución:** Verificar que se esté usando Python ≥ 3.9. Todas las librerías utilizadas son parte de la biblioteca estándar.

### El programa se cuelga
**Solución:** Usar `Ctrl+C` para interrumpir. El sistema tiene manejo de excepciones para terminar limpiamente.

### Proceso no termina
**Solución:** Verificar que no haya procesos zombie con `ps aux | grep python` y terminarlos si es necesario.

## 📊 Métricas de Rendimiento

- **Tiempo de ejecución:** ~60 segundos (1 muestra por segundo)
- **Memoria utilizada:** ~50MB promedio
- **Procesos concurrentes:** 5 (1 principal + 3 analizadores + 1 verificador)
- **Archivos generados:** 2 (`blockchain.json` + `reporte.txt`)

## 👥 Información del Desarrollo

**Materia:** Computación II - Universidad de Mendoza  
**Carrera:** Ingeniería en Informática  
**Profesores:** Ing. Gabriel Quintero, Ing. Carlos Taffernaberry  

---

**¡Listo para ejecutar!** 🚀

Para cualquier consulta sobre el funcionamiento del sistema, revisar los comentarios en el código fuente o contactar al desarrollador.
