# TPO2 - Testing de Aplicaciones

Calculadora simple en Python con tests automatizados (pytest) e integración continua mediante GitHub Actions.

**Materia:** Testing de Aplicaciones — UADE
**Alumno:** Martín Benítez Potochek (Legajo 1195640)
**Docente:** Laime Huanca Abel Israel

## Estructura

```
app/                    Lógica de la calculadora
tests/                  Tests automatizados (pytest)
.github/workflows/      Pipeline de CI/CD
main.py                 Demo por consola
requirements.txt        Dependencias
```

## Cómo correr los tests

```bash
pip install -r requirements.txt
pytest
```

## Pipeline

El workflow `.github/workflows/tests.yml` se dispara en cada push a `main` y ejecuta los tests automáticamente, generando un reporte HTML como artefacto.
