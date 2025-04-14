<template>
    <div class="map-container">
      <div ref="mapRef" class="map"></div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { Loader } from '@googlemaps/js-api-loader';
  
  const props = defineProps({
    lat: {
      type: Number,
      required: true,
    },
    lng: {
      type: Number,
      required: true,
    },
  });
  
  const mapRef = ref(null);
  
  onMounted(async () => {
    const loader = new Loader({
      // se usa .env para guardar la API key
      // y no exponerla en el frontend
      apiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
      version: 'weekly',
    });
  
    try {
      await loader.load();
      const map = new google.maps.Map(mapRef.value, {
        center: { lat: props.lat, lng: props.lng },
        zoom: 15,
      });
  
      // Add a marker
      new google.maps.Marker({
        position: { lat: props.lat, lng: props.lng },
        map: map,
        title: 'Branch Location',
      });
    } catch (error) {
      console.error('Failed to load Google Maps:', error);
    }
  });
  </script>
  
  <style scoped>
  .map-container {
    height: 400px;
    width: 100%;
    margin-top: 20px;
  }
  
  .map {
    height: 100%;
    width: 100%;
    border-radius: 8px;
    border: 1px solid #ccc;
  }
  </style>