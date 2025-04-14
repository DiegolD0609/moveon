import { defineStore } from 'pinia'
import api from '@/api/axios'  // Changed from direct axios import

export const useBranchStore = defineStore('branch', {
  state: () => ({
    customerData: null,
    nearestBranch: null,
    motorbikes: []
  }),
  actions: {
    async fetchMotorbikes() {
      try {
        const response = await api.get('/motorbikes')  // Using configured api
        this.motorbikes = response.data
      } catch (error) {
        console.error('Error fetching motorbikes:', error)
        throw error  // Re-throw for component handling
      }
    },
    async submitCustomer(data) {
        this.isLoading = true  // Set loading state
      try {
        const response = await api.post('/branches/nearest', data)
        this.customerData = data
        this.nearestBranch = response.data.nearest_branch
        this.distance = response.data.distance_km  // Store distance separately
        return true
      } catch (error) {
        console.error('Error submitting customer:', error)
        throw error  // Re-throw for form component
      } finally {
        this.isLoading = false  // Reset loading state
      }
    }
  }
})
