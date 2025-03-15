# MemInfo3lite (Memory Information 3 Lite )

**Versión:** 20250314a 4.1.0c  
**Autor:** Axel O'BRIEN (LiGNUxMan) y ChatGPT  
**Basado en:** El script original mem_info.py pata Python2 de p@draigBrady.com.
**Licencia:** GPLv3  

## Descripción
`mem_info3_lite.py` es un script en Python para monitorear el uso de memoria en sistemas Linux. Permite visualizar el consumo de RAM de los procesos en ejecución, identificando la memoria privada y compartida utilizada por cada uno. También muestra información sobre la cantidad de procesos en distintos estados y el porcentaje de uso de RAM del sistema.

## Características
- Muestra el uso de memoria de cada proceso con detalles de memoria privada y compartida.
- Ordena los procesos de menor a mayor consumo de RAM.
- Proporciona información sobre el uso total de RAM en el sistema.
- Muestra estadísticas sobre la cantidad de procesos en distintos estados (running, sleeping, zombie, etc.).
- Ejecutable en modo único o con actualización periódica según un intervalo definido por el usuario.
- Soporte para detección de versiones del kernel y precisión en el cálculo de memoria compartida.
- Coloreado dinámico en la salida para destacar valores críticos.

## Requisitos
- Python 3
- Dependencias del sistema: `psutil`
- Acceso root para ejecutar el script.

## Instalación
1. Clonar el repositorio o descargar el archivo `mem_info3_lite.py`:
   ```bash
   Descarga el script mem_info3_lite.py.
   ```
2. Instalar la dependencia `psutil` si no está disponible:
   ```bash
   pip install psutil
   ```
3. Dar permisos de ejecución al script:
   ```bash
   chmod +x mem_info3_lite.py
   ```

## Uso
### Ejecución única
```bash
sudo ./mem_info3_lite.py
```
```bash
sudo python3 mem_info3_lite.py
```

### Ejecución periódica (cada X segundos)
```bash
sudo ./mem_info3_lite.py 5  # Refresca cada 5 segundos
```
```bash
sudo python3 mem_info3_lite.py 5 # Refresca cada 5 segundos
```

## Ejemplo de salida

![mem_info3_lite](https://github.com/user-attachments/assets/76bc6a6d-74a7-493e-a610-b8a6afdd4ae0)

```
 35.23 MiB +  36.09 MiB =  71.32 MiB	mintreport-tray (1)
 51.82 MiB +  34.58 MiB =  86.39 MiB	diodon (1)
 52.54 MiB +  34.86 MiB =  87.40 MiB	xapp-sn-watcher (1)
 58.36 MiB +  33.68 MiB =  92.04 MiB	blueman-applet (1)
 55.02 MiB +  39.35 MiB =  94.37 MiB	gnome-terminal- (1)
 26.67 MiB +  77.54 MiB = 104.21 MiB	evolution-sourc (1)
 20.23 MiB +  86.76 MiB = 106.99 MiB	evolution-alarm (1)
 69.58 MiB +  43.72 MiB = 113.30 MiB	nemo-desktop (1)
 65.80 MiB +  48.10 MiB = 113.90 MiB	guake (1)
 95.14 MiB +  63.21 MiB = 158.35 MiB	Xorg (1)
127.69 MiB +  36.85 MiB = 164.54 MiB	xdg-desktop-por (3)
112.50 MiB +  54.25 MiB = 166.76 MiB	mintUpdate (1)
119.75 MiB +  49.51 MiB = 169.26 MiB	xed (1)
259.28 MiB +  22.00 MiB = 281.28 MiB	dropbox (1)
245.32 MiB + 105.47 MiB = 350.80 MiB	cinnamon (1)
  3.32 GiB + 165.90 MiB =   3.48 GiB	chrome (31)
-----------------------------------------------------------
  5.08 GiB +   1.81 GiB =   6.89 GiB    TOTAL SYSTEM
-----------------------------------------------------------
Private    + Shared     = RAM used	Program
-----------------------------------------------------------
Processes: 273 (running=1, sleeping=205, idle=65, stopped=0, zombie=1, other=1)
RAM used: 37% (4.93GiB / 15.49GiB)
```

## Notas
- Se requiere acceso root para obtener información detallada de memoria compartida.
- La precisión en la detección de memoria compartida depende de la versión del kernel.

## Licencia
Este proyecto está licenciado bajo la **GPLv3**. Ver el archivo `LICENSE` para más detalles.

---
## Contribuciones
Cualquier mejora, corrección o sugerencia es bienvenida. ¡Suma tu aporte a este proyecto!
Si necesitas cambios o más detalles, dime y lo ajustamos.

