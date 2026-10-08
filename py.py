import json
import math
import random

# Базовые настройки из gemini.json
RootObjectId = 335536
Blocks = []
object_id_counter = 100000

def generate_id():
    global object_id_counter
    object_id_counter += 1
    return object_id_counter

def add_cube(name, x, y, z, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, color="808080FF", flags=3):
    Blocks.append({
        "Name": name,
        "ObjectId": generate_id(),
        "ParentId": RootObjectId,
        "Position": {"x": x, "y": y, "z": z},
        "Rotation": {"x": rx, "y": ry, "z": rz},
        "Scale": {"x": sx, "y": sy, "z": sz},
        "BlockType": 1,
        "Properties": {
            "PrimitiveType": 3,
            "Color": color,
            "PrimitiveFlags": flags
        }
    })

def add_quad(name, x, y, z, rx=0.0, ry=0.0, rz=0.0, sx=1.0, sy=1.0, sz=1.0, color="808080FF", flags=3):
    Blocks.append({
        "Name": name,
        "ObjectId": generate_id(),
        "ParentId": RootObjectId,
        "Position": {"x": x, "y": y, "z": z},
        "Rotation": {"x": rx, "y": ry, "z": rz},
        "Scale": {"x": sx, "y": sy, "z": sz},
        "BlockType": 1,
        "Properties": {
            "PrimitiveType": 5,
            "Color": color,
            "PrimitiveFlags": flags
        }
    })

def add_light(name, x, y, z, color="F8BF6DFF", intensity=5.0, r=3.0, shadows=False):
    Blocks.append({
        "Name": name,
        "ObjectId": generate_id(),
        "ParentId": RootObjectId,
        "Position": {"x": x, "y": y, "z": z},
        "BlockType": 2,
        "Properties": {
            "Color": color,
            "Intensity": intensity,
            "Range": r,
            "Shadows": shadows
        }
    })

# --- ГЕНЕРАЦИЯ КАРТЫ ---

# 1. Пол и платформы
add_cube("Platform_Floor", 0, -0.5, 0, sx=60, sy=1, sz=120, color="3F3F3FFF")
add_cube("Platform_Left", -20, 0.5, 0, sx=15, sy=1, sz=100, color="595959FF")
add_cube("Platform_Right", 20, 0.5, 0, sx=15, sy=1, sz=100, color="595959FF")

# 2. Железнодорожные пути (4 пути)
for track_x in [-10, -5, 5, 10]:
    # Шпалы
    for z in range(-50, 50, 1):
        add_cube(f"Sleeper", track_x, 0.1, z, sx=1.5, sy=0.1, sz=0.3, color="434343FF")
    # Рельсы
    add_cube(f"Rail_L", track_x - 0.7, 0.2, 0, sx=0.1, sy=0.1, sz=100, color="717171FF")
    add_cube(f"Rail_R", track_x + 0.7, 0.2, 0, sx=0.1, sy=0.1, sz=100, color="717171FF")

# 3. Арочные своды (стиль метро)
arch_radius = 25
for z_pos in [-40, -10, 20, 50]:
    # Основная арка
    for angle in range(-90, 91, 5):
        rad = math.radians(angle)
        x = math.sin(rad) * arch_radius
        y = math.cos(rad) * arch_radius + 5
        rot_z = -angle
        add_cube(f"Arch_Main", x, y, z_pos, rz=rot_z, sx=0.5, sy=2.0, sz=1.0, color="717171FF")
        
        # Внутренняя арка (решетка)
        if angle % 10 == 0:
            add_cube(f"Arch_Inner", x*0.8, y*0.8 + 1, z_pos, rz=rot_z, sx=0.3, sy=1.5, sz=0.5, color="3F3F3FFF")
            # Соединительные балки
            add_cube(f"Arch_Strut", x*0.9, y*0.9 + 0.5, z_pos, rz=rot_z, sx=0.2, sy=0.2, sz=1.5, color="434343FF")

# 4. Колонны и опоры
for z_pos in range(-50, 51, 10):
    for x_pos in [-25, 25]:
        add_cube("Pillar", x_pos, 5, z_pos, sx=2, sy=10, sz=2, color="595959FF")
        # Балки жесткости
        add_cube("Brace", x_pos, 10, z_pos, rz=45, sx=0.5, sy=3, sz=0.5, color="717171FF")
        add_cube("Brace", x_pos, 10, z_pos, rz=-45, sx=0.5, sy=3, sz=0.5, color="717171FF")

# 5. Поезда на путях
def create_train(x_offset, z_offset):
    # Корпус
    add_cube("Train_Body", x_offset, 2.5, z_offset, sx=3, sy=4, sz=25, color="434343FF")
    # Крыша
    add_cube("Train_Roof", x_offset, 4.5, z_offset, sx=3.2, sy=0.2, sz=25, color="3F3F3FFF")
    # Окна
    for z_win in range(-10, 11, 2):
        add_quad("Train_Window", x_offset + 1.51, 3.0, z_offset + z_win, ry=90, sx=1, sy=1, color="A0A0A0FF", flags=2)
    # Колеса
    for z_wheel in range(-10, 11, 5):
        add_cube("Wheel", x_offset - 1.5, 0.8, z_offset + z_wheel, sx=0.5, sy=1, sz=1, color="1F1F1FFF")
        add_cube("Wheel", x_offset + 1.5, 0.8, z_offset + z_wheel, sx=0.5, sy=1, sz=1, color="1F1F1FFF")

create_train(7.5, -20)
create_train(-7.5, 10)

# 6. Мусор, ящики и бочки (для атмосферы)
for _ in range(1500):
    x = random.uniform(-22, 22)
    z = random.uniform(-60, 60)
    y = 1.5 if (abs(x) > 5 and abs(x) < 25) else 0.5
    rot_y = random.uniform(0, 360)
    scale_x = random.uniform(0.5, 1.5)
    scale_y = random.uniform(0.5, 1.5)
    scale_z = random.uniform(0.5, 1.5)
    color = random.choice(["434343FF", "595959FF", "717171FF"])
    add_cube("Debris", x, y, z, ry=rot_y, sx=scale_x, sy=scale_y, sz=scale_z, color=color)

# 7. Трубы и провода под потолком
for x_pos in range(-20, 21, 5):
    add_cube("Pipe", x_pos, 12, 0, sx=0.5, sy=0.5, sz=100, color="717171FF")
    
for z_pos in range(-50, 51, 15):
    add_cube("Wire", 0, 15, z_pos, sx=50, sy=0.1, sz=0.1, color="1F1F1FFF")

# 8. Освещение (лампы и источники света)
for z_pos in range(-40, 41, 10):
    # Лампы под потолком
    add_quad("Light_Quad", 0, 20, z_pos, rx=90, sx=4, sy=4, color="F8BF6DFF", flags=3)
    add_light("LightSource", 0, 19, z_pos, color="F8BF6DFF", intensity=4.0, r=15.0)
    
    # Лампы на колоннах
    add_light("LightSource_Col", -24, 8, z_pos, color="DB9D43FF", intensity=2.0, r=8.0)
    add_light("LightSource_Col", 24, 8, z_pos, color="DB9D43FF", intensity=2.0, r=8.0)

# 9. Туман и атмосфера
add_quad("Fog_Plane", 0, 10, -60, sx=100, sy=40, color="3F3F3FFF", flags=2)

# --- СОХРАНЕНИЕ JSON ---
result = {
    "RootObjectId": RootObjectId,
    "Blocks": Blocks
}

with open("map.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"Карта успешно сгенерирована! Объектов: {len(Blocks)}")
