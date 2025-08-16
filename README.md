# Computación II - Universidad de Mendoza

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Universidad](https://img.shields.io/badge/Universidad-Mendoza-red.svg)](https://um.edu.ar/)
[![Carrera](https://img.shields.io/badge/Carrera-Ing.%20Informática-green.svg)](https://www.um.edu.ar/ingenieria/)

Repositorio personal para la materia **Computación II** de la carrera de Ingeniería en Informática.

## 📋 Información de la Materia

- **Universidad:** Universidad de Mendoza - Facultad de Ingeniería
- **Carrera:** Ingeniería en Informática  
- **Materia:** Computación II (Código: 2038)
- **Año:** Tercer año
- **Carga Horaria:** 4 horas semanales (120 horas totales)
- **Correlativas:** Computación I, Sistemas Operativos
- **Profesores:** Ing. Gabriel Quintero, Ing. Carlos Taffernaberry

## 🎯 Objetivos de la Materia

La materia Computación II profundiza en herramientas de desarrollo de software, programación concurrente y sistemas distribuidos:

- Utilizar herramientas de **control de versiones** y trabajo colaborativo
- Implementar **programación concurrente** y resolver problemas de sincronización
- Desarrollar aplicaciones de red con **Sockets**
- Implementar soluciones de **programación paralela y asincrónica**
- Utilizar herramientas de **orquestación de servicios** (Docker)

## 📚 Temario

### **Capítulo 1:** Conceptos Básicos
- Modelo de ejecución de programas
- Herramientas de depuración y control de versiones
- Trabajo colaborativo en grupo

### **Capítulo 2:** Programación Concurrente
- Procesos e hilos
- Problemas clásicos de concurrencia
- Mecanismos de sincronización: semáforos, memoria compartida, paso de mensajes

### **Capítulo 3:** API de Sockets
- Introducción a los sockets y modelos de comunicación en redes
- Creación y gestión de sockets en TCP/IP

### **Capítulo 4:** Programación Paralela
- Justificación y modelos de paralelización
- Problemas comunes: interbloqueo, inanición y condiciones de carrera
- Algoritmos paralelos y distribución de tareas

### **Capítulo 5:** Programación Asíncrona
- Paradigma de programación asíncrona
- Diferencias entre operaciones bloqueantes, no bloqueantes y asincrónicas
- Uso de eventos y colas de tareas distribuidas

### **Capítulo 6:** Orquestación de Servicios
- Introducción a Docker: manejo de imágenes, contenedores y redes
- Uso de Docker Compose y archivos YAML

## 📁 Estructura del Repositorio

```
Computacion-II/
├── README.md                    # Este archivo
├── TP1_desarrollo/              # Trabajo Práctico 1
│   ├── main.py                  # Sistema principal
│   ├── verificar_cadena.py      # Verificador de integridad
│   ├── README.md               # Documentación del TP1
│   ├── blockchain.json         # Blockchain generada
│   └── reporte.txt            # Reporte estadístico
├── TP2/                        # Trabajo Práctico 2 (próximamente)
├── TP3/                        # Trabajo Práctico 3 (próximamente)
├── TP4/                        # Trabajo Práctico 4 (próximamente)
└── TP5/                        # Trabajo Práctico 5 (próximamente)
```

## 🚀 Trabajos Prácticos

### ✅ TP1 - Sistema Concurrente de Análisis Biométrico
**Estado:** **COMPLETADO** ✅

Sistema distribuido que simula monitoreo biométrico en tiempo real con blockchain local.

**Características:**
- **Programación concurrente** con procesos independientes
- **Comunicación IPC** (Pipes y Queues)
- **Análisis estadístico** con ventana móvil temporal
- **Blockchain local** para integridad de datos
- **Verificación externa** de integridad

**Tecnologías:** Python 3.9+, multiprocessing, hashlib, JSON

[📖 Ver documentación completa del TP1](./TP1_desarrollo/README.md)

### 🔄 TP2 - Aplicaciones Cliente-Servidor
**Estado:** Pendiente

### 🔄 TP3 - Programación Paralela
**Estado:** Pendiente

### 🔄 TP4 - Tareas Asíncronas
**Estado:** Pendiente

### 🔄 TP5 - Orquestación con Docker
**Estado:** Pendiente

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.9+
- **Concurrencia:** multiprocessing, threading
- **Comunicación:** Pipes, Queues, Sockets
- **Datos:** JSON, CSV, databases
- **Contenedores:** Docker, Docker Compose
- **Control de versiones:** Git, GitHub
- **Testing:** unittest, pytest

## 🏆 Evaluación

### Criterios de Regularización
- ✅ **Asistencia mínima:** 80% a clases
- ✅ **Trabajos prácticos:** 100% aprobados
- ✅ **Examen final:** Desarrollo y defensa de aplicación

### Puntuaciones Actuales
| TP | Descripción | Estado | Calificación |
|----|-------------|--------|--------------|
| TP1 | Análisis Biométrico Concurrente | ✅ Entregado | Pendiente |
| TP2 | Cliente-Servidor | 🔄 Pendiente | - |
| TP3 | Programación Paralela | 🔄 Pendiente | - |
| TP4 | Tareas Asíncronas | 🔄 Pendiente | - |
| TP5 | Orquestación Docker | 🔄 Pendiente | - |

## 📖 Bibliografía

### Principal
- **The Little Book of Semaphores** - Allen B. Downey (2016)
- **Programación Concurrente y en Tiempo Real** - Vallejo, González, Albusac (2016)
- **Parallel Programming with Python** - Jan Palach (2014)
- **Mastering Docker** - Russ McKendrick, Scott Gallagher (2018)

### Referencias Adicionales
- [Python Official Documentation](https://docs.python.org/)
- [Multiprocessing Guide](https://docs.python.org/3/library/multiprocessing.html)
- [Docker Documentation](https://docs.docker.com/)

## 🚀 Cómo Usar Este Repositorio

### Prerrequisitos
```bash
# Python 3.9 o superior
python3 --version

# Git para control de versiones
git --version
```

### Clonar el Repositorio
```bash
git clone https://github.com/abenavidezUM/Computacion-II.git
cd Computacion-II
```

### Ejecutar TP1
```bash
cd TP1_desarrollo
python3 main.py
python3 verificar_cadena.py
```

## 📞 Contacto

**Estudiante:** Benavidez Agustin  
**Email:** a.benavidez@alumno.um.edu.ar  
**Universidad:** Universidad de Mendoza  
**Carrera:** Ingeniería en Informática  

## 📄 Licencia

Este repositorio contiene material académico para fines educativos. 

---

**📚 Universidad de Mendoza - Facultad de Ingeniería**  
**🎓 Ingeniería en Informática - Computación II**  
**📅 Ciclo Lectivo 2025**