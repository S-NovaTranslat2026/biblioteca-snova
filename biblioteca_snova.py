from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json
import string

GENERADO_EN = datetime.now()

base = Path(".")  # Esto es temporal

# --------------------------------------------------
# LECTURA DE biblioteca.json
# --------------------------------------------------

with open("biblioteca.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

archivos = []

for letra, lista_archivos in datos.items():

    for item in lista_archivos:

        nombre_sin_extension = Path(item["nombre"]).stem

        fecha_dt = datetime.fromisoformat(
            item["fecha_mod"].replace("Z", "+00:00")
        )

        archivos.append({
            "nombre": nombre_sin_extension,
            "fecha_dt": fecha_dt,
            "fecha": fecha_dt.strftime("%d/%m/%Y"),
            "letra": letra,
            "ruta": f"https://drive.google.com/uc?export=download&id={item['id']}"
        })

archivos_ordenados = sorted(
    archivos,
    key=lambda x: x["fecha_dt"],
    reverse=True
)

por_fecha = defaultdict(list)
por_letra = defaultdict(list)

for a in archivos:
    por_fecha[a["fecha"]].append(a)
    por_letra[a["letra"]].append(a)

# --------------------------------------------------
# HTML CABECERA
# --------------------------------------------------

def header():

    ultima_fecha = GENERADO_EN.strftime("%d/%m/%Y %H:%M:%S")

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Biblioteca de Traducciones</title>

<style>

body {{
    background-color: #1a1a1a;
    color: #e0e0e0;
    font-family: Arial, sans-serif;
    margin: 20px;
}}

a {{
    color: #8ab4f8;
    text-decoration: none;
}}

a:hover {{
    text-decoration: underline;
}}

.container {{
    max-width: 1500px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    gap: 20px;
}}

.col {{
    width: 50%;
}}

.box {{
    background-color: #1e1e1e;
    border: 1px solid #333;
    border-radius: 6px;
    padding: 10px;
    margin-bottom: 20px;
}}

.scroll {{
    max-height: 600px;
    overflow-y: auto;
}}


.cabecera {{
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 20px;
    max-width: 1000px;
    margin: 0 auto 12px auto;
}}

.logo-cabecera {{
    width: 100px;
    height: 100px;
    object-fit: contain;
}}

.logo-izquierda {{
    justify-self: end;
}}

.logo-derecha {{
    justify-self: start;
}}

.title {{
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    margin: 0;
    color: #9f7bff;
    letter-spacing: 1px;
    white-space: nowrap;
}}

@media (max-width: 500px) {{
    .cabecera {{
        gap: 8px;
    }}

    .logo-cabecera {{
        width: 55px;
        height: 55px;
    }}

    .title {{
        font-size: 24px;
    }}
}}


.header-info {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 20px;
    color: #b0b0b0;
    margin-bottom: 10px;
    max-width: 1500px;
    margin-left: auto;
    margin-right: auto;
}}

.header-info div {{
    width: 50%;
}}

.header-info div:first-child {{
    text-align: left;
}}

.header-info div:last-child {{
    text-align: right;
}}

.barra-busqueda {{
    display: flex;
    gap: 10px;
    align-items: center;
}}

#buscador {{
    flex: 1;
    max-width: 500px;
}}

.indice-titulo {{
    text-align: center;
    margin-bottom: 10px;
}}

.indice-botones {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 10px;
}}

.btn-letra {{
    background-color: #2a2a2a;
    color: #e0e0e0;
    border: 1px solid #444;
    border-radius: 5px;
    padding: 7px 15px;
    cursor: pointer;
    font-size: 15px;
    transition: all 0.15s ease;
}}

.btn-letra:hover {{
    background-color: #353535;
    border-color: #666;
    transform: translateY(-1px);
}}

.btn-activo {{
    background-color: #4a6480;
    border-color: #6f9ed8;
    color: #ffffff;
    transform: scale(1.05);
    transform: translateY(-1px);
    transition: all 0.55s ease;
}}

.btn-activo:hover {{
    background-color: #5a7aa0;
    border-color: #8fb3e0;
}}

.btn-letra:active {{
    transform: translateY(0px) scale(0.98);
}}

.categoria-especial {{
    text-align: center;
    margin-top: 15px;
}}

#contenido-letra {{
    margin-top: 15px;
}}

.fecha {{
    font-weight: bold;
    margin-top: 15px;
}}

.separador-indice {{
    height: 1px;
    background: #333;
    border: none;
    margin: 10px 0 15px 0;
}}

.btn-letra .letra {{
    font-weight: bold;
    font-size: 18px;
    color: #ffffff;
}}

.btn-letra .count {{
    font-size: 12px;
    color: #9a9a9a;
    margin-left: 6px;
}}

.btn-vacio {{
    opacity: 0.35;
    cursor: not-allowed;
    filter: grayscale(40%);
}}

.btn-vacio:hover {{
    opacity: 0.5;
    background-color: #2a2a2a; /* evita “efecto hover engañoso” */
}}

.titulo-busqueda {{
    font-size: 24px;
    font-weight: bold;
    color: #4caf50;
}}

</style>

</head>
<body>


<div class="cabecera">
    <img src="imagenes/logo_izquierda.png"
         alt="Logo izquierdo"
         class="logo-cabecera logo-izquierda">

    <div class="title">Biblioteca</div>

    <img src="imagenes/logo_derecha.png"
         alt="Logo derecho"
         class="logo-cabecera logo-derecha">
</div>


<div class="header-info">
  <div>Última actualización: {ultima_fecha}</div>
  <div>Total de la biblioteca: {len(archivos)} archivos</div>
</div>

<hr>
"""

# --------------------------------------------------
# INDEX.HTML
# --------------------------------------------------

index_html = header()

biblioteca = [
    {
        "nombre": a["nombre"],
        "ruta": a["ruta"],
        "letra": a["letra"]
    }
    for a in archivos_ordenados
]

biblioteca_js = json.dumps(biblioteca, ensure_ascii=False)

index_html += f"""

<div class="container">

<!-- IZQUIERDA -->
<div class="col">

<div class="box scroll">

<h2>Historial cronológico</h2>
"""

historial_js = [
    {
        "fecha": fecha,
        "archivos": [
            {
                "nombre": a["nombre"],
                "ruta": a["ruta"],
                "letra": a["letra"]
            }
            for a in sorted(
                por_fecha[fecha],
                key=lambda x: x["nombre"]
            )
        ]
    }
    for fecha in sorted(
        por_fecha.keys(),
        key=lambda x: datetime.strptime(x, "%d/%m/%Y"),
        reverse=True
    )
]

historial_js_json = json.dumps(
    historial_js,
    ensure_ascii=False
)

index_html += """
<div id="historial-cronologico"></div>
"""

index_html += """
</div>

</div>

<!-- DERECHA -->
<div class="col">

<div class="box">

<div class="barra-busqueda">
    <span class="titulo-busqueda">Buscador</span>
    <input type="text" id="buscador" placeholder="Buscar...">
</div>

<p id="contador">0 resultados</p>
<div id="resultados" class="scroll"></div>

</div>

<div class="box scroll">

<h2 class="indice-titulo">
    Índice alfabético:
    <span style="font-size:14px; font-weight:normal;">
        (Seleccione una letra)
    </span>
</h2>

<hr class="separador-indice">

<div class="indice-botones">
"""

letras_base = list(string.ascii_uppercase)
especial = "0-99"

todas_las_letras = letras_base + [especial]

letras_normales = []

for letra in todas_las_letras:

    cantidad = len(por_letra.get(letra, []))

    clase_extra = "btn-vacio" if cantidad == 0 else ""

    # -----------------------------
    # BOTÓN NORMAL O ESPECIAL (YA UNIFICADO)
    # -----------------------------

    if letra == especial:

        # botón 0-99 (especial)
        categoria_especial = f"""
        <button class="btn-letra {clase_extra}"
                onclick="if ({cantidad} > 0) mostrarLetra('{letra}')">

            <span class="letra">0-9 y símbolos</span>
            <span class="count">({cantidad})</span>

        </button>
        """

    else:

        letras_normales.append(f"""
        <button class="btn-letra {clase_extra}"
                onclick="if ({cantidad} > 0) mostrarLetra('{letra}')">

            <span class="letra">{letra}</span>
            <span class="count">({cantidad})</span>

        </button>
        """)

index_html += "".join(letras_normales)

index_html += "</div>"

if categoria_especial:
    index_html += f'''
    <div class="categoria-especial">
        {categoria_especial}
    </div>
    '''

index_html += """
<hr>

<div id="contenido-letra">
Seleccione una letra
</div>

</div>

</div>

</div>

<script>

const biblioteca = """ + biblioteca_js + """;

const historialCronologico = """ + historial_js_json + """;

let letraActiva = null;


let archivoSeleccionado = null;


function crearFilaArchivo(item) {
    const fila = document.createElement("div");

    Object.assign(fila.style, {
        display: "flex",
        alignItems: "center",
        gap: "20px",
        flexWrap: "wrap"
    });

    const nombre = document.createElement("a");
    nombre.href = "#";
    nombre.textContent = item.nombre;

    if (archivoSeleccionado?.ruta === item.ruta) {
        nombre.style.color = "#d97706";
        nombre.style.fontWeight = "bold";
    }

    nombre.addEventListener("click", event => {
        event.preventDefault();

        archivoSeleccionado =
            archivoSeleccionado?.ruta === item.ruta ? null : item;
        
        mostrarHistorialCronologico();

        if (letraActiva !== null) {
            mostrarLetra(letraActiva);
        }

        actualizarResultadosBusqueda();
    });

    fila.appendChild(nombre);

    if (archivoSeleccionado?.ruta === item.ruta) {
        const descargar = document.createElement("a");
        descargar.href = item.ruta;
        descargar.textContent = "Descarga";
        descargar.title = "Descargar archivo";

        Object.assign(descargar.style, {
            display: "inline-block",
            marginLeft: "60px",
            padding: "4px 10px",
            background: "#245a81",
            color: "#ffffff",
            borderRadius: "5px",
            textDecoration: "none",
            fontSize: "0.9em",
            fontWeight: "bold"
        });

        const verLink = document.createElement("button");
        verLink.type = "button";
        verLink.textContent = "Ruta Enlace";

        verLink.addEventListener("click", () => {
            abrirModalLink(item.ruta);
        });

        fila.appendChild(descargar);
        fila.appendChild(verLink);
    }

    return fila;
}

function mostrarHistorialCronologico() {
    const contenedor = document.getElementById("historial-cronologico");

    contenedor.innerHTML = "";

    historialCronologico.forEach(grupo => {
        const fecha = document.createElement("div");
        fecha.className = "fecha";
        fecha.textContent = grupo.fecha;
        contenedor.appendChild(fecha);

        const ul = document.createElement("ul");

        grupo.archivos.forEach(item => {
            const li = document.createElement("li");
            li.appendChild(crearFilaArchivo(item));
            ul.appendChild(li);
        });

        contenedor.appendChild(ul);
    });
}

function mostrarLetra(letra) {
    document.getElementById("contenido-letra")
        .scrollIntoView({ behavior: "smooth", block: "start" });

    letraActiva = letra;

    const contenedor = document.getElementById("contenido-letra");

    document.querySelectorAll(".btn-letra")
        .forEach(btn => btn.classList.remove("btn-activo"));

    document.querySelectorAll(".btn-letra")
        .forEach(btn => {
            if (btn.getAttribute("onclick")?.includes(letra)) {
                btn.classList.add("btn-activo");
            }
        });

    const items = biblioteca
        .filter(item => item.letra === letra)
        .sort((a, b) =>
            a.nombre.localeCompare(b.nombre, "es", {
                sensitivity: "base"
            })
        );

    contenedor.innerHTML = "";

    const titulo = document.createElement("h3");
    titulo.textContent = `${letra} (${items.length} archivos)`;
    contenedor.appendChild(titulo);

    const ul = document.createElement("ul");

    items.forEach(item => {
        const li = document.createElement("li");
        li.appendChild(crearFilaArchivo(item));
        ul.appendChild(li);
    });

    contenedor.appendChild(ul);
}



function abrirModalLink(url) {
    const anterior = document.getElementById("modal-link");

    if (anterior) {
        anterior.remove();
    }

    const fondo = document.createElement("div");
    fondo.id = "modal-link";

    Object.assign(fondo.style, {
        position: "fixed",
        inset: "0",
        background: "rgba(0, 0, 0, 0.65)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: "99999"
    });

    const ventana = document.createElement("div");

    Object.assign(ventana.style, {
        background: "#ffffff",
        color: "#222222",
        padding: "20px",
        borderRadius: "8px",
        width: "min(90%, 500px)",
        boxSizing: "border-box",
        boxShadow: "0 4px 20px rgba(0, 0, 0, 0.4)"
    });

    const titulo = document.createElement("h3");
    titulo.textContent = "Enlace del archivo";

    const campo = document.createElement("textarea");
    campo.value = url;
    campo.readOnly = true;

    Object.assign(campo.style, {
        width: "100%",
        minHeight: "65px",
        boxSizing: "border-box",
        resize: "vertical",
        marginBottom: "12px"
    });

    const botones = document.createElement("div");

    Object.assign(botones.style, {
        display: "flex",
        justifyContent: "flex-end",
        gap: "8px",
        flexWrap: "wrap"
    });

    const copiar = document.createElement("button");
    copiar.type = "button";
    copiar.textContent = "Copiar";

    const cerrar = document.createElement("button");
    cerrar.type = "button";
    cerrar.textContent = "Cerrar";

    copiar.addEventListener("click", async () => {
        try {
            await navigator.clipboard.writeText(url);
            copiar.textContent = "¡Copiado!";
        } catch {
            campo.focus();
            campo.select();

            try {
                const correcto = document.execCommand("copy");
                copiar.textContent = correcto
                    ? "¡Copiado!"
                    : "Copia manualmente";
            } catch {
                copiar.textContent = "Copia manualmente";
            }
        }
    });

    cerrar.addEventListener("click", () => {
        fondo.remove();
    });

    botones.appendChild(copiar);
    botones.appendChild(cerrar);

    ventana.appendChild(titulo);
    ventana.appendChild(campo);
    ventana.appendChild(botones);
    fondo.appendChild(ventana);

    document.body.appendChild(fondo);

    campo.focus();
    campo.select();
}


const buscador = document.getElementById("buscador");
const resultados = document.getElementById("resultados");
const contador = document.getElementById("contador");

function actualizarResultadosBusqueda() {
    const texto = buscador.value.toLowerCase().trim();

    resultados.innerHTML = "";

    if (!texto) {
        contador.textContent = "0 resultados";
        return;
    }

    const coincidencias = biblioteca.filter(item =>
        item.nombre.toLowerCase().includes(texto)
    );

    contador.textContent = coincidencias.length + " resultados";

    coincidencias.slice(0, 50).forEach(item => {
        resultados.appendChild(crearFilaArchivo(item));
    });
}

buscador.addEventListener("input", actualizarResultadosBusqueda);

mostrarHistorialCronologico();

</script>

</body>
</html>
"""

# --------------------------------------------------
# GUARDAR
# --------------------------------------------------

(base / "index.html").write_text(index_html, encoding="utf-8")

print("OK - sistema actualizado")