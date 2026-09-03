# 🧠 Optimización e Inteligencia Artificial - 3011103

[![Python Version](https://img.shields.io/badge/python-3.14%2B-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linter: Flake8 & SonarQube](https://img.shields.io/badge/linter-flake8_|_sonarqube-brightgreen.svg)](https://flake8.pycqa.org/)
[![Data Versioning: DVC](https://img.shields.io/badge/data-DVC-orange.svg)](https://dvc.org/)

## 📖 Descripción del Proyecto

Este repositorio establece la estructura estándar y las mejores prácticas para los proyectos,
prácticas y talleres del curso **Optimización e Inteligencia Artificial** del Departamento de
Ciencias de la Computación y la Decisión de la **Universidad Nacional de Colombia, Sede Medellín**.

El propósito de este repositorio es facilitar la implementación, experimentación y evaluación de
métodos de optimización clásica y metaheurística. Abarca desde algoritmos basados en gradiente
(gradiente descendente estocástico, Newton, QuasiNewton) hasta enfoques metaheurísticos (Algoritmos
Genéticos, PSO, Colonia de Hormigas). Estos métodos se aplican directamente a la sintonización de
hiperparámetros en modelos de Machine Learning, incluyendo Random Forest, Redes Neuronales, Deep
Learning y enfoques no supervisados.

---

## 📂 Estructura de Directorios

Para mantener un ciclo de vida analítico organizado, reproducible y listo para integrarse en
pipelines de datos, se recomienda la siguiente jerarquía de archivos:

```text
├── config/              # Parámetros del proyecto (rutas, hiperparámetros, credenciales de ejemplo).
├── data/
│   ├── raw/             # Datos originales e inmutables.
│   ├── interim/         # Datos en transformación, resultados parciales de limpieza.
│   ├── processed/       # Datos limpios y listos para modelado.
│   └── external/        # Datos de terceros o fuentes externas.
├── docs/                # Documentación del proyecto (Sphinx/MkDocs), guías y referencias.
├── models/              # Modelos entrenados y serializados (ej. .pkl, .h5).
│   ├── trained/         # Modelos finales listos para inferencia.
│   ├── checkpoints/     # Puntos de guardado durante entrenamiento.
├── notebooks/           # Jupyter Notebooks para exploración y visualización (nombrados secuencialmente).
├── src/                 # Código fuente principal del proyecto.
│   ├── __init__.py
│   ├── data/            # Scripts para ingesta y transformación de datos.
│   ├── features/        # Scripts de feature engineering.
│   ├── models/          # Scripts para entrenamiento, optimización y predicción.
│   └── visualization/   # Generación de gráficos y pósteres digitales.
├── tests/               # Pruebas unitarias y de integración.
├── dashboards/          # Aplicaciones interactivas.
├── reports/             # Resultados y comunicación.
│   ├── figures/         # imágenes generadas por scripts/notebooks (versionadas o regenerables).
├── scripts/             # Automatización.
├── .gitignore           # Archivos ignorados por Git.
├── dvc.yaml             # Pipeline de versionado de datos y modelos.
├── environment.yml      # Dependencias para Conda.
├── requirements.txt     # Dependencias para pip.
└── README.md            # Este archivo.
```

---

## ⚙️ Requisitos y Dependencias

Para las sesiones prácticas y el desarrollo general, se recomienda el uso de **Anaconda** para la
gestión de entornos virtuales o **Google Colab** para la ejecución en la nube.

El proyecto gestiona sus dependencias de la siguiente forma:

| Herramienta | Archivo            | Propósito principal                                                                              |
| :---------- | :----------------- | :----------------------------------------------------------------------------------------------- |
| **Conda**   | `environment.yml`  | Ideal para resolver dependencias complejas en ciencia de datos (ej. librerías con binarios C++). |
| **Pip**     | `requirements.txt` | Instalación estándar de paquetes de Python en contenedores o entornos ligeros.                   |

**Librerías principales requeridas:**

- `numpy`, `pandas`, `scipy` (Manipulación matemática y de datos).
- `scikit-learn`, `tensorflow` / `pytorch` (Implementación de Random Forest y Redes Neuronales).
- `matplotlib`, `seaborn` (Visualización de convergencia).

---

## 🚀 Instalación y Configuración

Sigue estos pasos para replicar el entorno de desarrollo de manera consistente. Es imperativo tener
el entorno debidamente configurado antes de iniciar las ejecuciones prácticas.

**1. Clonar el repositorio:**

```bash
git clone https://github.com/KevinHidalgoDS/optimizacion-ia.git
cd optimizacion-ia
```

**2. Crear y activar el entorno virtual (Recomendado: Anaconda):**

```bash
conda env create -f environment.yml
conda activate optia_env
```

**3. (Alternativa) Instalación vía pip:**

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 💻 Uso y Ejecución

El código está modularizado para separar las pruebas interactivas de la ejecución en lotes.

- **Exploración:** Utiliza la carpeta `notebooks/` para experimentación inicial o al ejecutar
  prácticas sincrónicas en **Google Colab**.
- **Entrenamiento:** Para correr optimizaciones completas y simulaciones robustas (como
  simulaciones de Monte Carlo o búsquedas exhaustivas en grilla), ejecuta los módulos directamente
  desde la terminal:

```bash
# Ejemplo: Optimización de Random Forest (Práctica 1)
python src/models/train_rf_optimization.py --method grid_search

# Ejemplo: Optimización de Redes Neuronales (Práctica 2)
python src/models/train_nn_optimization.py --method gradient_descent
```

---

## 📏 Estándares de Código

La legibilidad y el "clean-code" son fundamentales, especialmente al realizar tareas de refactoring
algorítmico o al orquestar modelos analíticos para entornos productivos.

1. **Estilo base:** Todo el código en Python debe seguir el estándar **PEP 8**.
2. **Formateadores:** Se debe utilizar **Black** (longitud de línea de 88 caracteres) para unificar
   el estilo de forma automática.
3. **Linters:** Se emplea **Flake8** para identificar violaciones de estilo. En integraciones más
   avanzadas y despliegues, es altamente recomendado integrar **SonarQube** en el flujo local para
   detectar vulnerabilidades, asegurar una correcta parametrización del linter y evitar errores de
   _backtracking_ al optimizar expresiones regulares complejas dentro de funciones de parseo.
4. **Docstrings:** Documentar clases y funciones utilizando el formato de _NumPy_ o _Google_.

**Ejemplo de formato de función:**

```python
def optimize_hyperparameters(model, param_grid: dict) -> dict:
    """
    Optimiza los hiperparámetros del modelo usando búsqueda en grilla.

    Args:
        model: Estimador base de machine learning.
        param_grid (dict): Diccionario con los parámetros a evaluar.

    Returns:
        dict: Mejores hiperparámetros encontrados.
    """
    pass
```

---

## 📦 Versionado de Datos y Modelos

Nunca incluyas datasets grandes (`.csv`, `.parquet`) ni artefactos de modelos (`.h5`, `.pkl`)
directamente en Git.

- **DVC (Data Version Control):** Utiliza DVC para rastrear cambios en los datos. Los archivos
  `.dvc` se añaden a Git, mientras que los datos reales se almacenan en un _remote storage_ (como
  un blob storage de nube empresarial, ej. Azure Blob Storage administrado con identidades locales
  para desarrollo).
- **Git LFS (Large File Storage):** Alternativa para versionar binarios grandes directamente
  vinculados al repositorio.

---

## 🧪 Testing y Validación

La validación es crítica para asegurar que las funciones matemáticas (ej. derivadas del gradiente)
converjan correctamente.

- Estructura las pruebas dentro de la carpeta `tests/`.
- Utiliza **Pytest** para la ejecución de pruebas unitarias.

```bash
# Ejecutar todas las pruebas
pytest tests/
```

---

## 📚 Documentación

- Mantén el `README.md` actualizado frente a nuevos requerimientos del proyecto.
- Para el **Proyecto de Clase**, la entrega requiere documentar la implementación en Python,
  generar un póster digital y preparar una presentación final. [cite: 1] Los recursos visuales para
  esto deben almacenarse en la carpeta `docs/` o `src/visualization/`.
- Comenta de manera justificada las decisiones complejas en el código (ej. por qué se eligió un
  hiperparámetro o se modificó el "learning rate" en un método quasi-Newton).

---

## 🤝 Contribuciones

Para mantener la integridad del código al trabajar en equipo:

1. Crea una rama para tu feature: `git checkout -b feature/algoritmo-genetico`
2. Realiza commits descriptivos y atómicos.
3. Asegúrate de que el código pase el linter localmente antes de subir los cambios
   (`black . && flake8 .`).
4. Abre un Pull Request (PR) y solicita revisión de al menos un compañero antes del merge.

---

## 📄 Licencia y Atribuciones

Este material está estructurado para fines académicos de la **Universidad Nacional de Colombia,
Sede Medellín**.

**Licencia sugerida para el código:** MIT License (permite uso, modificación y distribución). Por
favor, asegúrate de referenciar adecuadamente la literatura o los fragmentos de código reutilizados
en tus módulos u optimizadores.

[//]: # (## Convertir jupyter a otros formatos)

[//]: # ()
[//]: # (una buena opción es tener instalado el paquete rise)

[//]: # ()
[//]: # (```PowerShell)

[//]: # (jupyter nbconvert --to FORMAT notebook.ipynb)

[//]: # (```)

[//]: # (otra opción es:)

[//]: # ()
[//]: # (```PowerShell)

[//]: # (jupyter nbconvert notebook.ipynb --to slides --post serve --SlidesExporter.reveal_theme=serif --SlidesExporter.reveal_scroll=True --SlidesExporter.reveal_transition=none)

[//]: # (jupyter nbconvert D:\SimulAva\notebooks\SimulacionMC.ipynb --to slides --post serve --SlideExporter.reveal_theme=serif --SlidesExporter.reveal_scroll=True --SlidesExporter.reveal_transition=none)

[//]: # (jupyter nbconvert --to html D:\SimulAva\notebooks\SimulacionMC.ipynb)

[//]: # (jupyter nbconvert --to pdf D:\SimulAva\notebooks\SimulacionMC.ipynb)

[//]: # (```)

[//]: # ()
[//]: # (Más info [nbconvert documentation]&#40;https://nbconvert.readthedocs.io/en/latest/usage.html&#41;)

[//]: # ()
[//]: # (## PowerShell)

[//]: # ()
[//]: # (Para revisar tamaño de los archivos)

[//]: # ()
[//]: # (```PowerShell)

[//]: # (Get-ChildItem -path "D:\Proyectos\Diplomado_UdeM\datasets\*" | Foreach {)

[//]: # (> $Files = Get-ChildItem $_.FullName -Recurse -File)

[//]: # (> $Size = '{0:N2}' -f &#40;&#40; $Files | Measure-Object -Property Length -Sum&#41;.Sum /1MB&#41;)

[//]: # (> [PSCustomObject]@{Profile = $_.FullName ; TotalObjects = "$&#40;$Files.Count&#41;" ; SizeMB = $Size})

[//]: # (> } | Export-CSV "D:\Proyectos\Diplomado_UdeM\folder_size_1.csv" -NoTypeInformation)

[//]: # (```)

[//]: # ()
[//]: # (## Git)

[//]: # ()
[//]: # (Identifica los archivos grandes: Puedes utilizar el siguiente comando para listar los archivos grandes en tu historial de Git:)

[//]: # ()
[//]: # (```bash)

[//]: # (git rev-list --objects --all | grep $&#40;git verify-pack -v .git/objects/pack/pack-*.idx | sort -k 3 -n | tail -10 | awk '{print$1}'&#41;)

[//]: # (```)

[//]: # ()
[//]: # (Este comando te mostrará los archivos más grandes en el historial de tu repositorio.)

[//]: # ()
[//]: # (Reduce el tamaño de los archivos: Si puedes, intenta comprimir o reducir el tamaño de los archivos problemáticos. Por ejemplo, si se trata de imágenes, videos o archivos de datos, podrías comprimirlos o reducir su resolución.)

[//]: # ()
[//]: # (Elimina los archivos grandes del historial de Git &#40;si es necesario&#41;: Si necesitas eliminar los archivos grandes del historial &#40;ya que seguirán existiendo en commits anteriores&#41;, puedes usar la herramienta BFG Repo-Cleaner o git filter-repo para limpiar el historial.)

[//]: # ()
[//]: # (Usando BFG Repo-Cleaner:)

[//]: # ()
[//]: # (```bash)

[//]: # (bfg --delete-files archivo_grande)

[//]: # (git reflog expire --expire=now --all && git gc --prune=now --aggressive)

[//]: # (```)

[//]: # ()
[//]: # (Añade nuevamente los archivos &#40;si redujiste el tamaño&#41;: Después de comprimir o reducir el tamaño de los archivos, vuelve a añadirlos con: bash Copiar código)

[//]: # ()
[//]: # (```bash)

[//]: # (git add archivo_comprimido)

[//]: # (git commit -m "Archivo reducido")

[//]: # (git push origin rama)

[//]: # (```)

[//]: # ()
[//]: # (Opción 2: Usar Git LFS &#40;Large File Storage&#41;)

[//]: # (Git LFS es una extensión de Git que te permite manejar archivos grandes sin afectar el rendimiento del repositorio. Con Git LFS, los archivos grandes no se almacenan directamente en Git, sino que se sustituyen por referencias, mientras los archivos reales se almacenan en un servidor separado.)

[//]: # ()
[//]: # (Instala Git LFS: Si no lo tienes instalado, puedes instalarlo según tu sistema operativo:)

[//]: # ()
[//]: # (Linux: bash Copiar código)

[//]: # ()
[//]: # (```bash)

[//]: # (sudo apt-get install git-lfs)

[//]: # (```)

[//]: # ()
[//]: # (Mac: bash Copiar código)

[//]: # ()
[//]: # (```bash)

[//]: # (brew install git-lfs)

[//]: # (```)

[//]: # ()
[//]: # (Windows: Descárgalo desde: git-lfs.github.com)

[//]: # (Inicializa Git LFS en tu repositorio: Después de instalar Git LFS, debes inicializarlo en el repositorio:)

[//]: # ()
[//]: # (```bash)

[//]: # (git lfs install)

[//]: # (```)

[//]: # ()
[//]: # (Rastrear los archivos grandes con LFS: Debes especificar los tipos de archivos que deseas rastrear con Git LFS. Por ejemplo, si los archivos grandes son imágenes PNG, puedes usar el siguiente comando:)

[//]: # ()
[//]: # (```bash)

[//]: # (git lfs track "*.png")

[//]: # (```)

[//]: # ()
[//]: # (También puedes rastrear archivos específicos de gran tamaño con:)

[//]: # ()
[//]: # (```bash)

[//]: # (git lfs track "archivo_grande")

[//]: # (```)

[//]: # ()
[//]: # (Añade y commitea los archivos grandes: Después de configurar LFS, añade y commitea los archivos rastreados:)

[//]: # ()
[//]: # (```bash)

[//]: # (git add .gitattributes archivo_grande)

[//]: # (git commit -m "Añadir archivo grande con LFS")

[//]: # (```)

[//]: # ()
[//]: # (Push al repositorio: Finalmente, empuja los cambios al repositorio:)

[//]: # ()
[//]: # (```bash)

[//]: # (git push origin rama)

[//]: # (```)

[//]: # ()
[//]: # (Git LFS subirá los archivos grandes al almacenamiento de Git LFS mientras que Git seguirá manejando el resto de los archivos como de costumbre.)

[//]: # ()
[//]: # (## The Boston Housing Dataset)

[//]: # ()
[//]: # ([bosto]&#40;https://lib.stat.cmu.edu/datasets/boston&#41;)

[//]: # ([The Boston Housing Dataset]&#40;https://www.kaggle.com/code/prasadperera/the-boston-housing-dataset&#41;)

[//]: # ()
[//]: # ()
[//]: # (## Python Plotly Express Tutorial: Unlock Beautiful Visualizations)

[//]: # ()
[//]: # ([Python Plotly Express Tutorial: Unlock Beautiful Visualizations]&#40;https://www.datacamp.com/tutorial/python-plotly-express-tutorial&#41;)

[//]: # ()
[//]: # (## UCI Machine Learning Repository)

[//]: # ()
[//]: # ([UCI Machine Learning Repository]&#40;https://archive.ics.uci.edu/datasets?Task=Regression&skip=0&take=10&sort=desc&orderBy=NumHits&search=ridge&#41;)

[//]: # ()
[//]: # (## Seaborn data)

[//]: # ()
[//]: # ([seaborn-data]&#40;https://github.com/mwaskom/seaborn-data&#41;)

[//]: # ([load_dataset]&#40;https://seaborn.pydata.org/generated/seaborn.load_dataset.html&#41;)

[//]: # (tree /A /F > "estructura_$&#40;Get-Date -Format yyyyMMdd_HHmm&#41;.txt")
