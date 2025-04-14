<template>
  <div class="results-wrapper">
    <div class="results-container">
      <h2 class="results-title">Tu sucursal más cercana</h2>

      <!--Se toma el nombre, direccion y distancia de las sucursales por medio de la API-->
      <div v-if="branchStore.nearestBranch" class="branch-card">
        <h3 class="branch-name">{{ branchStore.nearestBranch.name }}</h3>
        <p class="branch-address">{{ branchStore.nearestBranch.address }}</p>
        <p class="distance">Distancia: {{ branchStore.distance }} km</p>
        
        <!--Mapa con la ayuda de google maps API-->
        <div class="map-container">
          <MapDisplay 
            :lat="branchStore.nearestBranch.coordinates.latitude"
            :lng="branchStore.nearestBranch.coordinates.longitude"
          />
        </div>
        
        <button @click="goHome" class="action-button">
          Nueva búsqueda
        </button>
      </div>
      
      <div v-else class="no-results">
        <p>No se ha encontrado una sucursal. Por favor, intenta de nuevo.</p>
        <button @click="goBack" class="action-button">
          Regresar al formulario
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useBranchStore } from '@/stores/branchStore'
import MapDisplay from '@/components/MapDisplay.vue';

const router = useRouter()
const branchStore = useBranchStore()

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.push('/form')
}
</script>

<style scoped>
.results-wrapper {
  background-color: #2d3748; /* Dark gray background */
  min-height: 100vh;
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.results-container {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 800px;
}

.results-title {
  color: #2d3748;
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  font-weight: 700;
  text-align: center;
}

.branch-card {
  background: #f8fafc; /* Lighter background for the card */
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
  border: 1px solid #e2e8f0;
}

.branch-name {
  color: #2d3748;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.branch-address {
  color: #4a5568;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.distance {
  color: #2d3748;
  font-weight: 500;
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

.map-container {
  height: 300px;
  background: #e2e8f0; /* Matching light gray */
  margin: 1.5rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  border: 1px solid #cbd5e0;
}

.no-results {
  padding: 1.5rem;
  text-align: center;
}

.no-results p {
  color: #4a5568;
  margin-bottom: 1.5rem;
}

.action-button {
  padding: 0.875rem 1.75rem;
  background: #4299e1; /* Matching blue from form */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  width: 100%;
  max-width: 300px;
  margin: 1.5rem auto 0;
  transition: all 0.3s ease;
}

.action-button:hover {
  background: #3182ce; /* Darker blue on hover */
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .results-container {
    padding: 1.5rem;
  }
  
  .branch-name {
    font-size: 1.3rem;
  }
  
  .action-button {
    max-width: 100%;
  }
}
</style>