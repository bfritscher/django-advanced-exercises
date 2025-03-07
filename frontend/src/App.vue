<template>
  <div class="app-container">
    <h1 class="app-title">Orders</h1>
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    <OrderEntry v-for="order in orders" :key="order.id" :order="order" />
  </div>
</template>

<script>
import axios from "axios"
import OrderEntry from "@/components/OrderEntry.vue"
import { API_URL } from "@/config"

export default {
  name: "App",
  components: {
    OrderEntry
  },
  data() {
    return {
      orders: [],
      error: null
    }
  },
  mounted() {
    this.getOrders()
  },
  methods: {
    async getOrders() {
      try {
        this.error = null
        const response = await axios.get(`${API_URL}/api/orders/`)
        this.orders = response.data
      } catch (err) {
        this.error = `Failed to load orders: ${err.message}`
      }
    }
  }
}
</script>

<style scoped>
.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.app-title {
  color: #2c3e50;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 20px;
  border: 1px solid #f5c6cb;
}
</style>
