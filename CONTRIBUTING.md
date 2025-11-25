# Guía de Contribución al Sistema A2A

¡Gracias por tu interés en contribuir al Sistema A2A! Este documento establece las pautas para contribuir al proyecto.

## 🤝 Cómo Contribuir

### Reportar Bugs
Si encuentras un error, por favor abre un Issue en GitHub incluyendo:
- Pasos para reproducir el error.
- Comportamiento esperado vs real.
- Logs o capturas de pantalla relevantes.
- Entorno (OS, versión de Python, versión de NS-3).

### Sugerir Mejoras
Abre un Issue con la etiqueta `enhancement` describiendo tu idea y por qué sería útil.

### Pull Requests
1.  **Fork** el repositorio.
2.  Crea una rama para tu feature: `git checkout -b feature/mi-nueva-feature`.
3.  Implementa tus cambios siguiendo los estándares de código.
4.  Asegúrate de que los tests pasen: `python -m unittest discover tests`.
5.  Haz commit de tus cambios: `git commit -m 'feat: descripción breve'`.
6.  Haz push a tu rama: `git push origin feature/mi-nueva-feature`.
7.  Abre un Pull Request describiendo tus cambios.

---

## 💻 Estándares de Desarrollo

### Estilo de Código
- Seguimos **PEP 8** para Python.
- Usamos **Type Hints** en todas las funciones nuevas.
- Documentamos clases y funciones con **Docstrings** (formato Google).

```python
def mi_funcion(param: int) -> str:
    """
    Descripción breve.

    Args:
        param: Descripción del parámetro.

    Returns:
        Descripción del retorno.
    """
    pass
```

### Estructura del Proyecto
- `agents/`: Lógica de los agentes (LangGraph nodes).
- `config/`: Configuraciones globales.
- `utils/`: Utilidades compartidas (logging, errores, estado).
- `simulations/`: Directorio de trabajo para scripts y resultados.
- `tests/`: Tests unitarios e integración.

### Tests
Todo código nuevo debe incluir tests unitarios.
- Usamos `unittest`.
- Mocks para dependencias externas (NS-3, Ollama).
- Ejecutar tests antes de PR: `python -m unittest discover tests`.

---

## 🏗️ Arquitectura

El sistema utiliza una arquitectura de **Agentes Cognitivos** orquestados por **LangGraph**.
- **Estado Compartido (`AgentState`)**: Diccionario que pasa entre nodos.
- **Nodos**: Funciones puras que reciben estado y devuelven actualizaciones.
- **Memoria**: SQLite para persistencia de checkpoints.

---

## 📜 Licencia
Al contribuir, aceptas que tu código se licencie bajo la licencia MIT del proyecto.
