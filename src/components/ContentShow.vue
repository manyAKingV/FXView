<template>
  <div
    class="container-content-box-title"
    :style="{
      backgroundColor: currentTitleColor,
    }"
  >
    {{ showData?.name }}
  </div>
  <div
    class="container-content-box-show"
    :style="{
      backgroundColor: currentContentColor,
    }"
  >
    <div
      class="container-content-box-show-item"
      :class="{
        'container-content-box-show-item-last': index % 4 === 0 && index != 0,
      }"
      v-for="(item, index) in showData?.subcategories"
      :key="index"
    >
      <div class="container-content-box-show-item-title">
        {{ item.name }}
      </div>
      <div class="container-content-box-show-item-content">
        <div
          class="img-show"
          v-for="(it, ind) in item.items"
          :key="ind"
          @click="showCompanyInfo(it, $event)"
          :class="{
            'search-img':
              searchData?.findIndex((city) => city.name === it.name) !== -1
                ? true
                : false,
          }"
        >
          <img :src="require(`@/assets/logos/${it.logo}`)" class="img-item" />
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, defineProps, watch, defineExpose, defineEmits } from "vue";
const showDetailInfo = ref(false);
const currentTitleColor = ref(null);
const currentContentColor = ref(null);
const isShowDialog = ref(false);
const dialogTop = ref(0);
const dialogLeft = ref(0);
const props = defineProps({
  showData: {
    type: Array,
    default: () => [],
  },
  listIndex: {
    type: Number,
    default: 0,
  },
  searchData: {
    type: Array,
    default: () => [],
  },
});
const bgTitleColor = ["#FE8FB9", "#A6BBE6", "#A6E6DB", "#AEA6E6"];
const bgContentColor = ["#FFF0F6", "#E2E8F3", "#EAF4F2", "#F6F5FF"];
const emit = defineEmits(["handleClick"]);
const showCompanyInfo = (it, event) => {
  isShowDialog.value = true;
  showDetailInfo.value = it;
  const viewportWidth = window.innerWidth;
  dialogTop.value =
    event.currentTarget.getBoundingClientRect().top + window.screenY;
  const target = event.currentTarget;
  const rect = target.getBoundingClientRect();
  if (rect.left + 360 > viewportWidth - 20) {
    // 右侧空间不足，改到左侧
    dialogLeft.value = rect.left - 340;
  } else {
    dialogLeft.value = rect.left + 100;
  }
  emit(
    "handleClick",
    isShowDialog.value,
    it,
    dialogTop.value,
    dialogLeft.value
  );
};
watch(
  () => props.listIndex,
  () => {
    currentTitleColor.value = bgTitleColor[props.listIndex];
    currentContentColor.value = bgContentColor[props.listIndex];
  },
  {
    immediate: true,
  }
);
defineExpose({
  showDetailInfo,
  isShowDialog,
});
</script>
<style scoped>
.container-content-box-title {
  width: 100%;
  height: 60px;
  flex-shrink: 0;
  padding-left: 40px;
  display: flex;
  align-items: center;
  color: #000;
  text-align: center;
  font-family: "PingFang HK";
  font-size: 20px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
  letter-spacing: 2px;
}
.container-content-box-show {
  padding: 20px;
  min-height: 200px;
  display: flex;
  flex-wrap: wrap;
}
.container-content-box-show-item {
  margin-right: 6px;
  margin-top: 10px;
  width: 362px;
  box-sizing: border-box;
}
.container-content-box-show-item-last {
  margin-right: 0px;
}
.container-content-box-show-item-title {
  height: 40px;
  flex-shrink: 0;
  border: 1px solid rgba(0, 0, 0, 0.05);
  background: #fff;
  color: #000;
  font-family: "PingFang HK";
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 1.4px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.container-content-box-show-item-content {
  padding: 20px;
  background: #fff;
  height: 164px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(3, 48px);
  border: 1px solid rgba(0, 0, 0, 0.05);
  position: relative;
}
.img-show {
  width: 80px;
  height: 48px;
  padding: 10px;
}
.img-show:hover {
  cursor: pointer;
}
.img-show:hover .img-item {
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: #fff;
  box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, 0.05);
}
.img-item {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.img-item:hover {
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: #fff;
  box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, 0.05);
}
.search-img {
  border-radius: 4px;
  border: 1px solid #d91b64;
  background: #fff;
  box-shadow: 0px 4px 8px 0px #d91b64;
}
</style>
