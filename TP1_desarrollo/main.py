#!/usr/bin/env python3
"""
Sistema Concurrente de Análisis Biométrico con Cadena de Bloques Local
Trabajo Práctico 1 - Computación II

Autor: Benavidez Agustin
Fecha: 2025

Este programa implementa un sistema distribuido que:
1. Genera datos biométricos simulados en tiempo real
2. Procesa cada señal en paralelo usando IPC y multiprocessing
3. Valida y almacena resultados en una blockchain local
"""

import multiprocessing as mp
import time
import json
import hashlib
import random
import datetime
from typing import Dict, List, Any
from collections import deque


class BiometricGenerator:
    """Generador de datos biométricos simulados."""
    
    def __init__(self):
        self.sample_count = 60  # 60 muestras total
        
    def generate_sample(self) -> Dict[str, Any]:
        """
        Genera una muestra biométrica con el formato exacto requerido.
        
        Returns:
            dict: Muestra con timestamp, frecuencia, presión y oxígeno
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        sample = {
            "timestamp": timestamp,
            "frecuencia": random.randint(60, 180),
            "presion": [random.randint(110, 180), random.randint(70, 110)],  # [sistólica, diastólica]
            "oxigeno": random.randint(90, 100)
        }
        
        return sample
    
    def run(self, pipes: List):
        """
        Proceso principal que genera datos cada segundo.
        
        Args:
            pipes: Lista de pipes para comunicación con analizadores
        """
        print("🔄 Iniciando generación de datos biométricos...")
        print(f"📊 Generando {self.sample_count} muestras (1 por segundo)")
        
        try:
            for i in range(self.sample_count):
                sample = self.generate_sample()
                
                print(f"📈 Muestra {i+1:2d}/{self.sample_count}: "
                      f"FC={sample['frecuencia']:3d} bpm, "
                      f"PA={sample['presion'][0]}/{sample['presion'][1]} mmHg, "
                      f"O2={sample['oxigeno']:2d}%")
                
                # Enviar a todos los analizadores mediante pipes
                for pipe_conn in pipes:
                    pipe_conn.send(sample)
                
                # Esperar exactamente 1 segundo
                time.sleep(1)
                
        except Exception as e:
            print(f"❌ Error en generador: {e}")
        finally:
            # Cerrar todos los pipes
            for pipe_conn in pipes:
                pipe_conn.close()
            print("✅ Generador finalizado")


class BiometricAnalyzer:
    """Analizador de señales biométricas con ventana móvil temporal."""
    
    def __init__(self, signal_type: str):
        self.signal_type = signal_type
        self.window_data = deque()  # Ventana móvil temporal
        self.window_duration = 30  # 30 segundos
        
    def extract_signal_value(self, sample: Dict[str, Any]) -> float:
        """
        Extrae el valor de la señal específica del sample.
        
        Args:
            sample: Muestra biométrica completa
            
        Returns:
            float: Valor de la señal específica
        """
        if self.signal_type == "frecuencia":
            return float(sample["frecuencia"])
        elif self.signal_type == "presion":
            # Para presión, usamos la sistólica como valor principal
            return float(sample["presion"][0])
        elif self.signal_type == "oxigeno":
            return float(sample["oxigeno"])
        else:
            raise ValueError(f"Tipo de señal desconocido: {self.signal_type}")
    
    def update_window(self, sample: Dict[str, Any]):
        """
        Actualiza la ventana móvil temporal de 30 segundos.
        
        Args:
            sample: Nueva muestra a agregar
        """
        timestamp = datetime.datetime.strptime(sample["timestamp"], "%Y-%m-%dT%H:%M:%S")
        value = self.extract_signal_value(sample)
        
        # Agregar nueva muestra
        self.window_data.append((timestamp, value))
        
        # Remover muestras fuera de la ventana de 30 segundos
        current_time = timestamp
        while self.window_data:
            sample_time, _ = self.window_data[0]
            if (current_time - sample_time).total_seconds() > self.window_duration:
                self.window_data.popleft()
            else:
                break
    
    def calculate_statistics(self) -> tuple:
        """
        Calcula media y desviación estándar de la ventana actual.
        
        Returns:
            tuple: (media, desviación_estándar)
        """
        if not self.window_data:
            return 0.0, 0.0
            
        values = [value for _, value in self.window_data]
        n = len(values)
        
        # Media
        mean = sum(values) / n
        
        # Desviación estándar
        if n > 1:
            variance = sum((x - mean) ** 2 for x in values) / (n - 1)
            std_dev = variance ** 0.5
        else:
            std_dev = 0.0
            
        return mean, std_dev
    
    def run(self, pipe_conn, result_queue):
        """
        Proceso analizador principal.
        
        Args:
            pipe_conn: Conexión del pipe para recibir datos
            result_queue: Queue para enviar resultados al verificador
        """
        print(f"🔬 Analizador de {self.signal_type} iniciado")
        
        try:
            samples_received = 0
            
            while samples_received < 60:  # Esperar 60 muestras
                try:
                    # Recibir muestra del generador
                    sample = pipe_conn.recv()
                    samples_received += 1
                    
                    # Actualizar ventana móvil
                    self.update_window(sample)
                    
                    # Calcular estadísticas
                    mean, std_dev = self.calculate_statistics()
                    
                    # Preparar resultado (incluir datos originales para validación)
                    result = {
                        "tipo": self.signal_type,
                        "timestamp": sample["timestamp"],
                        "media": round(mean, 2),
                        "desv": round(std_dev, 2),
                        "original_data": sample  # Datos originales para validación
                    }
                    
                    # Enviar resultado al verificador
                    result_queue.put(result)
                    
                    print(f"📊 {self.signal_type.capitalize()}: "
                          f"ventana={len(self.window_data)} muestras, "
                          f"media={mean:.2f}, std={std_dev:.2f}")
                    
                except EOFError:
                    break
                    
        except Exception as e:
            print(f"❌ Error en analizador {self.signal_type}: {e}")
        finally:
            pipe_conn.close()
            print(f"✅ Analizador {self.signal_type} finalizado")


class BlockchainVerifier:
    """Verificador que construye la blockchain local."""
    
    def __init__(self):
        self.blockchain = []
        self.pending_results = {}  # timestamp -> {tipo: resultado}
        
    def is_valid_data(self, timestamp: str, results: Dict[str, Dict]) -> bool:
        """
        Valida si los datos están dentro de rangos normales usando valores originales.
        
        Args:
            timestamp: Timestamp de los datos
            results: Resultados de los tres analizadores con datos originales
            
        Returns:
            bool: True si hay alguna alerta (fuera de rango)
        """
        alert = False
        
        # Obtener datos originales de cualquiera de los analizadores (todos tienen la misma muestra)
        original_data = None
        for result in results.values():
            if "original_data" in result:
                original_data = result["original_data"]
                break
        
        if not original_data:
            print(f"⚠️  Error: No se encontraron datos originales para timestamp {timestamp}")
            return True  # Marcar como alerta si no hay datos
        
        # Validaciones según especificación: valores ORIGINALES, no medias
        frecuencia = original_data.get("frecuencia", 0)
        oxigeno = original_data.get("oxigeno", 0)
        presion = original_data.get("presion", [0, 0])
        presion_sistolica = presion[0] if len(presion) >= 1 else 0
        
        if frecuencia >= 200:
            alert = True
            print(f"⚠️  Alerta: Frecuencia alta ({frecuencia} bpm)")
            
        if not (90 <= oxigeno <= 100):
            alert = True
            print(f"⚠️  Alerta: Oxígeno fuera de rango ({oxigeno}%)")
            
        if presion_sistolica >= 200:
            alert = True
            print(f"⚠️  Alerta: Presión sistólica alta ({presion_sistolica} mmHg)")
            
        return alert
    
    def calculate_hash(self, block_data: Dict[str, Any]) -> str:
        """
        Calcula el hash SHA-256 del bloque según especificación.
        
        Args:
            block_data: Datos del bloque sin el hash
            
        Returns:
            str: Hash SHA-256 hexadecimal
        """
        prev_hash = block_data.get("prev_hash", "")
        datos_str = str(block_data["datos"])
        timestamp = block_data["timestamp"]
        
        # Hash según especificación: sha256(prev_hash + str(datos) + timestamp)
        hash_input = prev_hash + datos_str + timestamp
        return hashlib.sha256(hash_input.encode()).hexdigest()
    
    def create_block(self, timestamp: str, results: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Crea un nuevo bloque de la blockchain.
        
        Args:
            timestamp: Timestamp del bloque
            results: Resultados de los analizadores
            
        Returns:
            dict: Bloque construido
        """
        # Determinar hash del bloque anterior
        prev_hash = ""
        if self.blockchain:
            prev_hash = self.blockchain[-1]["hash"]
        
        # Detectar alertas
        alert = self.is_valid_data(timestamp, results)
        
        # Limpiar datos para el bloque (solo estadísticas, no datos originales)
        clean_results = {}
        for tipo, result in results.items():
            clean_results[tipo] = {
                "media": result["media"],
                "desv": result["desv"]
            }
        
        # Construir bloque
        block = {
            "timestamp": timestamp,
            "datos": clean_results,
            "alerta": alert,
            "prev_hash": prev_hash
        }
        
        # Calcular hash del bloque
        block["hash"] = self.calculate_hash(block)
        
        return block
    
    def save_blockchain(self):
        """Persiste la blockchain en blockchain.json."""
        try:
            with open("blockchain.json", "w") as f:
                json.dump(self.blockchain, f, indent=2)
        except Exception as e:
            print(f"❌ Error guardando blockchain: {e}")
    
    def run(self, result_queues: List[mp.Queue]):
        """
        Proceso verificador principal.
        
        Args:
            result_queues: Lista de queues de los analizadores
        """
        print("🔐 Verificador de blockchain iniciado")
        
        blocks_created = 0
        expected_blocks = 60
        
        try:
            while blocks_created < expected_blocks:
                # Recopilar resultados de los 3 analizadores para el mismo timestamp
                for queue in result_queues:
                    try:
                        result = queue.get(timeout=5)  # Timeout de 5 segundos
                        timestamp = result["timestamp"]
                        tipo = result["tipo"]
                        
                        if timestamp not in self.pending_results:
                            self.pending_results[timestamp] = {}
                            
                        self.pending_results[timestamp][tipo] = {
                            "media": result["media"],
                            "desv": result["desv"],
                            "original_data": result.get("original_data")  # Preservar datos originales
                        }
                        
                        # Verificar si tenemos los 3 resultados para este timestamp
                        if len(self.pending_results[timestamp]) == 3:
                            # Crear bloque
                            block = self.create_block(timestamp, self.pending_results[timestamp])
                            self.blockchain.append(block)
                            blocks_created += 1
                            
                            # Mostrar información del bloque
                            alert_flag = "🚨 ALERTA" if block["alerta"] else "✅ Normal"
                            print(f"🔗 Bloque {blocks_created:2d}: {block['hash'][:16]}... {alert_flag}")
                            
                            # Persistir blockchain
                            self.save_blockchain()
                            
                            # Limpiar resultados procesados
                            del self.pending_results[timestamp]
                            
                    except Exception as e:
                        print(f"⚠️  Timeout o error recibiendo resultado: {e}")
                        continue
                        
        except Exception as e:
            print(f"❌ Error en verificador: {e}")
        finally:
            print(f"✅ Verificador finalizado. {blocks_created} bloques creados.")


def main():
    """Función principal que coordina todo el sistema."""
    print("🏥 Sistema de Análisis Biométrico con Blockchain")
    print("=" * 50)
    
    # Crear pipes para comunicación Principal -> Analizadores
    pipes = []
    pipe_connections = []
    
    for i in range(3):
        parent_conn, child_conn = mp.Pipe()
        pipes.append(parent_conn)
        pipe_connections.append(child_conn)
    
    # Crear queues para comunicación Analizadores -> Verificador
    result_queues = [mp.Queue() for _ in range(3)]
    
    # Crear analizadores
    analyzers = [
        BiometricAnalyzer("frecuencia"),
        BiometricAnalyzer("presion"),
        BiometricAnalyzer("oxigeno")
    ]
    
    # Crear procesos
    generator = BiometricGenerator()
    verifier = BlockchainVerifier()
    
    processes = []
    
    try:
        # Iniciar proceso verificador
        verifier_process = mp.Process(
            target=verifier.run, 
            args=(result_queues,)
        )
        verifier_process.start()
        processes.append(verifier_process)
        
        # Iniciar procesos analizadores
        for i, analyzer in enumerate(analyzers):
            analyzer_process = mp.Process(
                target=analyzer.run,
                args=(pipe_connections[i], result_queues[i])
            )
            analyzer_process.start()
            processes.append(analyzer_process)
        
        # Ejecutar generador en proceso principal
        generator.run(pipes)
        
        # Esperar que terminen todos los procesos
        for process in processes:
            process.join()
            
        print("\n🎉 Sistema completado exitosamente!")
        print("📄 Archivos generados:")
        print("  - blockchain.json")
        print("\n💡 Ejecuta 'python verificar_cadena.py' para verificar integridad")
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrupción del usuario")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
    finally:
        # Cleanup
        for pipe_conn in pipe_connections:
            if not pipe_conn.closed:
                pipe_conn.close()
        
        for queue in result_queues:
            queue.close()
            
        # Terminar procesos si están vivos
        for process in processes:
            if process.is_alive():
                process.terminate()
                process.join()


if __name__ == "__main__":
    main()
