#!/usr/bin/env python3
"""
Script de Verificación de Integridad de Blockchain
Trabajo Práctico 1 - Computación II

Este script independiente:
1. Lee blockchain.json
2. Recalcula hashes y verifica encadenamiento
3. Informa bloques corruptos
4. Genera reporte estadístico completo

Autor: Benavidez Agustin
Fecha: 2025
"""

import json
import hashlib
import sys
from typing import Dict, List, Any, Tuple


class BlockchainVerifier:
    """Verificador de integridad de blockchain."""
    
    def __init__(self, blockchain_file: str = "blockchain.json"):
        self.blockchain_file = blockchain_file
        self.blockchain = []
        self.corrupted_blocks = []
        
    def load_blockchain(self) -> bool:
        """
        Carga la blockchain desde el archivo JSON.
        
        Returns:
            bool: True si se cargó correctamente
        """
        try:
            with open(self.blockchain_file, 'r') as f:
                self.blockchain = json.load(f)
            print(f"✅ Blockchain cargada: {len(self.blockchain)} bloques")
            return True
        except FileNotFoundError:
            print(f"❌ Error: No se encontró el archivo {self.blockchain_file}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Error: Archivo JSON corrupto - {e}")
            return False
        except Exception as e:
            print(f"❌ Error inesperado cargando blockchain: {e}")
            return False
    
    def calculate_hash(self, block: Dict[str, Any]) -> str:
        """
        Recalcula el hash de un bloque según la especificación.
        
        Args:
            block: Bloque a verificar
            
        Returns:
            str: Hash SHA-256 calculado
        """
        prev_hash = block.get("prev_hash", "")
        datos_str = str(block["datos"])
        timestamp = block["timestamp"]
        
        # Hash según especificación: sha256(prev_hash + str(datos) + timestamp)
        hash_input = prev_hash + datos_str + timestamp
        return hashlib.sha256(hash_input.encode()).hexdigest()
    
    def verify_block(self, index: int, block: Dict[str, Any], expected_prev_hash: str) -> Tuple[bool, List[str]]:
        """
        Verifica la integridad de un bloque individual.
        
        Args:
            index: Índice del bloque en la cadena
            block: Bloque a verificar
            expected_prev_hash: Hash esperado del bloque anterior
            
        Returns:
            tuple: (es_válido, lista_de_errores)
        """
        errors = []
        
        # Verificar estructura básica
        required_fields = ["timestamp", "datos", "alerta", "prev_hash", "hash"]
        for field in required_fields:
            if field not in block:
                errors.append(f"Campo requerido '{field}' faltante")
        
        if errors:
            return False, errors
        
        # Verificar encadenamiento
        if block["prev_hash"] != expected_prev_hash:
            errors.append(f"Prev_hash incorrecto. Esperado: {expected_prev_hash}, "
                         f"Encontrado: {block['prev_hash']}")
        
        # Verificar hash del bloque
        calculated_hash = self.calculate_hash(block)
        if block["hash"] != calculated_hash:
            errors.append(f"Hash incorrecto. Esperado: {calculated_hash}, "
                         f"Encontrado: {block['hash']}")
        
        # Verificar estructura de datos
        if "datos" in block:
            datos = block["datos"]
            required_data_fields = ["frecuencia", "presion", "oxigeno"]
            for field in required_data_fields:
                if field not in datos:
                    errors.append(f"Campo de datos '{field}' faltante")
                elif not isinstance(datos[field], dict):
                    errors.append(f"Campo de datos '{field}' debe ser un diccionario")
                else:
                    # Verificar subcampos
                    if "media" not in datos[field] or "desv" not in datos[field]:
                        errors.append(f"Subcampos 'media' o 'desv' faltantes en {field}")
        
        return len(errors) == 0, errors
    
    def verify_blockchain(self) -> bool:
        """
        Verifica la integridad completa de la blockchain.
        
        Returns:
            bool: True si toda la cadena es válida
        """
        if not self.blockchain:
            print("⚠️  Blockchain vacía")
            return False
        
        print("\n🔍 Verificando integridad de la blockchain...")
        print("=" * 50)
        
        is_valid = True
        expected_prev_hash = ""
        
        for i, block in enumerate(self.blockchain):
            block_valid, errors = self.verify_block(i, block, expected_prev_hash)
            
            if block_valid:
                print(f"✅ Bloque {i:2d}: {block['hash'][:16]}... - Válido")
                expected_prev_hash = block["hash"]
            else:
                print(f"❌ Bloque {i:2d}: {block.get('hash', 'N/A')[:16]}... - CORRUPTO")
                for error in errors:
                    print(f"    ❗ {error}")
                self.corrupted_blocks.append({
                    "index": i,
                    "hash": block.get("hash", "N/A"),
                    "errors": errors
                })
                is_valid = False
        
        print("=" * 50)
        
        if is_valid:
            print("🎉 ¡Blockchain íntegra! Todos los bloques son válidos.")
        else:
            print(f"⚠️  Blockchain corrupta. {len(self.corrupted_blocks)} bloque(s) con errores.")
        
        return is_valid
    
    def generate_statistics(self) -> Dict[str, Any]:
        """
        Genera estadísticas completas de la blockchain.
        
        Returns:
            dict: Estadísticas calculadas
        """
        if not self.blockchain:
            return {}
        
        total_blocks = len(self.blockchain)
        alert_blocks = sum(1 for block in self.blockchain if block.get("alerta", False))
        
        # Recopilar todos los valores para calcular promedios
        frecuencia_values = []
        presion_values = []
        oxigeno_values = []
        
        for block in self.blockchain:
            datos = block.get("datos", {})
            
            if "frecuencia" in datos and "media" in datos["frecuencia"]:
                frecuencia_values.append(datos["frecuencia"]["media"])
            
            if "presion" in datos and "media" in datos["presion"]:
                presion_values.append(datos["presion"]["media"])
            
            if "oxigeno" in datos and "media" in datos["oxigeno"]:
                oxigeno_values.append(datos["oxigeno"]["media"])
        
        # Calcular promedios
        avg_frecuencia = sum(frecuencia_values) / len(frecuencia_values) if frecuencia_values else 0
        avg_presion = sum(presion_values) / len(presion_values) if presion_values else 0
        avg_oxigeno = sum(oxigeno_values) / len(oxigeno_values) if oxigeno_values else 0
        
        return {
            "total_blocks": total_blocks,
            "alert_blocks": alert_blocks,
            "avg_frecuencia": round(avg_frecuencia, 2),
            "avg_presion": round(avg_presion, 2),
            "avg_oxigeno": round(avg_oxigeno, 2),
            "corrupted_blocks": len(self.corrupted_blocks),
            "integrity_percentage": round((total_blocks - len(self.corrupted_blocks)) / total_blocks * 100, 2) if total_blocks > 0 else 0
        }
    
    def generate_report(self, output_file: str = "reporte.txt"):
        """
        Genera el reporte final completo.
        
        Args:
            output_file: Archivo de salida del reporte
        """
        stats = self.generate_statistics()
        
        if not stats:
            print("❌ No se pueden generar estadísticas - blockchain vacía")
            return
        
        print(f"\n📊 Generando reporte estadístico...")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("REPORTE DE ANÁLISIS BIOMÉTRICO CON BLOCKCHAIN\n")
                f.write("=" * 50 + "\n\n")
                
                # Información general
                f.write("📈 ESTADÍSTICAS GENERALES\n")
                f.write("-" * 25 + "\n")
                f.write(f"Total de bloques procesados: {stats['total_blocks']}\n")
                f.write(f"Bloques con alertas médicas: {stats['alert_blocks']}\n")
                f.write(f"Porcentaje de alertas: {stats['alert_blocks']/stats['total_blocks']*100:.1f}%\n")
                f.write(f"Integridad de la cadena: {stats['integrity_percentage']}%\n\n")
                
                # Promedios biométricos
                f.write("🏥 PROMEDIOS BIOMÉTRICOS\n")
                f.write("-" * 25 + "\n")
                f.write(f"Frecuencia cardíaca promedio: {stats['avg_frecuencia']} bpm\n")
                f.write(f"Presión arterial promedio: {stats['avg_presion']} mmHg\n")
                f.write(f"Oxígeno en sangre promedio: {stats['avg_oxigeno']}%\n\n")
                
                # Información de integridad
                f.write("🔐 VERIFICACIÓN DE INTEGRIDAD\n")
                f.write("-" * 30 + "\n")
                if stats['corrupted_blocks'] == 0:
                    f.write("✅ Blockchain íntegra - Sin bloques corruptos\n")
                else:
                    f.write(f"⚠️  {stats['corrupted_blocks']} bloque(s) corrupto(s) detectado(s)\n")
                    f.write("\nDetalles de bloques corruptos:\n")
                    for corrupted in self.corrupted_blocks:
                        f.write(f"  - Bloque {corrupted['index']}: {corrupted['hash'][:16]}...\n")
                        for error in corrupted['errors']:
                            f.write(f"    * {error}\n")
                
                f.write(f"\nReporte generado: {self.get_current_timestamp()}\n")
                
            print(f"✅ Reporte guardado en: {output_file}")
            
        except Exception as e:
            print(f"❌ Error generando reporte: {e}")
    
    def get_current_timestamp(self) -> str:
        """Obtiene timestamp actual formateado."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def print_summary(self):
        """Imprime un resumen en consola."""
        stats = self.generate_statistics()
        
        if not stats:
            return
        
        print(f"\n📊 RESUMEN DE VERIFICACIÓN")
        print("=" * 30)
        print(f"📄 Total de bloques: {stats['total_blocks']}")
        print(f"🚨 Bloques con alertas: {stats['alert_blocks']}")
        print(f"💓 Frecuencia promedio: {stats['avg_frecuencia']} bpm")
        print(f"🩸 Presión promedio: {stats['avg_presion']} mmHg")
        print(f"🫁 Oxígeno promedio: {stats['avg_oxigeno']}%")
        print(f"🔐 Integridad: {stats['integrity_percentage']}%")


def main():
    """Función principal del verificador."""
    print("🔍 Verificador de Integridad de Blockchain")
    print("Trabajo Práctico 1 - Computación II")
    print("=" * 45)
    
    # Verificar argumentos
    blockchain_file = "blockchain.json"
    if len(sys.argv) > 1:
        blockchain_file = sys.argv[1]
    
    verifier = BlockchainVerifier(blockchain_file)
    
    # Cargar blockchain
    if not verifier.load_blockchain():
        sys.exit(1)
    
    # Verificar integridad
    is_valid = verifier.verify_blockchain()
    
    # Generar reporte
    verifier.generate_report()
    
    # Mostrar resumen
    verifier.print_summary()
    
    # Código de salida
    if is_valid:
        print("\n🎉 Verificación completada exitosamente")
        sys.exit(0)
    else:
        print(f"\n⚠️  Verificación completada con {len(verifier.corrupted_blocks)} error(es)")
        sys.exit(1)


if __name__ == "__main__":
    main()
