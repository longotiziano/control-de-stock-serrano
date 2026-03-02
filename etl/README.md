# Validaciones
En este directorio se encuentran los archivos y módulos relacionados a la verificación de los datasets.\
Estás mismas están divididas en 2 secciones:

### En el Excel
- Que NO haya materias primas duplicadas en ninguna de las hojas, permitiendo el nombre de la materia prima utilizarse como PK

### En el programa
- Verificaciones de estructura del Excel
- Validaciones de datos más complejas que no se pueden incluir en el Excel

## config.json
Contiene la **configuración general del programa**:
- Columnas de los DataFrames requeridas para el análisis
- Bares que están DENTRO del Excel

## verificadores_datos.py
- Que los items del Excel de ventas coincidan con los de la hoja `Stock`
- Que las cantidades sean acordes (que lo consumido no exceda lo almacenado y cantidades negativas)

## verificadores_estructura.py
Verificaciones iniciales que no contienen datos, si no la estructura general del worksheet
- Si las columnas presentes coinciden con las del `config.json`
- Si las hojas en el worksheet son suficientes para el análisis