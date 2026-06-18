# NodeExporter for Blender

[![Blender Version](https://img.shields.io/badge/Blender-3.6%20%7C%204.x%20%7C%205.x-orange.svg)](https://www.blender.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

NodeExporter es un complemento (add-on) para Blender diseñado para extraer redes de nodos (Geometry Nodes y Shader Materials) y compilarlas en un visor web interactivo e independiente basado en HTML5, CSS3 y JavaScript

El propósito de esta herramienta es facilitar la visualización, documentación y exportación gráfica de sistemas de nodos complejos fuera del entorno de Blender, manteniendo una alta fidelidad visual y operativa.

## Características Principales

* **Visor Web Independiente:** Genera un archivo HTML autónomo que no requiere de servidores locales ni dependencias externas para su ejecución.
* **Exportación de Imágenes en Alta Resolución:** Permite la exportación del lienzo web a formato PNG (escala 2x), con soporte para fondos sólidos o canal alfa (transparencia) para su integración en software de composición gráfica y edición.
* **Interfaz y Lienzo Dinámico:** Implementa un entorno de trabajo infinito y redimensionable, con una interfaz superpuesta que permite la personalización en tiempo real del fondo, la densidad de la cuadrícula y el trazado de las conexiones (grosor y estilo de línea).
* **Sincronización de Estados Nativos:** Detecta y reproduce el estado de los elementos provenientes de Blender, soportando nodos minimizados (colapsados) y el ocultamiento de puertos individuales, reajustando la topología de los enlaces automáticamente.
* **Operaciones Interactivas:** Permite la modificación de la red directamente en el navegador, incluyendo el reposicionamiento de bloques, desconexión de enlaces y gestión de marcos (Frames) a través de un menú contextual.

## Instalación

1. Descargue el archivo `NodeExporter.zip` desde la sección de **Releases** de este repositorio.
2. En Blender, diríjase a **Edit > Preferences > Add-ons**.
3. Haga clic en **Install...**, seleccione el archivo `NodeExporter.zip` descargado y confirme.
4. Active la casilla correspondiente a **NodeExporter** en la lista de complementos.
5. El panel de control estará disponible en la barra lateral (tecla `N`) del editor de nodos.

## Instrucciones de Uso

1. Abra un espacio de trabajo en Blender que contenga un árbol de Geometry Nodes o un Material activo.
2. Despliegue la barra lateral en el Node Editor y ubique la pestaña **NodeExporter**.
3. Presione el botón **Usar Nodo en Pantalla** para establecer el árbol de nodos activo como objetivo de exportación.
4. Seleccione el directorio de destino en su sistema local.
5. Presione **Exportar y Abrir Visor**. El sistema generará el archivo JSON de datos, compilará el archivo HTML y lo ejecutará en su navegador web predeterminado.

## Arquitectura del Proyecto

El complemento está estructurado en dos componentes principales:

```text
NodeExporter/
├── __init__.py    # Lógica backend: Extracción mediante la API de Blender y formateo de datos a JSON.
└── visor.html     # Motor frontend: Renderizado DOM, cálculos de lienzo y UI interactiva.
