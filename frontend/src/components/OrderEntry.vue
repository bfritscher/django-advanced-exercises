<template>
  <div class="order-card">
    <div class="order-header">
      <span class="order-id">Order #{{ order.id }}</span>
      <span>Customer: {{ order.customer.username }}</span>
      <span class="order-total">Total: ${{ order.total }}</span>
    </div>
    <div class="order-lines">
      <OrderLine v-for="orderline in order.orderlines" :key="orderline.id" :orderline="orderline" />
    </div>
    <div class="order-actions">
      <button
        @click="confirmReceipt"
        class="confirm-btn"
        :disabled="isConfirmed || isConfirming"
        :class="{ confirmed: isConfirmed }"
      >
        {{ confirmButtonText }}
      </button>
    </div>
  </div>
</template>

<script>
import OrderLine from "@/components/OrderLine.vue"
import axios from "axios"
import { API_URL } from "@/config"

export default {
  name: "OrderEntry",
  components: {
    OrderLine
  },
  props: {
    order: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      isConfirming: false,
      isConfirmed: this.order.customer_received || false
    }
  },
  computed: {
    confirmButtonText() {
      if (this.isConfirmed) return "Receipt Confirmed"
      if (this.isConfirming) return "Confirming..."
      return "Confirm Receipt"
    }
  },
  methods: {
    confirmReceipt() {
      if (this.isConfirmed || this.isConfirming) return

      this.isConfirming = true

      axios({
        method: "patch",
        url: `${API_URL}/api/orders/${this.order.id}/`,
        data: {
          customer_received: true
        }
      })
        .then(() => {
          this.isConfirmed = true
        })
        .catch((error) => {
          console.error("Error confirming receipt:", error)
          // Handle error - maybe show a notification to user
        })
        .finally(() => {
          this.isConfirming = false
        })
    }
  }
}
</script>

<style scoped>
.order-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.order-header {
  display: flex;
  justify-content: space-between;
  padding-bottom: 10px;
  border-bottom: 1px solid #dee2e6;
  margin-bottom: 10px;
}

.order-id {
  font-weight: bold;
  color: #3498db;
}

.order-total {
  font-weight: bold;
}

.order-lines {
  padding-left: 15px;
}

.order-actions {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
}

.confirm-btn {
  padding: 8px 16px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.confirm-btn:hover:not(:disabled) {
  background-color: #2980b9;
}

.confirm-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.confirm-btn.confirmed {
  background-color: #27ae60;
}
</style>
