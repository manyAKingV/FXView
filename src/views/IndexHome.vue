<template>
  <FitScreen mode="full" :height="1080" :width="1920">
    <div class="container">
      <div class="firm-log">
        <div class="firm-title">{{ data.landscape.category.name }}</div>
        <div class="firm-list-container">
          <div
            class="firm-list"
            v-for="(item, index) in showData"
            :key="index"
            :class="{
              'firm-list-one': index === 0,
              'firm-list-two': index === 1,
              'firm-list-three': index === 2,
              'firm-list-four': index === 3,
              'firm-list-five': index === 4,
            }"
          >
            <div class="firm-type">{{ item.name }}</div>
            <div class="firm-list-logo">
              <img
                :src="require(`@/assets/logos/${it.logo}`)"
                class="firm-list-logo-item-img"
                v-for="(it, ind) in item.items"
                :key="ind"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </FitScreen>
</template>
<script setup>
import { ref } from "vue";
import FitScreen from "@fit-screen/vue";
import data from "../mock/data.json";
const showData = ref(data.landscape.category.subcategories);
</script>
<style scoped>
.container {
  width: 100%;
  height: 100%;
  padding: 30px;
}
.firm-log {
  width: 100%;
  height: 100%;
  background: #e5fbf7;
  border-radius: 8px;
  padding: 12px;
}
.firm-list {
  min-height: 200px;
  border: 1px dotted #63be90;
  border-radius: 8px;
  display: flex;
  margin-bottom: 8px;
  padding: 6px 4px;
}
.firm-type {
  font-size: 12px;
  color: #4a4849;
  width: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.firm-list-logo {
  width: calc(100% - 80px);
  background: #ffffff;
  border-radius: 8px;
}
.firm-list-logo-item {
  padding: 0 10px;
}
.firm-list-logo-item-img {
  max-width: 120px;
  height: 100px;
  object-fit: contain;
  padding: 0 10px;
}
.firm-list-logo-item-text {
  font-size: 10px;
  color: #423f3f;
}
.firm-title {
  color: #63be90;
  margin: 12px 6px;
}
.firm-list-one {
  width: 50%;
}
.firm-list-two {
  width: 25%;
}
.firm-list-three {
  width: 25%;
}
.firm-list-four {
  width: 55%;
}
.firm-list-five {
  width: 45%;
}
.firm-list-container {
  display: flex;
  flex-wrap: wrap;
}
</style>
