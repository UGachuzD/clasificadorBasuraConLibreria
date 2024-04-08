<template>
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height mx-auto" max-width="1000">
      <v-card color="white" class="elevation-12" max-width="1000" height="500" outlined>
        <!-- Cambia el color de fondo a blanco -->
        <v-card-title class="text-center">CLASIFICADOR DE RESIDUOS</v-card-title>
        <v-container>
          <v-row justify="center"> <!-- Centra las columnas horizontalmente -->
            <v-col cols="5">
              <v-card class="pa-6" max-width="600" height="400" outlined>
                <v-card-title class="text-center">Imagen a clasificar:</v-card-title>
                <v-file-input label="Seleccionar" variant="outlined" @change="handleFileUpload"></v-file-input>
                <!-- Campo para mostrar información -->
                <v-btn color="primary" @click="clasificarResiduo" :disabled="!selectedImage">Clasificar</v-btn>
                <!-- Botón para limpiar campos -->
                <v-btn color="error" @click="limpiarCampos">Limpiar</v-btn>
              </v-card>
            </v-col>
            <v-col cols="7">
              <v-card class="pa-6" max-width="600" height="400" outlined>
                <v-card-title class="text-center">Visualización de la imagen:</v-card-title>
                <v-img :src="imageSegmentada" max-width="100%" max-height="90%"></v-img>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-responsive>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';

const selectedImage = ref("");
const imageSegmentada = ref("");

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = (e) => {
    selectedImage.value = e.target.result;

  };

  reader.readAsDataURL(file);
};

const clasificarResiduo = async () => {
  const formData = new FormData();
  formData.append('image', await fetch(selectedImage.value).then(res => res.blob()));

  try {
    const response = await fetch('http://127.0.0.1:5000/segment', {
      method: 'POST',
      body: formData
    });
    console.log(response);

    if (!response.ok) {
      throw new Error('Error al clasificar la imagen');
    }

    const data = await response.json();
    console.log("Se clasificó la imagen correctamente");
    console.log(data['segmentacion']);

    // Obtener la imagen segmentada
    await obtenerImagenSegmentada(data['segmentacion']);
  } catch (error) {
    console.error(error);
    imageSegmentada.value = "Error al clasificar la imagen";
  }
};

const obtenerImagenSegmentada = async (url) => {
  try {
    const response = await fetch('http://127.0.0.1:5000/segmented-image');
    if (!response.ok) {
      throw new Error('Error al obtener la imagen segmentada');
    }
    const imageUrl = URL.createObjectURL(await response.blob());
    imageSegmentada.value = imageUrl;
  } catch (error) {
    console.error(error);
    imageSegmentada.value = ""; 
  }
};

const limpiarCampos = () => {
  selectedImage.value = "";
  imageSegmentada.value = "";
};
</script>

<style scoped>

</style>
