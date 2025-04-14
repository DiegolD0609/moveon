<template>
  <!-- Este componente se encarga de mostrar un spinner de carga cuando isLoading es verdadero -->
    <div class="spinner-overlay" v-if="isLoading">
        <div class="spinner"></div>
        <p> Buscando la sucursal mas cercana...</p>
    </div>
</template>

<script>
export default{
    props: {
        isLoading:Boolean
    }
}
</script>
<style scoped>
.spinner-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: #09f;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>