#!/usr/bin/env python3
"""
Script de Prueba del Agente de Escritura Científica Mejorado v2.0
Demuestra la generación de documentos académicos con referencias IEEE
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.scientific_writer_enhanced import (
    generate_experiment_briefing_enhanced,
    get_relevant_references,
    IEEE_REFERENCES
)
from datetime import datetime


def create_sample_results():
    """Crea resultados de ejemplo para pruebas"""
    return {
        "experiment_name": "Performance Evaluation of AODV and OLSR in High-Mobility MANETs",
        "timestamp": datetime.now().isoformat(),
        "configuration": {
            "protocols": ["AODV", "OLSR"],
            "nodes": 20,
            "area": "1000x1000m",
            "duration": "200s",
            "mobility": "RandomWaypoint",
            "speed": "5-15 m/s",
            "traffic": "CBR (4 pkt/s)",
            "packet_size": "512 bytes",
            "repetitions": 10,
            "seeds": list(range(12345, 12355)),
            "ns3_version": "3.36"
        },
        "metrics": {
            "AODV": {
                "pdr": {
                    "mean": 0.870,
                    "std": 0.050,
                    "ci": [0.850, 0.890],
                    "min": 0.790,
                    "max": 0.940
                },
                "delay": {
                    "mean": 45.2,
                    "std": 8.3,
                    "ci": [42.1, 48.3],
                    "min": 32.1,
                    "max": 61.5,
                    "unit": "ms"
                },
                "throughput": {
                    "mean": 2.3,
                    "std": 0.4,
                    "ci": [2.1, 2.5],
                    "min": 1.7,
                    "max": 2.9,
                    "unit": "Mbps"
                },
                "overhead": {
                    "mean": 0.150,
                    "std": 0.030,
                    "ci": [0.140, 0.160],
                    "min": 0.110,
                    "max": 0.210
                }
            },
            "OLSR": {
                "pdr": {
                    "mean": 0.910,
                    "std": 0.040,
                    "ci": [0.890, 0.930],
                    "min": 0.840,
                    "max": 0.970
                },
                "delay": {
                    "mean": 38.7,
                    "std": 6.2,
                    "ci": [36.2, 41.2],
                    "min": 28.3,
                    "max": 49.1,
                    "unit": "ms"
                },
                "throughput": {
                    "mean": 2.5,
                    "std": 0.3,
                    "ci": [2.3, 2.7],
                    "min": 2.0,
                    "max": 3.1,
                    "unit": "Mbps"
                },
                "overhead": {
                    "mean": 0.220,
                    "std": 0.040,
                    "ci": [0.200, 0.240],
                    "min": 0.160,
                    "max": 0.290
                }
            }
        },
        "statistical_analysis": {
            "pdr_comparison": {
                "test": "paired t-test",
                "p_value": 0.003,
                "significant": True,
                "effect_size": 0.046,
                "conclusion": "OLSR has significantly higher PDR than AODV"
            },
            "delay_comparison": {
                "test": "paired t-test",
                "p_value": 0.012,
                "significant": True,
                "effect_size": -0.144,
                "conclusion": "OLSR has significantly lower delay than AODV"
            },
            "throughput_comparison": {
                "test": "paired t-test",
                "p_value": 0.089,
                "significant": False,
                "effect_size": 0.087,
                "conclusion": "No significant difference in throughput"
            },
            "overhead_comparison": {
                "test": "paired t-test",
                "p_value": 0.001,
                "significant": True,
                "effect_size": 0.467,
                "conclusion": "OLSR has significantly higher overhead than AODV"
            }
        }
    }


def test_enhanced_briefing():
    """Prueba generación de briefing académico mejorado"""
    print("\n" + "="*80)
    print("🧪 TEST: Generación de Briefing Académico con Referencias IEEE")
    print("="*80)
    
    results = create_sample_results()
    
    print("\n📊 Datos del experimento:")
    print(f"  - Protocolos: {results['configuration']['protocols']}")
    print(f"  - Nodos: {results['configuration']['nodes']}")
    print(f"  - Repeticiones: {results['configuration']['repetitions']}")
    
    print("\n🔍 Detectando referencias relevantes...")
    refs = get_relevant_references("AODV OLSR PDR throughput statistical", results)
    print(f"  - Referencias detectadas: {len(refs)}")
    for i, ref in enumerate(refs[:5], 1):
        print(f"    [{i}] {ref[:80]}...")
    
    print("\n📝 Generando briefing académico...")
    state = {"experiment_results": results, "messages": []}
    
    try:
        document = generate_experiment_briefing_enhanced(results, state)
        
        print("\n✅ Briefing generado exitosamente!")
        print(f"📏 Longitud: {len(document)} caracteres")
        print(f"📄 Líneas: {document.count(chr(10))} líneas")
        
        # Contar referencias
        ref_count = document.count("[")
        print(f"📚 Referencias incluidas: ~{ref_count} citas")
        
        print("\n📄 Primeras 1000 caracteres del documento:")
        print("-" * 80)
        print(document[:1000])
        print("...")
        print("-" * 80)
        
        # Verificar calidad académica
        print("\n🎓 Verificación de Calidad Académica:")
        checks = {
            "Referencias IEEE": "[" in document and "]" in document,
            "Intervalos de confianza": "CI:" in document or "confidence" in document.lower(),
            "Significancia estadística": "p <" in document or "p =" in document or "significant" in document.lower(),
            "Tercera persona": "we" not in document.lower()[:500],
            "Formato IEEE": "Fig." in document or "Table" in document or "TABLE" in document,
        }
        
        for check, passed in checks.items():
            status = "✅" if passed else "⚠️"
            print(f"  {status} {check}")
        
        # Guardar documento
        output_dir = Path("generated_documents/enhanced")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"briefing_enhanced_{timestamp}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(document)
        
        print(f"\n💾 Documento guardado en: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_ieee_references():
    """Muestra la base de datos de referencias IEEE"""
    print("\n" + "="*80)
    print("📚 BASE DE DATOS DE REFERENCIAS IEEE")
    print("="*80)
    
    print(f"\nTotal de referencias estándar: {len(IEEE_REFERENCES)}")
    print("\nReferencias disponibles:\n")
    
    for key, ref in IEEE_REFERENCES.items():
        print(f"🔖 {key.upper()}")
        print(f"   {ref}")
        print()


def compare_versions():
    """Compara versión original vs mejorada"""
    print("\n" + "="*80)
    print("📊 COMPARACIÓN: Versión Original vs Mejorada")
    print("="*80)
    
    print("\n🔴 VERSIÓN ORIGINAL (v1.0):")
    print("-" * 80)
    print("""
## Resultados

Los resultados muestran que OLSR tuvo mejor rendimiento que AODV.
El PDR fue de 91% para OLSR y 87% para AODV. El delay fue menor 
en OLSR (38.7 ms) comparado con AODV (45.2 ms).

El throughput fue similar en ambos protocolos (2.3-2.5 Mbps).
El overhead fue mayor en OLSR (22%) que en AODV (15%).
    """)
    
    print("\n🟢 VERSIÓN MEJORADA (v2.0):")
    print("-" * 80)
    print("""
## IV. EXPERIMENTAL RESULTS

### A. Packet Delivery Ratio Analysis

The experimental evaluation demonstrates that OLSR [2] achieves 
superior packet delivery performance compared to AODV [1]. 
Specifically, OLSR attained a mean PDR of 91.0% (95% CI: [89.0%, 93.0%]), 
representing a statistically significant improvement of 4.6% over 
AODV's 87.0% (95% CI: [85.0%, 89.0%]) (p = 0.003, paired t-test [13]).

This performance differential can be attributed to OLSR's proactive 
routing mechanism [2], which maintains continuously updated topology 
information through periodic HELLO and TC messages. In contrast, 
AODV's reactive approach [1] incurs route discovery delays during 
topology changes, particularly in high-mobility scenarios [10].

### B. End-to-End Delay Characteristics

Consistent with the PDR findings, OLSR [2] exhibited lower mean 
end-to-end delay (38.7 ± 6.2 ms) compared to AODV [1] (45.2 ± 8.3 ms), 
representing a 14.4% reduction. This improvement is statistically 
significant (p = 0.012) [13] and aligns with results reported in [7].
    """)
    
    print("\n📈 MEJORAS EVIDENTES:")
    improvements = [
        "✅ Referencias IEEE integradas [1], [2], [7], [10], [13]",
        "✅ Intervalos de confianza en todos los resultados",
        "✅ Significancia estadística reportada (p-values)",
        "✅ Explicación técnica de causas",
        "✅ Comparación con literatura",
        "✅ Estructura jerárquica clara (IV.A, IV.B)",
        "✅ Terminología técnica precisa",
        "✅ Argumentación lógica y respaldada"
    ]
    
    for improvement in improvements:
        print(f"  {improvement}")


def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "="*80)
    print("🖊️  PRUEBA DEL AGENTE DE ESCRITURA CIENTÍFICA MEJORADO v2.0")
    print("="*80)
    print("\nEste script demuestra las mejoras en:")
    print("  • Referencias IEEE automáticas")
    print("  • Estilo académico formal")
    print("  • Argumentación rigurosa")
    print("  • Cuantificación sistemática")
    print("="*80)
    
    # Mostrar referencias disponibles
    show_ieee_references()
    
    # Comparar versiones
    compare_versions()
    
    # Probar generación mejorada
    success = test_enhanced_briefing()
    
    # Resumen final
    print("\n" + "="*80)
    print("📊 RESUMEN")
    print("="*80)
    
    if success:
        print("\n✅ Prueba completada exitosamente!")
        print("\n📁 Revisa el documento generado en: generated_documents/enhanced/")
        print("\n📚 Documentación completa en: docs/MEJORAS-AGENTE-ESCRITURA.md")
        print("\n🎯 Próximo paso: Integrar con tus experimentos reales")
    else:
        print("\n❌ La prueba falló. Revisa los errores arriba.")
    
    print("="*80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
