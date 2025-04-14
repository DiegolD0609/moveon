<template>
  <!--Se tomo una imagen previamente optimizada para mejor tiempo de respuesta guardada en assets/images-->
  <div class="landing-container">
    <div class="image-section">
      <img src="@/assets/images/fondo_landingpage-min.jpg" alt="Motorbike" class="hero-image">
    </div>
    
    <div class="content-section">
      <div class="text-content">
        <h1>Bienvenido a Move On</h1>
        <p>Encuentra la sucursal más cercana para tu motocicleta</p>
        <button @click="navigateToForm">Inicia</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateToForm = () => {
  router.push('/form')
}
</script>

<style scoped>
.landing-container {
  display: flex;
  height: 100vh;
}

.image-section {
  flex: 70%;
  overflow: hidden;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.content-section {
  flex:30%;
  background-color: #2c3e50; /* Dark grey-blue */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.text-content {
  max-width: 475px;
  color: white;
  text-align: center;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

button {
  padding: 0.75rem 1.5rem;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s;
}

button:hover {
  background: #3aa876;
}
</style>