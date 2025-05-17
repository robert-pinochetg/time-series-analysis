import os
import requests

# Carpeta donde se guardarán los archivos descargados
download_folder = "00-excel-files"
os.makedirs(download_folder, exist_ok=True)

# Función para generar nombre de archivo local
def generate_filename(year, week):
    return f"ukestat-laks-og-orret-uke{str(week).zfill(2)}-{year}.xlsx"

# Función para intentar descargar un archivo desde una URL
def try_download(url, file_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(response.content)
        return True
    except requests.exceptions.RequestException:
        return False

# Lógica principal
for year in range(2020, 2026):
    for week in range(1, 53):
        filename = generate_filename(year, week)
        file_path = os.path.join(download_folder, filename)

        # Si el archivo ya existe, saltar
        if os.path.exists(file_path):
            print(f"🔁 Ya existe: {filename}, se omite descarga.")
            continue

        base_url = f"https://en.seafood.no/globalassets/markedsinnsikt/apne-rapporter/ukestatistikk/{year}/"
        week_plain = f"uke{week}"
        week_dash = f"uke-{week}"

        # Intentar descargar con guión
        url_with_dash = base_url + f"ukestat-laks-og-orret-{week_dash}.xlsx"
        if try_download(url_with_dash, file_path):
            print(f"✅ Descargado: {filename}")
            continue

        # Intentar descargar sin guión
        url_without_dash = base_url + f"ukestat-laks-og-orret-{week_plain}.xlsx"
        if try_download(url_without_dash, file_path):
            print(f"✅ Descargado: {filename}")
            continue

        # Si ninguno funcionó, se detiene bajo el supuesto de que ya no hay más archivos disponibles
        print(f"❌ No se encontró archivo para semana {week} de {year}. Descarga detenida.")
        break  # Se detiene la descarga para ese año
