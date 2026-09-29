# 📚 Diccionario de Datos: Ames Housing Dataset

Este documento describe la estructura, significado, tipos de datos y posibles transformaciones de las variables contenidas en el conjunto de datos **Ames Housing** (`house_prices.csv`), basado en la especificación de `data/raw/data_description_updated.txt`.

---

## 📌 1. Descripción General del Dataset

- **Nombre del Dataset:** Ames Housing Dataset
- **Ubicación:** Ames, Iowa, EE. UU.
- **Registros / Observaciones:** 1,460 propiedades residenciales.
- **Variables / Atributos:** 20 columnas (1 Identificador, 1 Variable Objetivo y 18 Características predictoras).
- **Problema de Aprendizaje Automático:** Regresión supervisada.
- **Objetivo Principal:** Predecir el precio final de venta (`SalePrice`) de las propiedades a partir de sus atributos físicos, calidad constructiva, amenidades y dimensiones.

---

## 📊 2. Tabla Resumen de Variables

| Variable | Tipo de Dato | Rol | Unidad / Escala | Descripción Breve |
| :--- | :--- | :--- | :--- | :--- |
| **`Id`** | Numérico Discreto | Identificador | Entero secuencial | Identificador único para cada propiedad. |
| **`SalePrice`** | Numérico Continuo | **Variable Objetivo (Target)** | Dólares ($ USD) | Precio final de venta de la vivienda. |
| **`GrLivArea`** | Numérico Continuo | Característica | Pies cuadrados ($\text{ft}^2$) | Área habitable sobre el nivel del suelo. |
| **`YearBuilt`** | Numérico Discreto | Característica | Año (AAAA) | Año original de construcción de la vivienda. |
| **`YearRemodAdd`** | Numérico Discreto | Característica | Año (AAAA) | Año de la remodelación o adición más reciente. |
| **`1stFlrSF`** | Numérico Continuo | Característica | Pies cuadrados ($\text{ft}^2$) | Área total del primer piso. |
| **`2ndFlrSF`** | Numérico Continuo | Característica | Pies cuadrados ($\text{ft}^2$) | Área total del segundo piso. |
| **`NumFloors`** | Numérico Discreto | Característica | Número entero | Número de niveles/pisos de la vivienda. |
| **`HasBasement`** | Categórico Binario | Característica | `Yes` / `No` | Indica si la vivienda dispone de sótano. |
| **`TotalBsmtSF`** | Numérico Continuo | Característica | Pies cuadrados ($\text{ft}^2$) | Área total del sótano (terminada y sin terminar). |
| **`Garage`** | Categórico Binario | Característica | `Yes` / `No` | Indica si la vivienda cuenta con garaje. |
| **`GarageArea`** | Numérico Continuo | Característica | Pies cuadrados ($\text{ft}^2$) | Área total del garaje. |
| **`GarageCars`** | Numérico Discreto | Característica | Capacidad de autos | Capacidad de vehículos que caben en el garaje. |
| **`KitchenQual`** | Categórico Ordinal | Característica | Escala cualitativa (`Po` a `Ex`) | Calificación de la calidad de la cocina. |
| **`TotRmsAbvGrd`** | Numérico Discreto | Característica | Cantidad | Total de habitaciones sobre el nivel del suelo (sin baños). |
| **`BedroomAbvGr`** | Numérico Discreto | Característica | Cantidad | Número de dormitorios sobre el nivel del suelo. |
| **`TotalBathrooms`** | Numérico Continuo | Característica | Cantidad ponderada | Número total de baños (completos y medios, calculados). |
| **`OverallQual`** | Numérico Ordinal | Característica | Escala del 1 al 10 | Calidad global de materiales y acabados de la vivienda. |
| **`PoolQC`** | Categórico Ordinal | Característica | Escala cualitativa + `No Pool` | Calidad de la piscina (o indicación de ausencia). |
| **`Pool`** | Categórico Binario | Característica | `Yes` / `No` | Indica si la propiedad cuenta con piscina. |

---

## 🔍 3. Detalle de Variables

### 3.1. Identificador y Variable Objetivo

#### `Id`
- **Tipo:** Numérico discreto (entero).
- **Descripción:** Código único asignado a cada vivienda en el conjunto de datos.
- **Uso:** Excluir del entrenamiento de modelos predictivos para evitar sobreajuste o memorización espuria.

#### `SalePrice`
- **Tipo:** Numérico continuo (entero/flotante).
- **Descripción:** Precio de venta final de la vivienda en dólares estadounidenses ($ USD).
- **Rol:** Variable respuesta / target del problema de regresión.

---

### 3.2. Dimensiones y Superficies

#### `GrLivArea` (*Above grade ground living area*)
- **Tipo:** Numérico continuo.
- **Unidad:** Pies cuadrados ($\text{ft}^2$).
- **Descripción:** Superficie habitable por encima del nivel del suelo. Excluye sótano, garaje, terrazas y porches.

#### `1stFlrSF` (*First Floor square feet*)
- **Tipo:** Numérico continuo.
- **Unidad:** Pies cuadrados ($\text{ft}^2$).
- **Descripción:** Área total del primer piso de la casa.

#### `2ndFlrSF` (*Second Floor square feet*)
- **Tipo:** Numérico continuo.
- **Unidad:** Pies cuadrados ($\text{ft}^2$).
- **Descripción:** Área total del segundo piso de la casa (0 si es de una sola planta).

#### `TotalBsmtSF` (*Total square feet of basement area*)
- **Tipo:** Numérico continuo.
- **Unidad:** Pies cuadrados ($\text{ft}^2$).
- **Descripción:** Área total del sótano, sumando tanto áreas terminadas como sin terminar.

#### `GarageArea`
- **Tipo:** Numérico continuo.
- **Unidad:** Pies cuadrados ($\text{ft}^2$).
- **Descripción:** Superficie total cubierta del garaje (0 si no cuenta con garaje).

---

### 3.3. Aspectos Temporales y Estructurales

#### `YearBuilt`
- **Tipo:** Numérico discreto (año).
- **Descripción:** Año en que la vivienda fue originalmente construida.

#### `YearRemodAdd`
- **Tipo:** Numérico discreto (año).
- **Descripción:** Año de remodelación o ampliación más reciente de la propiedad. Si no ha tenido remodelaciones, su valor coincide con `YearBuilt`.

#### `NumFloors`
- **Tipo:** Numérico discreto.
- **Descripción:** Número de pisos o niveles de la estructura sobre el suelo.

---

### 3.4. Distribución de Espacios y Habitaciones

#### `TotRmsAbvGrd` (*Total rooms above grade*)
- **Tipo:** Numérico discreto.
- **Descripción:** Conteo total de habitaciones sobre el nivel del suelo. No incluye cuartos de baño.

#### `BedroomAbvGr` (*Bedrooms above grade*)
- **Tipo:** Numérico discreto.
- **Descripción:** Número total de dormitorios ubicados sobre el nivel del suelo.

#### `TotalBathrooms`
- **Tipo:** Numérico continuo / discreto fraccional (incrementos de 0.5).
- **Descripción:** Número consolidado de baños de la propiedad, derivado de baños completos y medios baños (tanto en sótano como sobre el nivel del suelo).
- **Fórmula de Cálculo:**
  $$\text{TotalBathrooms} = \text{FullBath} + (0.5 \times \text{HalfBath}) + \text{BsmtFullBath} + (0.5 \times \text{BsmtHalfBath})$$

---

### 3.5. Garaje, Sótano y Piscina

#### `HasBasement`
- **Tipo:** Categórico binario.
- **Valores posibles:**
  - `Yes`: La vivienda posee sótano.
  - `No`: La vivienda no posee sótano.

#### `Garage`
- **Tipo:** Categórico binario.
- **Valores posibles:**
  - `Yes`: La vivienda posee garaje.
  - `No`: La vivienda no posee garaje.

#### `GarageCars`
- **Tipo:** Numérico discreto.
- **Descripción:** Capacidad del garaje medida por la cantidad máxima de automóviles estándar que puede albergar.

#### `Pool`
- **Tipo:** Categórico binario.
- **Valores posibles:**
  - `Yes`: La propiedad dispone de piscina.
  - `No`: La propiedad no dispone de piscina.

---

### 3.6. Calidades y Acabados (Variables Ordinales)

#### `OverallQual` (*Overall Material and Finish Quality*)
- **Tipo:** Numérico ordinal.
- **Rango:** Enteros del 1 al 10.
- **Descripción:** Evaluación general de los materiales, mano de obra y acabados empleados en la vivienda.
  - `1`: Muy pobre / Pésimo (`Very Poor`)
  - `10`: Muy excelente / Excepcional (`Very Excellent`)

#### `KitchenQual` (*Kitchen Quality*)
- **Tipo:** Categórico ordinal.
- **Descripción:** Calidad de los acabados y equipamiento de la cocina.
- **Valores y equivalencias:**
  - `Ex`: Excelente (*Excellent*)
  - `Gd`: Buena (*Good*)
  - `TA`: Típica / Promedio (*Average/Typical*)
  - `Fa`: Regular (*Fair*)
  - `Po`: Mala / Pobre (*Poor*)

#### `PoolQC` (*Pool Quality*)
- **Tipo:** Categórico ordinal.
- **Descripción:** Nivel de calidad de la piscina (si aplica).
- **Valores y equivalencias:**
  - `Ex`: Excelente (*Excellent*)
  - `Gd`: Buena (*Good*)
  - `TA`: Típica / Promedio (*Average/Typical*)
  - `Fa`: Regular (*Fair*)
  - `No Pool`: Sin piscina

---

## 🛠️ 4. Guía de Transformación y Mapeos

### 4.1. Codificación Ordinal para `KitchenQual`
Para modelos que requieren variables numéricas (como regresión lineal, redes neuronales o SVM), se recomienda mapear la escala cualitativa a una escala numérica ordinal del 1 al 5:

```python
kitchen_quality_mapping = {
    "Ex": 5,  # Excellent
    "Gd": 4,  # Good
    "TA": 3,  # Typical / Average
    "Fa": 2,  # Fair
    "Po": 1,  # Poor
}

# Aplicar mapeo a la columna KitchenQual
df["KitchenQual"] = df["KitchenQual"].map(kitchen_quality_mapping)
```

### 4.2. Codificación Ordinal para `PoolQC`
De forma análoga, la calidad de la piscina puede traducirse a una escala donde la ausencia de piscina (`No Pool`) represente el valor base (0):

```python
pool_qc_mapping = {
    "No Pool": 0,
    "Fa": 1,  # Fair
    "TA": 2,  # Typical / Average
    "Gd": 3,  # Good
    "Ex": 4,  # Excellent
}

df["PoolQC"] = df["PoolQC"].map(pool_qc_mapping)
```

### 4.3. Variables Binarias (`HasBasement`, `Garage`, `Pool`)
Estas columnas categóricas pueden transformarse en valores binarios (`1` y `0`):

```python
binary_mapping = {"Yes": 1, "No": 0}

for col in ["HasBasement", "Garage", "Pool"]:
    if col in df.columns:
        df[col] = df[col].map(binary_mapping)
```
