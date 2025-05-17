import os
import requests

# Carpeta donde se guardarán los archivos descargados
download_folder = "01-downloads"
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Función para intentar descargar un archivo desde una URL
def try_download(url, year, week, suffix):
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Si se descarga exitosamente, guarda el archivo
        week_str = str(week).zfill(2)
        file_name = f"ukestat-laks-og-orret-uke{suffix}-{year}.xlsx"
        file_path = os.path.join(download_folder, file_name)
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Descargado: {file_name}")
        return True
    except requests.exceptions.RequestException:
        return False

# Iterar por años y semanas
for year in range(2023, 2026):
    for week in range(1, 53):
        week_plain = f"uke{week}"
        week_dash = f"uke-{week}"

        base_url = f"https://en.seafood.no/globalassets/markedsinnsikt/apne-rapporter/ukestatistikk/{year}/"

        # Primero intenta con guión
        url_with_dash = base_url + f"ukestat-laks-og-orret-{week_dash}.xlsx"
        if try_download(url_with_dash, year, week, f"-{str(week).zfill(2)}"):
            continue

        # Luego intenta sin guión
        url_without_dash = base_url + f"ukestat-laks-og-orret-{week_plain}.xlsx"
        if try_download(url_without_dash, year, week, str(week).zfill(2)):
            continue

        # Si ambos fallan
        print(f"❌ No se encontró archivo para semana {week} de {year}")
