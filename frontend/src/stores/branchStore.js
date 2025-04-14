import { defineStore } from 'pinia'
import api from '@/api/axios'  

export const useBranchStore = defineStore('branch', {
  state: () => ({
    customerData: null,
    nearestBranch: null,
    motorbikes: [],
    isLoading: false
  }),
  actions: {
    async fetchMotorbikes() {
      try {
        const response = await api.get('/motorbikes')  
        this.motorbikes = response.data
      } catch (error) {
        console.error('Error fetching motorbikes:', error)
        throw error  
      }
    },
    async submitCustomer(data) {
        this.isLoading = true  
      try {
        const response = await api.post('/branches/nearest', data)
        this.customerData = data
        this.nearestBranch = response.data.nearest_branch
        this.distance = response.data.distance_km  
        return true
      } catch (error) {
        console.error('Error submitting customer:', error)
        throw error
      } finally {
        this.isLoading = false  
      }
    }
  }
})
