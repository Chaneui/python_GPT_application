import os
from pillow_heif import register_heif_opener, open_heif
import piexif
import folium

register_heif_opener()

# 원본 폴더 경로 설정
source_folder = r'이 곳에 원본 이미지 파일이 위치한 폴더의 경로를 입력합니다'

map = folium.Map(location=[36, 128], zoom_start=8)

for filename in os.listdir(source_folder):
    if filename.lower().endswith('.heic'):
        source_path = os.path.join(source_folder, filename)

        try:
            heif_file = open_heif(source_path)
        except Exception as e:
            print(f"Error opening {filename}: {e}")
            continue

        metadata = heif_file.info.get('exif')
        
        if metadata:
            exif_dict = piexif.load(metadata)
            
            gps_info = exif_dict.get("GPS")
            if gps_info:
                gps_lat = gps_info.get(piexif.GPSIFD.GPSLatitude)
                gps_lat_ref = gps_info.get(piexif.GPSIFD.GPSLatitudeRef)
                gps_lon = gps_info.get(piexif.GPSIFD.GPSLongitude)
                gps_lon_ref = gps_info.get(piexif.GPSIFD.GPSLongitudeRef)

                if gps_lat and gps_lon and gps_lat_ref and gps_lon_ref:
                    def convert_to_degrees(value):
                        d, m, s = value
                        return d[0] / d[1] + (m[0] / m[1] / 60.0) + (s[0] / s[1] / 3600.0)
                    
                    lat = convert_to_degrees(gps_lat)
                    if gps_lat_ref == b'S':
                        lat = -lat
                    
                    lon = convert_to_degrees(gps_lon)
                    if gps_lon_ref == b'W':
                        lon = -lon

                    folium.Marker([lat, lon], tooltip=filename).add_to(map)
                    print(f"Added marker for {filename} at ({lat}, {lon})")
                else:
                    print(f"No complete GPS data found in {filename}")
            else:
                print(f"No GPS metadata found in {filename}")
        else:
            print(f"No EXIF metadata found in {filename}")

map.save(os.path.join(source_folder, 'image_map.html'))
print("Map has been saved as 'image_map.html'")