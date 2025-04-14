<template>
  <!--Creacion del formulario-->
  <div class="form-wrapper">
    <div class="form-container">
      <h2>Completa los datos siguientes</h2>
      <form @submit.prevent="handleSubmit">
        <!--Cada inciso es necesario para hacer la busqueda-->
        <div class="form-group">
          <label>Nombre Completo</label>
          <input v-model="formData.name" required>
        </div>
        
        <div class="form-group">
          <label>Email</label>
          <input v-model="formData.email" type="email" required>
        </div>

        <h3 class="section-title">Datos de tu domicilio</h3>
        
        <div class="form-group">
          <label>Calle</label>
          <input v-model="formData.street" required>
        </div>
        
        <div class="form-group">
          <label>Número</label>
          <input v-model="formData.number">
        </div>
        
        <div class="form-group">
          <label>Colonia</label>
          <input v-model="formData.neighborhood" required>
        </div>
        
        <div class="form-group">
          <label>Ciudad</label>
          <input v-model="formData.city" required>
        </div>
        <!--Se tomo la decision de hacer un dropdown para mostrar los estados-->
        <div class="form-group">
          <label>Estado</label>
          <select v-model="formData.state" required>
            <option disabled value="">Selecciona un estado</option>
            <option v-for="state in states" :key="state" :value="state">
              {{ state }}
            </option>
          </select>
        </div>
        
        <div class="form-group">
          <label>País</label>
          <input v-model="formData.country" required>
        </div>
        
        <div class="form-group">
          <label>Código postal</label>
          <input v-model="formData.zipcode">
        </div>
        <!--El frontend toma del backend las motos previamente guardadas "motorbikes" es el key item-->
        <div class="form-group">
          <label>Motocicleta preferida</label>
          <select v-model="formData.motorbike_id" required>
            <option v-for="bike in branchStore.motorbikes" :key="bike.id" :value="bike.id">
              {{ bike.brand }} {{ bike.model }} {{ bike.year }} {{ bike.color }}
            </option> 
          </select>
        </div>
        <!--Se genero una pantalla de carga para esperar la respuesta del API-->
        <button type="submit" :disabled="branchStore.isLoading">
          {{ branchStore.isLoading ? 'Buscando...' : 'Encontrar sucursal más cercana' }}
        </button>
      </form>
      <Spinner :isLoading="branchStore.isLoading" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBranchStore } from '@/stores/branchStore'
import Spinner from '@/components/Spinner.vue'

const router = useRouter()
const branchStore = useBranchStore()

const formData = ref({
  name: '',
  email: '',
  street: '',
  number: '',
  neighborhood: '',
  city: '',
  state: '',
  country: '',
  zipcode: '',
  motorbike_id: null
})

const states = ref([
  'Aguascalientes', 'Baja California', 'Baja California Sur',
  'Campeche', 'Chiapas', 'Chihuahua', 'Coahuila', 'Colima',
  'Ciudad de México', 'Durango', 'Guanajuato', 'Guerrero',
  'Hidalgo', 'Jalisco', 'México', 'Michoacán', 'Morelos',
  'Nayarit', 'Nuevo León', 'Oaxaca', 'Puebla', 'Querétaro',
  'Quintana Roo', 'San Luis Potosí', 'Sinaloa', 'Sonora',
  'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz', 'Yucatán',
  'Zacatecas'
]);

onMounted(async () => {
  await branchStore.fetchMotorbikes()
})

const handleSubmit = async () => {
  try {
    await branchStore.submitCustomer(formData.value)
    router.push('/results')
  } catch (error) {
    alert('Error al enviar el formulario. Por favor intenta nuevamente.')
  }
}
</script>

<style scoped>
.form-wrapper {
  background-color: #2d3748;
  min-height: 100vh;
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-container {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 800px;
}

h2 {
  color: #2d3748;
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  font-weight: 700;
  text-align: center;
}

.section-title {
  color: #4a5568;
  font-size: 1.2rem;
  margin: 1.5rem 0 1rem;
  font-weight: 600;
}

.form-group {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #4a5568;
  font-weight: 500;
  font-size: 0.95rem;
}

input, select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: #f8fafc;
}

input:focus, select:focus {
  border-color: #4299e1;
  outline: none;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
  background-color: #ffffff;
}

button {
  margin-top: 1.5rem;
  padding: 0.875rem 1.75rem;
  background: #4299e1;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  width: 100%;
  transition: all 0.3s ease;
}

button:hover {
  background: #3182ce;
}

button:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}
</style>