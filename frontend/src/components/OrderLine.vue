<template>
  <div class="orderline">
    <div class="orderline-id">#{{ orderline.id }}</div>
    <div class="orderline-product">{{ orderline.product.name }}</div>
    <div class="orderline-details">
      <span>${{ orderline.product.price }}</span>
      <span>× {{ orderline.quantity }}</span>
    </div>
    <div class="orderline-total">${{ orderline.total }}</div>
  </div>
</template>

<script>
export default {
  name: "OrderLine",
  props: {
    orderline: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.orderline {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  margin: 5px 0;
  background-color: #ffffff;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.orderline-id {
  color: #7f8c8d;
  font-size: 0.9em;
  width: 10%;
}

.orderline-product {
  font-weight: 600;
  color: #34495e;
  width: 40%;
}

.orderline-details {
  width: 30%;
  display: flex;
  gap: 10px;
}

.orderline-total {
  font-weight: bold;
  width: 20%;
  text-align: right;
}
</style>
