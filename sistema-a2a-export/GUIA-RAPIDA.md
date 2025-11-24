# 🚀 Guía Rápida - Sistema A2A

## Para Empezar en 5 Minutos

### 1. Instalación Automática

```bash
cd sistema-a2a-tesis
chmod +x scripts/install.sh
./scripts/install.sh
```

**Tiempo**: 60-90 minutos (automático)

### 2. Verificar Instalación

```bash
source venv/bin/activate
python scripts/check_system.py
```

**Resultado esperado**: Todas las marcas ✅

### 3. Primera Ejecución

```bash
python main.py --task "Simular protocolo AODV con 20 nodos"
```

**Tiempo**: 5-10 minutos

---

## 📋 Comandos Esenciales

### Uso Básico

```bash
# Activar entorno
source venv/bin/activate

# Ejecutar tarea
python main.py --task "Tu tarea aquí"

# Ver logs
tail -f logs/sistema_a2a.log

# Verificar sistema
python scripts/check_system.py
```

### Ejemplos de Tareas

```bash
# Comparación simple
python main.py --task "Comparar AODV y OLSR con 50 nodos"

# Análisis de escalabilidad
python main.py --task "Evaluar AODV con 25, 50, 100 nodos"

# Escenario VANET
python main.py --task "Simular VANET con 30 vehículos en área urbana"
```

---

## 📁 Estructura de Resultados

```
simulations/
├── results/          # Datos XML de NS-3
├── plots/            # Gráficos PNG
└── scripts/          # Código generado

logs/                 # Logs del sistema
```

---

## 🔧 Solución Rápida de Problemas

### Ollama no responde

```bash
pkill ollama
ollama serve &
sleep 5
curl http://localhost:11434/api/tags
```

### NS-3 no compila

```bash
cd ~/tesis-a2a/ns-allinone-3.43/ns-3.43
./ns3 clean
./ns3 configure --enable-python-bindings
./ns3 build
```

### Dependencias Python faltan

```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📚 Documentación Completa

- **[Instalación Detallada](docs/01-INSTALACION.md)** - Instalación paso a paso
- **[Configuración](docs/02-CONFIGURACION.md)** - Configurar el sistema
- **[Uso Básico](docs/03-USO-BASICO.md)** - Guía para el grupo
- **[Uso Avanzado](docs/04-USO-AVANZADO.md)** - Características avanzadas
- **[Troubleshooting](docs/05-TROUBLESHOOTING.md)** - Solución de problemas

---

## 🎯 Flujo de Trabajo Típico

1. **Activar entorno**: `source venv/bin/activate`
2. **Definir tarea clara**: "Comparar X y Y con Z nodos"
3. **Ejecutar**: `python main.py --task "..."`
4. **Monitorear**: `tail -f logs/sistema_a2a.log`
5. **Revisar resultados**: `ls simulations/plots/`
6. **Analizar métricas**: Ver gráficos y propuesta del agente

---

## ⏱️ Tiempos Estimados

| Actividad | Tiempo |
|-----------|--------|
| Instalación completa | 60-90 min |
| Tarea simple (20 nodos) | 5-10 min |
| Tarea compleja (100 nodos) | 15-20 min |
| Comparación de protocolos | 10-15 min |

---

## 💡 Tips Rápidos

1. **Empieza simple**: Prueba con 10-20 nodos primero
2. **Sé específico**: Define claramente qué quieres simular
3. **Revisa logs**: Siempre verifica que no haya errores
4. **Guarda resultados**: Copia archivos importantes a otra carpeta
5. **Documenta**: Anota qué hiciste y qué obtuviste

---

## 🆘 Ayuda Rápida

**¿Sistema no funciona?**
```bash
python scripts/check_system.py
```

**¿Simulación falla?**
```bash
grep "ERROR" logs/sistema_a2a.log
```

**¿Necesitas ayuda?**
- Consulta: `docs/05-TROUBLESHOOTING.md`
- Contacta al administrador del sistema

---

## 🎓 Para el Grupo de Investigación

### Roles

- **Investigadores**: Definen tareas y analizan resultados
- **Asistentes**: Ejecutan simulaciones y recopilan datos
- **Administrador**: Mantiene el sistema funcionando

### Mejores Prácticas

1. Una tarea a la vez (no ejecutar en paralelo)
2. Documentar cada experimento
3. Guardar resultados importantes
4. Reportar problemas al administrador
5. Compartir hallazgos con el grupo

---

## 📞 Contacto

**Administrador del Sistema**: [Tu Nombre]  
**Email**: [tu_email@universidad.edu]  
**Horario de Soporte**: [Lunes-Viernes 9:00-18:00]

---

**Versión**: 1.0.0  
**Última Actualización**: Noviembre 2025

---

## ✅ Checklist de Inicio

- [ ] Sistema instalado
- [ ] Verificación pasada (todas ✅)
- [ ] Entorno virtual activado
- [ ] Primera tarea ejecutada exitosamente
- [ ] Resultados revisados
- [ ] Documentación leída

**¿Todo listo?** ¡Comienza tu investigación! 🚀
