<template>
  <v-container class="fill-height">
    <v-responsive
      class="align-center fill-height mx-auto text-center"
      max-width="1000px"
    >
      <h1>CLASIFICADOR DE RESIDUOS</h1>
      <v-row justify="center">
        <v-col cols="5">
          <v-card
            class="pa-6"
            width="400px"
            height="500px"
            variant="elevated"
            color="#F7F7FF"
          >
            <v-card-title class="text-center"
              >Imagen a clasificar:</v-card-title
            >
            <v-file-input
              v-model="filePath"
              label="Seleccionar"
              variant="outlined"
              @change="handleFileUpload"
            ></v-file-input>
            <v-row justify="center">
              <v-btn
                color="primary"
                @click="clasificarResiduo"
                :disabled="!selectedImage"
                class="mr-4"
                >Clasificar</v-btn
              >
              <!-- Botón para limpiar campos -->
              <v-btn color="error" @click="limpiarCampos">Limpiar</v-btn>
            </v-row>
          </v-card>
        </v-col>
        <v-col cols="7">
          <v-card
            class="pa-6"
            width="600px"
            height="500px"
            variant="elevated"
            color="#F7F7FF"
          >
            <v-card-title class="text-center"
              >Visualización de la imagen:</v-card-title
            >
            <v-img
              :src="imageSegmentada"
              max-width="100%"
              max-height="90%"
            ></v-img>
          </v-card>
        </v-col>
      </v-row>
    </v-responsive>
  </v-container>
</template>

<script setup>
import { ref } from "vue";

const selectedImage = ref("");
const imageSegmentada = ref("");
const filePath = ref([]);
const tipoArchivo = ref("Imagen");

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
  formData.append(
    "image",
    await fetch(selectedImage.value).then((res) => res.blob())
  );

  try {
    const response = await fetch("http://127.0.0.1:5000/segment", {
      method: "POST",
      body: formData,
    });
    console.log(response);

    if (!response.ok) {
      throw new Error("Error al clasificar la imagen");
    }

    const data = await response.json();
    console.log("Se clasificó la imagen correctamente");
    console.log(data["segmentacion"]);
    await obtenerImagenSegmentada(data["segmentacion"]);
  } catch (error) {
    console.error(error);
    imageSegmentada.value = "Error al clasificar la imagen";
  }
};

const obtenerImagenSegmentada = async (url) => {
  try {
    const response = await fetch("http://127.0.0.1:5000/segmented-image");
    if (!response.ok) {
      throw new Error("Error al obtener la imagen segmentada");
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
  filePath.value = [];
  tipoArchivo.value = "Imagen";

};
</script>

<style scoped>

</style>
