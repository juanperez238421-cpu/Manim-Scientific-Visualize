# Protocolo completo para validar, renderizar y entregar escenas ManimCE en calidad `-pqh`

**Versión:** 1.0  
**Fecha de consolidación:** 26 de julio de 2026  
**Entorno de referencia:** Manim Community Edition 0.20.1  
**Objetivo principal:** producir un archivo `.mp4` final en alta calidad, verificable y reproducible, a partir de una escena ManimCE.

---

## 1. Propósito

Este protocolo define el flujo técnico completo para:

1. Revisar un archivo ManimCE.
2. Identificar las escenas disponibles.
3. Validar sintaxis, rutas, assets y LaTeX.
4. Ejecutar una prueba rápida.
5. Renderizar la escena final con el indicador literal `-pqh`.
6. Verificar resolución, duración, códec y existencia del archivo.
7. Empaquetar el `.mp4`, el código fuente y las sumas de verificación.
8. Usar una ruta alternativa cuando Docker o Python local no estén disponibles.
9. Diagnosticar fallos comunes sin alterar innecesariamente la lógica de la animación.

El protocolo prioriza **Docker** por reproducibilidad. También incluye:

- instalación local con entorno virtual;
- ejecución en Google Colab;
- render remoto mediante GitHub Actions y la imagen oficial de ManimCE.

---

## 2. Criterio de aceptación

Un render se considera terminado correctamente solo si se cumplen todos los puntos siguientes:

- El archivo Python compila con `py_compile`.
- La clase solicitada existe y hereda de una clase válida de Manim.
- La escena termina sin traceback.
- Manim genera un archivo `.mp4` no vacío.
- El video puede ser leído por `ffprobe`.
- La resolución coincide con la solicitada.
- La velocidad de fotogramas coincide con la configuración.
- El códec es adecuado para entrega, preferiblemente H.264.
- El formato de píxel es compatible, preferiblemente `yuv420p`.
- El contenido visual no queda cortado, superpuesto ni fuera del marco.
- El código fuente exacto usado para renderizar se conserva.
- Se registra el comando exacto de render.
- Se calcula una suma SHA-256 del producto final.

---

## 3. Significado de las opciones de calidad

### 3.1 `-pql`

```bash
manim -pql archivo.py NombreEscena
```

- `-p`: intenta abrir una vista previa al finalizar.
- `-q`: selecciona calidad.
- `l`: baja calidad.

Uso recomendado:

- validación rápida;
- revisión de sintaxis visual;
- detección de texto fuera del marco;
- prueba de rutas y assets;
- comprobación de animaciones y transiciones.

No debe usarse como entrega final.

---

### 3.2 `-pqm`

```bash
manim -pqm archivo.py NombreEscena
```

Calidad media. Es útil para una revisión visual más precisa antes del render final cuando la escena es larga.

---

### 3.3 `-pqh`

```bash
manim -pqh archivo.py NombreEscena
```

Alta calidad con intento de vista previa.

Para un proyecto horizontal estándar, normalmente produce:

- 1920 × 1080;
- 30 o 60 fps, según configuración;
- archivo MP4.

Esta es la opción final solicitada en este protocolo.

---

### 3.4 `-qh`

```bash
manim -qh archivo.py NombreEscena
```

Alta calidad sin abrir vista previa. Es más apropiada para:

- servidores;
- Docker;
- Colab;
- GitHub Actions;
- ejecución sin interfaz gráfica.

Cuando se requiere usar literalmente `-pqh` en un entorno sin interfaz, debe neutralizarse `xdg-open` sin modificar el render.

---

## 4. Tiempos operativos y umbrales de intervención

Los tiempos dependen de la CPU, cantidad de ecuaciones, imágenes, animaciones, resolución, caché y velocidad de descarga. Los valores siguientes son ventanas operativas de referencia, no garantías.

| Etapa | Tiempo habitual | No intervenir antes de | Revisar si supera |
|---|---:|---:|---:|
| Inspección del archivo Python | 1–5 min | 1 min | 10 min |
| `py_compile` | 1–10 s | 10 s | 1 min |
| Detección de escenas | 1–10 s | 10 s | 1 min |
| Descarga inicial de imagen Docker | 2–10 min | 5 min | 20 min |
| Render `-pql` de escena corta | 15 s–3 min | 2 min | 10 min |
| Render `-pql` de escena larga | 2–15 min | 10 min | 30 min |
| Render `-pqh` de escena corta | 1–10 min | 5 min | 30 min |
| Render `-pqh` de clase de 3–10 min | 5–45 min | 20 min | 90 min |
| Primera compilación LaTeX | 10–90 s adicionales | 60 s | 5 min |
| Cola de GitHub Actions | 0–5 min | 5 min | 15 min |
| Carga de artifact | 10 s–3 min | 2 min | 10 min |
| Verificación con `ffprobe` | 1–10 s | 10 s | 1 min |

### Regla para escenas largas

No cancelar un render solo porque la consola permanezca varios minutos en una animación compleja. Antes de detenerlo, comprobar:

- actividad de CPU;
- crecimiento de `media/`;
- nuevos archivos parciales;
- mensajes de progreso de Manim;
- ausencia de traceback.

### Frecuencia de seguimiento recomendada

- Render local corto: revisar cada 30–60 segundos.
- Render local largo: revisar cada 2–5 minutos.
- GitHub Actions: revisar cada 30–90 segundos.
- No consultar el estado cada pocos segundos, porque no aporta información útil.

---

## 5. Estructura recomendada del proyecto

```text
proyecto_manim/
│
├── main.py
├── assets/
│   ├── images/
│   ├── svg/
│   ├── audio/
│   ├── fonts/
│   └── data/
│
├── media/
├── delivery/
├── requirements.txt
├── manim.cfg
└── README_RENDER.md
```

### Reglas

- Usar rutas relativas.
- No depender de carpetas personales de Windows.
- Mantener los assets dentro del proyecto.
- Evitar nombres ambiguos como `final2.py`.
- Registrar el nombre exacto de la escena.

Ejemplo correcto:

```python
ImageMobject("assets/images/diagram.png")
```

Ejemplo no portable:

```python
ImageMobject(r"D:\Academica\Proyecto\diagram.png")
```

---

## 6. Revisión previa del código

### 6.1 Validar que el archivo existe

Linux/macOS:

```bash
ls -lh main.py
```

PowerShell:

```powershell
Get-Item .\main.py
```

---

### 6.2 Validar sintaxis Python

```bash
python -m py_compile main.py
```

Resultado esperado: el comando termina sin imprimir traceback.

Si aparece un error, corregirlo antes de instalar o iniciar Manim.

---

### 6.3 Identificar las escenas

Búsqueda rápida:

```bash
grep -nE '^class .*\((Scene|MovingCameraScene|ThreeDScene|ZoomedScene)' main.py
```

PowerShell:

```powershell
Select-String -Path .\main.py -Pattern '^class .*\((Scene|MovingCameraScene|ThreeDScene|ZoomedScene)'
```

También puede usarse:

```bash
manim main.py
```

Manim mostrará o solicitará las escenas disponibles si el archivo contiene varias.

---

### 6.4 Comprobar resolución y FPS

Buscar configuraciones como:

```python
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30
```

Configuración horizontal recomendada:

```python
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
```

Configuración vertical recomendada:

```python
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30
```

---

### 6.5 Detectar rutas absolutas

Linux/macOS:

```bash
grep -nE '([A-Za-z]:\\|/Users/|/home/[^/]+/Desktop|/mnt/)' main.py
```

Reemplazar las rutas de usuario por rutas relativas.

---

### 6.6 Revisar caracteres Unicode dentro de `Tex`

`Tex` usa LaTeX. Algunos caracteres Unicode pegados directamente pueden hacer fallar `pdfLaTeX`.

Ejemplo problemático:

```python
Tex("Calculate ΣFx and ΣFy")
```

Opciones correctas:

```python
Tex("Calculate sum Fx and sum Fy")
```

o:

```python
MathTex(r"\text{Calculate } \Sigma F_x \text{ and } \Sigma F_y")
```

Regla práctica:

- texto común: `Text`;
- texto con LaTeX: `Tex`;
- expresiones matemáticas: `MathTex`.

---

## 7. Ruta principal: Docker local

## 7.1 Verificar Docker

```bash
docker --version
```

Resultado esperado:

```text
Docker version ...
```

También comprobar el servicio:

```bash
docker info
```

Si `docker --version` funciona pero `docker info` falla, el motor no está iniciado.

---

## 7.2 Descargar una versión fija de ManimCE

Para reproducibilidad, usar una etiqueta de versión, no `stable`.

```bash
docker pull manimcommunity/manim:v0.20.1
```

Tiempo habitual:

- conexión rápida: 2–5 min;
- primera descarga lenta: 5–15 min.

No cancelar antes de 10 minutos si las capas siguen avanzando.

---

## 7.3 Prueba rápida en Linux o macOS

```bash
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp/manim-home \
  -v "$PWD:/manim" \
  -w /manim \
  manimcommunity/manim:v0.20.1 \
  manim -pql main.py NombreEscena \
  --format=mp4 \
  --disable_caching
```

### Razón de `--user`

Evita que el contenedor genere archivos propiedad de `root` y previene errores de escritura en `media/`.

### Razón de `HOME=/tmp/manim-home`

Proporciona un directorio escribible para cachés y configuración.

---

## 7.4 Prueba rápida en PowerShell

```powershell
docker run --rm -it `
  -v "${PWD}:/manim" `
  -w /manim `
  manimcommunity/manim:v0.20.1 `
  manim -pql main.py NombreEscena `
  --format=mp4 `
  --disable_caching
```

En Docker Desktop para Windows normalmente no se necesita mapear UID/GID.

---

## 7.5 Render final con `-pqh` en Linux o macOS

En entornos gráficos:

```bash
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp/manim-home \
  -v "$PWD:/manim" \
  -w /manim \
  manimcommunity/manim:v0.20.1 \
  manim -pqh main.py NombreEscena \
  --format=mp4 \
  --disable_caching
```

---

## 7.6 Render literal `-pqh` en entorno sin interfaz

GitHub Actions, servidores y algunos contenedores no pueden abrir el reproductor solicitado por `-p`.

Usar un reemplazo temporal de `xdg-open`:

```bash
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp/manim-home \
  -v "$PWD:/manim" \
  -w /manim \
  --entrypoint bash \
  manimcommunity/manim:v0.20.1 \
  -c '
    set -euo pipefail
    mkdir -p /tmp/colab-bin
    printf "#!/usr/bin/env bash\nexit 0\n" > /tmp/colab-bin/xdg-open
    chmod +x /tmp/colab-bin/xdg-open
    export PATH="/tmp/colab-bin:$PATH"

    manim -pqh main.py NombreEscena \
      --format=mp4 \
      --disable_caching
  '
```

### Importante: usar `bash -c`, no `bash -lc`

El shell de inicio `bash -lc` puede reconstruir `PATH` y ocultar el ejecutable `manim` instalado dentro de la imagen oficial.

Correcto:

```bash
bash -c 'manim ...'
```

Riesgoso:

```bash
bash -lc 'manim ...'
```

---

## 8. Ruta alternativa: entorno virtual local

Usar esta ruta cuando Docker no está disponible, pero existe acceso a paquetes Python y dependencias del sistema.

## 8.1 Crear el entorno

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

---

## 8.2 Actualizar herramientas

```bash
python -m pip install --upgrade pip setuptools wheel
```

---

## 8.3 Instalar ManimCE

```bash
python -m pip install manim==0.20.1
```

---

## 8.4 Verificar dependencias

```bash
manim --version
ffmpeg -version
latex --version
dvisvgm --version
```

Si `latex` o `dvisvgm` faltan, instalar TeX Live.

Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y \
  ffmpeg \
  libcairo2-dev \
  libpango1.0-dev \
  pkg-config \
  python3-dev \
  texlive \
  texlive-latex-extra \
  texlive-fonts-recommended \
  texlive-science \
  tipa \
  dvisvgm
```

---

## 8.5 Render

Prueba:

```bash
manim -pql main.py NombreEscena --format=mp4 --disable_caching
```

Final:

```bash
manim -pqh main.py NombreEscena --format=mp4 --disable_caching
```

En servidor sin interfaz:

```bash
manim -qh main.py NombreEscena --format=mp4 --disable_caching
```

---

## 9. Qué hacer si `pip` o `apt` no tienen acceso de red

No repetir indefinidamente el mismo comando.

Después de:

- 2–3 intentos de `pip`;
- confirmación de errores 5xx, DNS o conexión;
- confirmación de índices Debian inexistentes o bloqueados;

cambiar de ruta.

Orden recomendado:

1. Docker local ya instalado.
2. Entorno virtual local.
3. Google Colab.
4. GitHub Actions con la imagen oficial.
5. Otro servidor controlado.

No declarar que Manim fue instalado si el instalador no terminó correctamente.

---

## 10. Ruta remota: GitHub Actions con Docker

Esta ruta es apropiada cuando:

- el entorno local no permite instalar paquetes;
- Docker local no está disponible;
- se necesita un render reproducible;
- el repositorio tiene GitHub Actions habilitado.

### Principio de seguridad

- usar una rama temporal;
- no modificar `main`;
- abrir un PR en borrador si se necesita activar el workflow;
- no fusionar el PR;
- cerrar el PR después de descargar el artifact.

---

## 10.1 Workflow completo

Crear:

```text
.github/workflows/render_manim_pqh.yml
```

Contenido:

```yaml
name: Render Manim PQH

on:
  workflow_dispatch:
  pull_request:
    branches:
      - main

permissions:
  contents: read

jobs:
  render:
    runs-on: ubuntu-latest
    timeout-minutes: 120

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Validate Python source
        shell: bash
        run: |
          set -euo pipefail
          python -m py_compile main.py
          test -s main.py

      - name: Pull official Manim image
        shell: bash
        run: |
          set -euo pipefail
          docker pull manimcommunity/manim:v0.20.1

      - name: Render with literal -pqh
        shell: bash
        run: |
          set -euo pipefail

          set +e
          docker run --rm \
            --user "$(id -u):$(id -g)" \
            -e HOME=/tmp/manim-home \
            -v "$PWD:/manim" \
            -w /manim \
            --entrypoint bash \
            manimcommunity/manim:v0.20.1 \
            -c '
              set -euo pipefail
              mkdir -p /tmp/colab-bin
              printf "#!/usr/bin/env bash\nexit 0\n" > /tmp/colab-bin/xdg-open
              chmod +x /tmp/colab-bin/xdg-open
              export PATH="/tmp/colab-bin:$PATH"

              manim -pqh main.py NombreEscena \
                --format=mp4 \
                --disable_caching
            ' 2>&1 | tee render.log

          status=${PIPESTATUS[0]}
          set -e
          echo "$status" > render_status.txt

      - name: Verify MP4
        id: verify
        shell: bash
        run: |
          set -euo pipefail

          status="$(cat render_status.txt)"
          if [ "$status" -ne 0 ]; then
            echo "Render failed with status $status"
            exit "$status"
          fi

          VIDEO="$(find media -type f -name 'NombreEscena.mp4' -print -quit)"
          test -n "$VIDEO"
          test -s "$VIDEO"

          echo "video=$VIDEO" >> "$GITHUB_OUTPUT"
          ls -lh "$VIDEO"

          if command -v ffprobe >/dev/null 2>&1; then
            ffprobe -v error \
              -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt \
              -show_entries format=duration,size \
              -of default=noprint_wrappers=1 \
              "$VIDEO" || true
          fi

      - name: Stage delivery
        shell: bash
        run: |
          set -euo pipefail
          mkdir -p delivery

          cp "${{ steps.verify.outputs.video }}" \
            delivery/NombreEscena_pqh.mp4

          cp main.py delivery/
          cp render.log delivery/

          sha256sum delivery/* > delivery/SHA256SUMS.txt

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: NombreEscena_pqh
          path: delivery/
          if-no-files-found: error
          retention-days: 7
```

---

## 10.2 Tiempos de GitHub Actions

### Primera ejecución

1. Cola: 0–5 min.
2. Checkout: 10–60 s.
3. Descarga de imagen Docker: 1–8 min.
4. Render: 5–45 min para una clase larga.
5. Verificación: 5–30 s.
6. Empaquetado: 5–30 s.
7. Carga del artifact: 10 s–3 min.

### Umbral de intervención

- `queued` durante menos de 10 min: normal.
- `docker pull` durante menos de 15 min: normal si las capas avanzan.
- render sin error durante menos de 45 min: no cancelar una escena larga.
- sin nuevos logs durante 20–30 min: revisar CPU, timeout y tamaño del proyecto.

---

## 11. Localización robusta del MP4

No asumir siempre una carpeta fija.

Manim normalmente genera:

```text
media/videos/<nombre_archivo>/<calidad>/<NombreEscena>.mp4
```

Ejemplo:

```text
media/videos/main/1080p30/MainScene.mp4
```

Buscar de forma robusta:

```bash
find media -type f -name 'NombreEscena.mp4'
```

PowerShell:

```powershell
Get-ChildItem .\media -Recurse -Filter "NombreEscena.mp4"
```

Seleccionar el archivo más reciente si existen varias versiones.

Linux:

```bash
find media -type f -name 'NombreEscena.mp4' \
  -printf '%T@ %p\n' \
  | sort -nr \
  | head -1
```

---

## 12. Verificación técnica del video

## 12.1 Confirmar existencia y tamaño

```bash
test -s media/videos/.../NombreEscena.mp4
ls -lh media/videos/.../NombreEscena.mp4
```

---

## 12.2 Inspeccionar con `ffprobe`

```bash
ffprobe -v error \
  -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt \
  -show_entries format=duration,size \
  -of default=noprint_wrappers=1 \
  NombreEscena.mp4
```

Salida esperada:

```text
codec_name=h264
width=1920
height=1080
pix_fmt=yuv420p
r_frame_rate=30/1
duration=...
size=...
```

---

## 12.3 Generar suma SHA-256

Linux/macOS:

```bash
sha256sum NombreEscena.mp4
```

PowerShell:

```powershell
Get-FileHash .\NombreEscena.mp4 -Algorithm SHA256
```

---

## 12.4 Probar decodificación completa

```bash
ffmpeg -v error -i NombreEscena.mp4 -f null -
```

Si el comando termina sin errores, FFmpeg pudo leer el video completo.

---

## 12.5 Extraer fotogramas de control

Inicio:

```bash
ffmpeg -ss 00:00:05 -i NombreEscena.mp4 -frames:v 1 frame_inicio.png
```

Mitad:

```bash
ffmpeg -ss 00:01:30 -i NombreEscena.mp4 -frames:v 1 frame_mitad.png
```

Final:

```bash
ffmpeg -sseof -5 -i NombreEscena.mp4 -frames:v 1 frame_final.png
```

Revisar:

- márgenes;
- títulos;
- ecuaciones;
- colores;
- figuras;
- triángulos auxiliares;
- textos duplicados;
- elementos persistentes de escenas previas.

---

## 13. Empaquetado de entrega

Crear carpeta:

```bash
mkdir -p delivery
```

Copiar:

```bash
cp NombreEscena.mp4 delivery/
cp main.py delivery/
```

Crear registro:

```bash
cat > delivery/RENDER_INFO.txt <<'EOF'
Scene: NombreEscena
Source: main.py
ManimCE: 0.20.1
Command:
manim -pqh main.py NombreEscena --format=mp4 --disable_caching
EOF
```

Calcular hashes:

```bash
sha256sum delivery/* > delivery/SHA256SUMS.txt
```

Comprimir:

```bash
zip -r NombreEscena_pqh_delivery.zip delivery/
```

---

## 14. Errores reales y soluciones obligatorias

## 14.1 `manim: command not found` dentro de la imagen oficial

### Causa posible

Uso de un shell de inicio:

```bash
bash -lc
```

que reemplaza el `PATH` configurado por la imagen.

### Solución

Usar:

```bash
bash -c
```

y conservar el `PATH` original.

---

## 14.2 `PermissionError` al crear `media/`

### Causa

El usuario del contenedor no tiene permiso sobre el volumen montado.

### Solución Linux:

```bash
--user "$(id -u):$(id -g)"
-e HOME=/tmp/manim-home
```

También asegurar que el directorio sea escribible:

```bash
mkdir -p media
chmod u+rwx media
```

No usar `chmod 777` salvo como diagnóstico temporal.

---

## 14.3 El render termina, pero el workflow no encuentra el MP4

### Causa

Ruta codificada incorrectamente.

### Solución

No asumir el nombre de carpeta de calidad. Usar:

```bash
find media -type f -name 'NombreEscena.mp4' -print -quit
```

---

## 14.4 `ffprobe` hace fallar una entrega válida

### Causa

`ffprobe` no está instalado en el host o devuelve un código no crítico.

### Solución

Hacer la inspección condicional:

```bash
if command -v ffprobe >/dev/null 2>&1; then
  ffprobe ... "$VIDEO" || true
fi
```

La verificación obligatoria debe ser:

```bash
test -s "$VIDEO"
```

---

## 14.5 `xdg-open` falla al usar `-pqh`

### Causa

El entorno no tiene escritorio.

### Soluciones

Preferida para automatización:

```bash
manim -qh ...
```

Cuando el requisito exige literalmente `-pqh`, usar un shim temporal:

```bash
mkdir -p /tmp/colab-bin
printf '#!/usr/bin/env bash\nexit 0\n' > /tmp/colab-bin/xdg-open
chmod +x /tmp/colab-bin/xdg-open
export PATH="/tmp/colab-bin:$PATH"
```

---

## 14.6 Unicode incompatible con LaTeX

Síntoma típico:

```text
LaTeX Error: Unicode character ... not set up for use with LaTeX
```

Soluciones:

- reemplazar el símbolo en texto normal;
- usar `MathTex`;
- usar comandos LaTeX como `\Sigma`;
- evitar copiar símbolos Unicode directamente dentro de `Tex`.

---

## 14.7 Asset faltante

Orden de diagnóstico:

1. comprobar la ruta;
2. comprobar mayúsculas y minúsculas;
3. comprobar extensión;
4. convertir ruta absoluta en relativa;
5. verificar que el archivo esté en el volumen Docker;
6. usar placeholder solo si el original no está disponible;
7. documentar la sustitución.

---

## 14.8 Caché desactualizada

Usar:

```bash
--disable_caching
```

y, si es necesario:

```bash
rm -rf media/Tex media/texts
```

No borrar toda la carpeta `media/` sin conservar el producto final.

---

## 14.9 La escena parece detenida

Antes de cancelar:

```bash
ps aux | grep -E 'manim|ffmpeg|latex'
du -sh media
find media -type f -mmin -2
```

Si hay actividad, continuar.

Si no hay actividad ni nuevos logs durante 20–30 min:

- revisar memoria;
- revisar espacio;
- revisar timeout;
- buscar un proceso LaTeX bloqueado;
- comprobar si existe traceback truncado.

---

## 15. Protocolo de revisión visual

Después de renderizar:

### 15.1 Inicio

Comprobar:

- portada centrada;
- título dentro del margen;
- ausencia de parpadeo;
- fondo correcto;
- elementos no heredados de otra escena.

### 15.2 Secciones matemáticas

Comprobar:

- ecuaciones legibles;
- colores vinculados a la figura;
- transformaciones coherentes;
- ausencia de ecuaciones duplicadas;
- pausas suficientes;
- flechas con sentido correcto.

### 15.3 Figuras geométricas

Comprobar:

- proporciones reales;
- orientación correcta;
- etiquetas fuera de flechas y vértices;
- marcadores de ángulo recto;
- hipotenusa paralela al vector cuando corresponda;
- ningún triángulo auxiliar invertido.

### 15.4 Transiciones

Comprobar:

- objetos antiguos realmente eliminados;
- títulos sin acumulación;
- cámara sin saltos;
- limpieza completa entre secciones.

### 15.5 Final

Comprobar:

- cierre visible;
- sin pantalla negra excesiva;
- sin objetos cortados;
- video termina en el momento esperado.

---

## 16. Caso de referencia validado

### Código

```text
Statics_Week_VectorDecomposition_RightTriangles_Fixed_Rendered.py
```

### Escena

```text
Statics_Week_VectorDecomposition_Full
```

### Comando exacto

```bash
manim -pqh \
  Statics_Week_VectorDecomposition_RightTriangles_Fixed_Rendered.py \
  Statics_Week_VectorDecomposition_Full \
  --format=mp4 \
  --disable_caching
```

### Configuración detectada

```text
1920 × 1080
30 fps
```

### Resultado verificado

```text
codec_name=h264
width=1920
height=1080
pix_fmt=yuv420p
r_frame_rate=30/1
duration=188.222591
size=10896192
```

### Controles de entorno disponibles

```bash
JR_REAL_TIMER=0
JR_SHOW_ANSWER_KEY=0
```

Ejemplo Docker:

```bash
docker run --rm \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp/manim-home \
  -e JR_REAL_TIMER=0 \
  -e JR_SHOW_ANSWER_KEY=0 \
  -v "$PWD:/manim" \
  -w /manim \
  --entrypoint bash \
  manimcommunity/manim:v0.20.1 \
  -c '
    set -euo pipefail
    mkdir -p /tmp/colab-bin
    printf "#!/usr/bin/env bash\nexit 0\n" > /tmp/colab-bin/xdg-open
    chmod +x /tmp/colab-bin/xdg-open
    export PATH="/tmp/colab-bin:$PATH"

    manim -pqh \
      Statics_Week_VectorDecomposition_RightTriangles_Fixed_Rendered.py \
      Statics_Week_VectorDecomposition_Full \
      --format=mp4 \
      --disable_caching
  '
```

---

## 17. Secuencia mínima obligatoria

No omitir este orden:

1. Confirmar archivo.
2. Confirmar escena.
3. Ejecutar `py_compile`.
4. Revisar rutas y assets.
5. Revisar Unicode/LaTeX.
6. Renderizar `-pql`.
7. Revisar visualmente.
8. Corregir.
9. Repetir `-pql`.
10. Renderizar `-pqh`.
11. Localizar el MP4 con `find`.
12. Verificar archivo no vacío.
13. Ejecutar `ffprobe`.
14. Extraer fotogramas de control.
15. Calcular SHA-256.
16. Empaquetar código y video.
17. Registrar comando y versión.
18. Entregar.

---

## 18. Checklist final

### Código

- [ ] El archivo `.py` existe.
- [ ] `py_compile` termina correctamente.
- [ ] La escena existe.
- [ ] Las rutas son relativas.
- [ ] Los assets existen.
- [ ] No hay Unicode incompatible en `Tex`.
- [ ] La resolución está definida.
- [ ] Los FPS están definidos.
- [ ] Los flags de entorno están documentados.

### Prueba

- [ ] Se ejecutó `-pql`.
- [ ] No hay traceback.
- [ ] No hay recortes.
- [ ] No hay superposiciones.
- [ ] Las figuras tienen orientación correcta.
- [ ] Las ecuaciones son legibles.
- [ ] Las transiciones limpian objetos antiguos.

### Final

- [ ] Se ejecutó el comando literal `-pqh`.
- [ ] El MP4 existe.
- [ ] El MP4 no está vacío.
- [ ] `ffprobe` puede leerlo.
- [ ] Resolución correcta.
- [ ] FPS correctos.
- [ ] Códec H.264.
- [ ] Formato `yuv420p`.
- [ ] Se revisaron fotogramas.
- [ ] Se calculó SHA-256.
- [ ] Se conservó el código exacto.
- [ ] Se registró el comando.
- [ ] Se creó paquete de entrega.

---

## 19. Formato de informe de éxito

```text
Render completado correctamente.

Fuente:
- main.py

Escena:
- NombreEscena

Versión:
- ManimCE 0.20.1

Comando:
- manim -pqh main.py NombreEscena --format=mp4 --disable_caching

Salida:
- media/videos/.../NombreEscena.mp4

Video:
- Resolución: 1920 × 1080
- FPS: 30
- Códec: H.264
- Formato de píxel: yuv420p
- Duración: ...
- Tamaño: ...

Validaciones:
- Python: aprobado
- Manim: aprobado
- ffprobe: aprobado
- inspección visual: aprobada
- SHA-256: ...
```

---

## 20. Formato de informe de fallo

```text
El render final no se completó.

Etapa:
- instalación / validación / LaTeX / render / verificación / artifact

Error exacto:
- incluir la última parte del traceback

Causa confirmada o probable:
- describir sin inventar

Acciones realizadas:
- py_compile
- revisión de rutas
- prueba -pql
- revisión de permisos
- revisión de PATH
- revisión de LaTeX

Siguiente corrección:
- indicar el cambio concreto

Archivos parciales conservados:
- listar rutas
```

No responder únicamente “falló”. Siempre conservar logs y entregar un diagnóstico reproducible.

---

## 21. Comandos rápidos

### Validar

```bash
python -m py_compile main.py
```

### Probar

```bash
manim -pql main.py NombreEscena --format=mp4 --disable_caching
```

### Render final

```bash
manim -pqh main.py NombreEscena --format=mp4 --disable_caching
```

### Buscar salida

```bash
find media -type f -name 'NombreEscena.mp4'
```

### Verificar

```bash
ffprobe -v error \
  -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt \
  -show_entries format=duration,size \
  -of default=noprint_wrappers=1 \
  NombreEscena.mp4
```

### Hash

```bash
sha256sum NombreEscena.mp4
```

### Comprobar decodificación

```bash
ffmpeg -v error -i NombreEscena.mp4 -f null -
```

---

## 22. Regla final

Un archivo `.mp4` no debe entregarse únicamente porque Manim terminó.

Debe existir evidencia de:

- compilación correcta;
- render completo;
- resolución correcta;
- lectura correcta por FFmpeg;
- inspección visual;
- código fuente conservado;
- comando reproducible;
- hash de integridad.

Solo entonces el render `-pqh` se considera listo para entrega.
