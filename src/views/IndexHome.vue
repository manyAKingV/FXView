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
          <ContentShow
            :showData="item"
            :listIndex="index"
            @handleClick="handleClick"
            ref="contentShowRef"
          />
        </div>
      </div>
    </div>
    <div
      class="img-detail"
      v-if="isShowDialog"
      :style="{ top: dialogTop + 'px', left: dialogLeft + 'px' }"
    >
      <div class="img-detail-title">
        <img
          class="img-detail-title-img"
          :src="require(`@/assets/logos/${showDetailInfo?.logo}`)"
        />
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="28"
          height="28"
          viewBox="0 0 28 28"
          fill="none"
          class="img-close"
          @click="handleClose"
        >
          <path
            d="M7.63635 7.63635L20.3636 20.3636"
            stroke="#666666"
            stroke-width="2"
          />
          <path
            d="M20.3636 7.63635L7.63635 20.3636"
            stroke="#666666"
            stroke-width="2"
          />
        </svg>
      </div>
      <div class="img-detail-title-text">
        {{ showDetailInfo?.name }}
      </div>
      <div class="img-detail-title-country">中国</div>
      <div class="img-detail-title-desc">
        {{ showDetailInfo?.description }}
      </div>
      <div class="img-detail-bottom-desc">
        <div class="img-detail-bottom-desc-one">
          创立于<span class="img-detail-bottom-desc-span">{{
            handleTime()
          }}</span>
        </div>
        <div class="img-detail-bottom-desc-one">
          文本展示<span class="img-detail-bottom-desc-span">xxx</span>
        </div>
        <div class="img-detail-bottom-desc-web" @click="pathStamp">
          <span class="web-text">网站</span>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
          >
            <path d="M15 9L14.9998 5H10.9998" stroke="black" />
            <path d="M15.091 5L11.2046 8.88642" stroke="black" />
            <path d="M8.33333 5H5V15H15V11.6667" stroke="black" />
          </svg>
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
const showDetailInfo = ref(null);
const contentShowRef = ref(null);
const isShowDialog = ref(false);
const dialogTop = ref(0);
const dialogLeft = ref(0);
onMounted(async () => {
  const response = await fetch("/static/data.yaml");
  const yamlText = await response.text();
  const parsedData = jsyaml.load(yamlText);
  landscapeData.value = parsedData?.landscape;
});
const handleTime = () => {
  return showDetailInfo.value?.description?.split(" ")?.[1]?.split("-")?.[0];
};
const handleClick = (props, it, clientY, clientX) => {
  isShowDialog.value = props;
  showDetailInfo.value = it;
  dialogTop.value = clientY;
  dialogLeft.value = clientX;
};
const handleClose = () => {
  isShowDialog.value = false;
};
const pathStamp = () => {
  window.location.href = showDetailInfo.value?.homepage_url;
};
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
.img-detail {
  width: 340px;
  height: 340px;
  border-radius: 4px;
  border: 1px solid #c2ccd9;
  background: #fff;
  position: fixed;
  z-index: 99;
  padding: 20px;
}
.img-detail-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.img-detail-title-img {
  width: 120px;
  height: 40px;
  object-fit: cover;
}
.img-detail-title-text {
  margin-top: 20px;
  margin-bottom: 10px;
  color: #000;
  font-family: "PingFang HK";
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 1.4px;
}
.img-detail-title-country {
  color: #000;
  font-family: "PingFang HK";
  font-size: 12px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 1.2px;
  opacity: 0.5;
}
.img-detail-title-desc {
  margin: 20px 0;
  color: #000;
  font-family: "PingFang HK";
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 1.4px;
}
.img-detail-bottom-desc {
  display: flex;
}
.img-detail-bottom-desc-one {
  color: rgba(0, 0, 0, 0.5);
  font-family: "PingFang HK";
  font-size: 12px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 1.2px;
  margin-right: 20px;
}
.img-detail-bottom-desc-span {
  color: #000;
  margin-left: 8px;
}
.img-detail-bottom-desc-web {
  color: #000;
  font-family: Avenir;
  font-size: 12px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 1.2px;
  text-decoration-line: underline;
  text-decoration-style: solid;
  text-decoration-skip-ink: auto;
  text-decoration-thickness: auto;
  text-underline-offset: auto;
  text-underline-position: from-font;
  display: flex;
}
.img-close:hover {
  cursor: pointer;
}
.img-detail-bottom-desc-web:hover {
  cursor: pointer;
  color: #d91b64;
  text-decoration-color: #d91b64;
}
</style>
