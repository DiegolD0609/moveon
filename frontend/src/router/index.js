import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/views/LandingPage.vue'
import FormPage from '@/views/FormPage.vue'
import ResultsPage from '@/views/ResultsPage.vue'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/form', component: FormPage },
  { path: '/results', component: ResultsPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router