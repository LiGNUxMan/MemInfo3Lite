#!/usr/bin/env python3

# Version 20250314ag 4.1.0c
#
# Autor: Axel O'BRIEN (LiGNUxMan) y ChatGPT
#
# Basado en el cript mem_info.py de P@draigBrady.com
#

### VER DEPENDENCIAS ###
import sys
import os
import psutil
# import socket
import time
# from datetime import timedelta
# from datetime import datetime

#### ROOT ####
# Verificar si el script tiene permisos de root
if os.geteuid() != 0:
    sys.stderr.write("Sorry, root permission required.\n")
    sys.exit(1)

#### INTERVAL ####
# 📌 Definir el intervalo de actualización (por defecto es None para ejecución única)
interval = None

# 📌 Si se pasa un argumento, usarlo como intervalo
if len(sys.argv) > 1:
    try:
        interval = int(sys.argv[1])  # Convertir argumento a entero
    except ValueError:
        print("Error: El parámetro debe ser un número natural (segundos).")
        sys.exit(1)

#### FONTS ####
#Letra normal, bold e italic
RESET = "\033[0m"
BOLD = "\033[1m"
# ITALIC = "\033[3m"
# Colores ANSI para terminal
# GREEN = "\033[92m" #
# ORANGE = "\033[38;5;208m" #
# ORANGE = "\033[38;5;214m" # naranja intenso
RED = "\033[31m" # RED = "\033[91m"
YELLOW = "\033[33m" # YELLOW = "\033[93m"

##############################
############ MAIN ############
##############################
def main_script():
    """ Ejecuta la lógica del script mostrando los valores. """

    # Tamaño de página en KiB
    PAGESIZE = os.sysconf("SC_PAGE_SIZE") / 1024 # KiB
    our_pid = os.getpid()  # PID del script actual

    # KERNEL
    # 📌 Obtener la versión del kernel
    def get_kernel_version():
        with open("/proc/sys/kernel/osrelease") as f:
            version = f.read().strip().split(".")[:3]
            version[2] = version[2].split("-")[0]  # Eliminar sufijos adicionales
            return tuple(map(int, version))

    kernel_version = get_kernel_version()

    #### RAM ####
    # 📌 Obtener información de la memoria RAM
    mem = psutil.virtual_memory()

    # 📌 Obtener la memoria total del sistema
    def get_total_system_memory():
        with open("/proc/meminfo") as meminfo:
            for line in meminfo:
                if line.startswith("MemTotal:"):
                    return int(line.split()[1])  # MemTotal está en KB
        return 0

    total_system_memory = get_total_system_memory()

    # 📌 Calcular porcentaje de RAM utilizada
    percent_used = (mem.used / total_system_memory) * 100

    # 📌 Obtener la memoria compartida de un proceso
    def get_shared_memory(pid):
        try:
            smaps_path = f"/proc/{pid}/smaps"
            if os.path.exists(smaps_path):
                with open(smaps_path) as smaps:
                    return sum(int(line.split()[1]) for line in smaps if "Shared" in line)
            elif (2, 6, 1) <= kernel_version <= (2, 6, 9):
                return 0  # No se puede determinar en este rango de kernels
            else:
                return int(open(f"/proc/{pid}/statm").readline().split()[2]) * PAGESIZE
        except:
            return 0  # Evitar errores si el proceso ya no existe

    # 📌 Obtener uso de memoria de procesos
    cmds, shareds, count = {}, {}, {}

    for line in os.popen("ps -e -o rss=,pid=,comm=").readlines():
        try:
            size, pid, cmd = map(str.strip, line.strip().split(None, 2))
            if int(pid) == our_pid:
                continue  # Omitir este script
            shared = get_shared_memory(pid)
            shareds[cmd] = max(shareds.get(cmd, 0), shared)
            cmds[cmd] = cmds.get(cmd, 0) + int(size) - shared
            count[cmd] = count.get(cmd, 0) + 1
        except:
            continue  # Evitar errores con procesos que desaparecen

    # Sumar la memoria compartida más alta de cada programa
    for cmd in cmds:
        cmds[cmd] += shareds[cmd]

    # Ordenar por consumo de RAM (de menor a mayor)
    sorted_processes = sorted(cmds.items(), key=lambda x: x[1])

    # Calcular totales de memoria
    total_private = sum(cmds[cmd] - shareds[cmd] for cmd in cmds)
    total_shared = sum(shareds.values())
    total_memory = total_private + total_shared

    #### PROCESSES ####
    # 📌 Obtener cantidad de procesos por estado
    states = {
        "running": 0,
        "sleeping": 0,
        "idle": 0,
        "stopped": 0,
        "zombie": 0,
        "other": 0
    }

    total_processes = 0

    for proc in psutil.process_iter(attrs=['pid', 'status']):
        total_processes += 1
        status = proc.info['status']
    
        if status == psutil.STATUS_RUNNING: #R - Running (Ejecutándose) 🏃
            states["running"] += 1
        elif status == psutil.STATUS_SLEEPING: #S - Sleeping (Durmiendo) 😴
            states["sleeping"] += 1
        elif status == psutil.STATUS_IDLE: #I - Idle (Inactivo) 🛑
            states["idle"] += 1
        elif status == psutil.STATUS_STOPPED: #T - Stopped (Detenido) ✋
            states["stopped"] += 1
        elif status == psutil.STATUS_ZOMBIE: #Z - Zombie ☠️
            states["zombie"] += 1
        else:
            states["other"] += 1 #Otros estados no contemplados

    # 📌 Evaluar precisión de la memoria compartida
    def shared_memory_accuracy():
        if kernel_version[:2] == (2, 4):
            if "Inact_" not in open("/proc/meminfo").read():
                return 1
            return 0
        elif kernel_version[:2] == (2, 6):
            if os.path.exists(f"/proc/{os.getpid()}/smaps"):
                return 1
            if (2, 6, 1) <= kernel_version <= (2, 6, 9):
                return -1
            return 0
        else:
            return 1

    # 📌 Función para convertir valores a unidades legibles (KiB, MiB, GiB, etc.)
    def human(num, power="Ki"):
        powers = ["Ki", "Mi", "Gi", "Ti"]
        while num >= 1024:
            num /= 1024.0
            power = powers[powers.index(power) + 1]
        return "%.2f %sB" % (num, power)

    # 📌 Función para aplicar color según umbral
    def apply_color(value, yellow_threshold, red_threshold, suffix=""):
        if value > red_threshold:
            return f"{RED}{value}{suffix}{RESET}"  # 🔴 Rojo
        elif value > yellow_threshold:
            return f"{YELLOW}{value}{suffix}{RESET}"  # 🟡 Amarillo
        else:
            return f"{value}{suffix}"  # Sin color

    # 📌 Aplicar colores a cada parámetro
    ram_usage = int(mem.percent)
    ram_usage_str = apply_color(ram_usage, 75, 90, "%")

    # 📌 Imprimir resultados
    print("-" * 59)
    print("Private    + Shared     = RAM used\tProgram")
    print("-" * 59)
    for cmd, size in sorted_processes:
        private_mem = cmds[cmd] - shareds[cmd]
        shared_mem = shareds[cmd]
        total_mem = cmds[cmd]
        print(f"{human(private_mem):>10} + {human(shared_mem):>10} = {human(total_mem):>10}\t{cmd} ({count[cmd]})")
    print("-" * 59)
    print(f"{BOLD}{human(total_private):>10}{RESET} + {BOLD}{human(total_shared):>10}{RESET} = {BOLD}{human(total_memory):>10}{RESET}    TOTAL SYSTEM")
    print("-" * 59)
    print("Private    + Shared     = RAM used\tProgram")
    print("-" * 59)
    print(f"Processes: {BOLD}{total_processes}{RESET} (running={BOLD}{states['running']}{RESET}, sleeping={BOLD}{states['sleeping']}{RESET}, idle={BOLD}{states['idle']}{RESET}, stopped={BOLD}{states['stopped']}{RESET}, zombie={BOLD}{states['zombie']}{RESET}, other={BOLD}{states['other']}{RESET})")
    print(f"RAM used: {BOLD}{ram_usage_str}{RESET} ({BOLD}{mem.used / (1024**3):.2f}GiB{RESET} / {BOLD}{mem.total / (1024**3):.2f}GiB){RESET}")

    # Mostrar advertencias sobre precisión de memoria compartida
    if shared_memory_accuracy() in [-1, 0]:
        sys.stderr.write("Warning: Shared memory is not reported by this system.\n")
        sys.stderr.write("Values reported will be too large.\n")

# 📌 Si NO hay parámetro → ejecutar una vez y salir
if interval is None:
    main_script()
else:
    # 📌 Si hay un parámetro → ejecutar en bucle cada X segundos
    count = 1  # Inicializa el contador
    while True:
        os.system('clear')
        main_script()  # 🔥 Aquí se ejecuta correctamente en cada iteración

        # Cuenta regresiva
        for i in range(interval, 0, -1):
            sys.stdout.write(f"\rRuns: {count} / Next run in {i}/{interval} seconds... ")
            sys.stdout.flush()
            time.sleep(1)

        count += 1  # Aumenta el contador en cada iteración



