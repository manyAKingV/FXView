<template>
  <FitScreen mode="full" :height="1080" :width="1920">
    <div class="container">
      <div class="container-title">AI全景图</div>
      <div class="container-content">
        <div
          class="container-content-box"
          v-for="(item, index) in landscapeData"
          :key="index"
        >
          <ContentShow :showData="item" :listIndex="index" />
        </div>
      </div>
    </div>
  </FitScreen>
</template>
<script setup>
import { ref, onMounted } from "vue";
import FitScreen from "@fit-screen/vue";
import jsyaml from "js-yaml";
import ContentShow from "../components/ContentShow.vue";

const landscapeData = ref([]);
onMounted(async () => {
  const response = await fetch("/static/data.yaml");
  const yamlText = await response.text();
  const parsedData = jsyaml.load(yamlText);
  landscapeData.value = parsedData?.landscape;
});
</script>
<style scoped>
.container {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}
.firm-log {
  background: #e5fbf7;
  border-radius: 8px;
  padding: 12px;
}
.firm-list {
  min-height: 200px;
  border: 1px dotted #63be90;
  border-radius: 8px;
}
.container-title {
  width: 100%;
  height: 80px;
  flex-shrink: 0;
  background: #fff;
  box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, 0.05);
  color: #000;
  font-family: "PingFang HK";
  font-size: 20px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 2px;
  padding-left: 42px;
  display: flex;
  align-items: center;
}
.container-content {
  width: 100%;
  padding: 20px;
}
.container-content-box {
  margin-bottom: 20px;
}
</style>
