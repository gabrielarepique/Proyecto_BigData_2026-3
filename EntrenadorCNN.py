import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# ==============================================================================
# CONFIGURACIÓN DE RUTAS (Modificado para tu usuario real EQUIPO)
# ==============================================================================
BASE_DIR = # Ruta base de tu proyecto + \Data'
DATA_DIR = os.path.join(BASE_DIR, 'ObjetoV2', 'Data')

# Dimensiones de las imágenes para MobileNetV2
IMG_WIDTH, IMG_HEIGHT = 224, 224
BATCH_SIZE = 32
EPOCHS_TOP = 15       # Épocas para entrenar solo las capas nuevas
EPOCHS_FINE = 15      # Épocas para el ajuste fino

# ==============================================================================
# 1. DATA AUGMENTATION (Opción 1: Agresivo para romper el sesgo del fondo)
# ==============================================================================
print("⏳ Configurando generadores de datos con Data Augmentation...")

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=25,          # Rota las imágenes para cambiar la perspectiva del termo
    width_shift_range=0.2,       # Desplazamientos horizontales
    height_shift_range=0.2,      # Desplazamientos verticales
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    # --- Parámetros clave para el termo rosa y las luces del laboratorio ---
    brightness_range=[0.5, 1.5], # Simula sombras y destellos fuertes de luz
    channel_shift_range=40.0,    # Altera los tonos de color para forzar a la IA a buscar formas
    validation_split=0.2         # 20% para validación
)

# El generador de validación SOLO escala, no debe alterar las imágenes de prueba
val_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

# Cargar datos de entrenamiento
train_generator = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

# Cargar datos de validación
validation_generator = val_datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

num_classes = train_generator.num_classes
print(f"✅ Clases detectadas: {list(train_generator.class_indices.keys())}")

# ==============================================================================
# 2. CONSTRUCCIÓN DEL MODELO (Transfer Learning con MobileNetV2)
# ==============================================================================
print("⏳ Cargando arquitectura base MobileNetV2...")
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(IMG_WIDTH, IMG_HEIGHT, 3))

# Inicialmente congelamos la base para entrenar las capas superiores
base_model.trainable = False

# Añadimos nuestras capas personalizadas
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)  # Ayuda a evitar que se sature con el fondo
predictions = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# ==============================================================================
# 3. ENTRENAMIENTO - FASE 1: CAPAS SUPERIORES
# ==============================================================================
print("⚙️ Compilando Fase 1...")
model.compile(optimizer=Adam(learning_rate=1e-4), loss='categorical_crossentropy', metrics=['accuracy'])

# Guardará el mejor modelo intermedio en tu carpeta actual en formato .h5
checkpoint_path = # Ruta base de tu proyecto + \best_model.h5'
checkpoint = ModelCheckpoint(
    filepath=os.path.join(BASE_DIR, 'best_model.h5'),
    monitor='val_loss',
    save_best_only=True
)
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

print("\n🚀 Iniciando Fase 1: Entrenando capas superiores...")
model.fit(
    train_generator,
    epochs=EPOCHS_TOP,
    validation_data=validation_generator,
    callbacks=[checkpoint, early_stopping]
)

# ==============================================================================
# 4. ENTRENAMIENTO - FASE 2: FINE-TUNING (Ajuste Fino)
# ==============================================================================
print("\n🔓 Descongelando capas altas de MobileNetV2 para adaptarlas al termo...")
base_model.trainable = True

# Congelamos las primeras 100 capas, dejamos libres las últimas para ajustar detalles finos
for layer in base_model.layers[:100]:
    layer.trainable = False

# Compilamos con un Learning Rate extremadamente bajo para no dañar los pesos
model.compile(optimizer=Adam(learning_rate=1e-5), loss='categorical_crossentropy', metrics=['accuracy'])

print("🚀 Iniciando Fase 2: Fine-Tuning de precisión...")
model.fit(
    train_generator,
    epochs=EPOCHS_FINE,
    validation_data=validation_generator,
    callbacks=[checkpoint, early_stopping]
)

# ==============================================================================
# 5. GUARDAR MODELO FINAL (Corregido sin errores de permisos)
# ==============================================================================
modelo_final_path =# Ruta base de tu proyecto + \modeloCNN.h5'
print("\n⏳ Guardando el modelo final procesado...")
model.save(modelo_final_path)
print(f"✅ ¡Excelente! Proceso finalizado. Modelo guardado en: {modelo_final_path}")