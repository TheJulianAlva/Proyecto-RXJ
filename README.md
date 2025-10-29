# Proyecto RXJ

Un juego de puzzles y exploración en 3D inspirado en los clásicos del *survival horror*, construido desde cero con Python, PyGame y OpenGL.


### Técnicas

* **Renderizado 3D en Tiempo Real:** Utiliza PyOpenGL para renderizar la escena 3D.
* **Modo Inmediato:** Todo el renderizado se basa en funciones clásicas de OpenGL (`glPushMatrix`, `glBegin`, etc.).
* **Gestión de Escena Basada en Triggers:** El cambio de cámara se gestiona mediante volúmenes de disparo (triggers) invisibles que el jugador activa al moverse.

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3
* **Ventana y Eventos:** [PyGame](https://www.pygame.org/news) (para el bucle principal, gestión de ventanas y eventos de input).
* **Gráficos 3D:** [PyOpenGL](http://pyopengl.sourceforge.net/) (para todas las llamadas de renderizado 3D).
---
## 🎮 Controles (Controles de Tanque)

* `W`: Moverse hacia adelante (en la dirección que mira el personaje).
* `S`: Moverse hacia atrás.
* `A`: Rotar (girar) a la izquierda.
* `D`: Rotar (girar) a la derecha.
* `E`: Interactuar (abrir puertas, examinar objetos).
* `ESC`: Abrir menú de pausa.
---
## 🏛️ Arquitectura y Patrones de Diseño

El proyecto está estructurado siguiendo patrones de diseño robustos para mantener el código limpio, escalable y desacoplado.

* **Programación Orientada a Objetos (OOP):** Cada entidad del juego (Jugador, Puerta, Puzzle) es una clase que gestiona su propio estado, lógica de actualización (`update()`) y renderizado (`draw()`).
* **Máquina de Estados (State Machine):** Un `engine.py` gestiona el estado global del juego (ej. `MenuState`, `PlayState`, `PauseState`), asegurando que solo la lógica relevante esté activa.
* **Patrón Singleton:** Se utiliza para los gestores globales que necesitan ser accesibles desde cualquier parte del código:
    * `InputManager`: Centraliza todo el input del teclado/ratón y lo traduce a "acciones" (ej. "move_forward").
    * `CameraManager`: Almacena todas las cámaras fijas (`Camera`) y gestiona cuál es la `active_camera`.
* **Patrón Observer (Planeado):** Se usará para la lógica de los puzzles. Un `Puzzle` (Subject) notificará a una `Door` (Observer) cuando sea resuelto.

### Estructura de Carpetas

```
Proyecto_RXJ/
├── main.py
├── engine.py             # Gestiona la máquina de estados
│
├── states/               # Estados del juego
│   ├── base_state.py
│   └── play_state.py
│
├── game_objects/         # Clases de objetos del mundo
│   ├── player.py
│   ├── camera.py
│   └── trigger_volume.py
│
└── systems/              # Singletons globales
    ├── input_manager.py
    └── camera_manager.py
```

## 🚀 Instalación y Ejecución (Configuración Inicial)

Esta guía es para configurar el proyecto en tu computadora por **primera vez**.

1.  **Clona el repositorio:**
    Abre tu terminal (Git Bash, Símbolo del sistema, etc.) y clona el proyecto en la carpeta que prefieras. Reemplaza `[URL_DEL_REPO]` con la URL SSH o HTTPS de GitHub.
    ```bash
    git clone [URL_DEL_REPO]
    ```
---

## 🤝 Flujo de Trabajo y Contribución (Git y GitHub)

Esta es la guía **obligatoria** que todo miembro del equipo debe seguir para añadir código al proyecto.

### Principio Fundamental: `main` está protegido

La rama `main` es nuestra versión estable. **NUNCA trabajamos directamente en `main`**. Todo el trabajo se hace en ramas separadas y se integra mediante *Pull Requests*.

---

### Paso 1: Crea tu Rama de Trabajo

Antes de escribir una sola línea de código, crea una rama nueva.

1.  **Sincroniza tu `main` local:**
    Asegúrate de tener la versión más reciente del proyecto.
    ```bash
    git checkout main
    git pull origin main
    ```

2.  **Crea y múevete a tu nueva rama:**
    Usa un nombre descriptivo para tu rama (ej. `feat/logica-jugador`, `fix/bug-colision`).
    ```bash
    git checkout -b nombre-de-tu-rama
    ```

### Paso 2: Trabaja y Haz Commits (¡Patrón Obligatorio!)

Modifica el código, añade tus mejoras y guarda tu progreso con *commits*.

1.  **Añade tus cambios:**
    ```bash
    git add .
    ```

2.  **Crea tu commit:**
    Usaremos un patrón de "Commits Convencionales" para mantener el historial limpio. Escribe tus mensajes de commit así:
    `tipo: [Descripción breve de lo que hiciste]`

    **Tipos comunes:**
    * **`feat:`** (Nueva característica. Ej: `feat: Implementa la clase Player y su movimiento`)
    * **`fix:`** (Corrección de un bug. Ej: `fix: Arregla el cálculo de rotación del jugador`)
    * **`docs:`** (Cambios en la documentación. Ej: `docs: Actualiza README con la guía de Git`)
    * **`style:`** (Formato, punto y coma, etc. Ej: `style: Formatea player.py según PEP8`)
    * **`refactor:`** (Cambios en el código que no añaden nada nuevo ni arreglan nada. Ej: `refactor: Mueve la lógica de dibujo del jugador a un método privado`)
    * **`test:`** (Añadir o modificar pruebas).

    **Comando de commit de ejemplo:**
    ```bash
    git commit -m "feat: Añade la clase TriggerVolume para los cambios de cámara"
    ```

### Paso 3: Sube tu Rama a GitHub

Cuando hayas terminado tu trabajo (o quieras guardarlo en la nube), sube tu rama.
```bash
# La primera vez que subes la rama, usa '-u' para enlazarla
git push -u origin nombre-de-tu-rama
```
Para subidas posteriores en la misma rama, solo necesitas:
```bash
git push
```

### Paso 4: Crea un Pull Request (PR)

Aquí es donde pides que tu código se integre a `main`.

1.  Ve a la página del repositorio en **GitHub.com**.
2.  GitHub detectará automáticamente tu rama nueva y te mostrará un botón: **"Compare & pull request"**. Haz clic en él.
3.  **Rellena el PR:**
    * **Título:** Un título claro (ej. "Implementación de la clase Player").
    * **Descripción:** Explica **qué** hiciste, **por qué** y **cómo** pueden probarlo.
    * **Reviewers:** Asigna a uno o más compañeros de equipo para que revisen tu código.

### Paso 5: Revisión y Merge

1.  **Aprobación:** Una vez que tu PR esté listo, haz clic en el botón **"Merge pull request"**.
2.  ¡Felicidades! Tu código ahora es parte de la rama `main`.

### Paso 6: Limpieza y Sincronización

Después de que tu PR se haya integrado:

1.  Vuelve a tu `main` local y actualízalo.
    ```bash
    git checkout main
    git pull origin main
    ```
2.  (Opcional) Borra tu rama antigua, ya no la necesitas.
    ```bash
    git branch -d nombre-de-tu-rama
    ```

---

