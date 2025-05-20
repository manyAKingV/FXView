<template>
    <div id="app">
        <div class="title">
            <img src="@/assets/logo.png" alt="Company Logo" class="logo">
        </div>
        <a-layout-content class="content-container">
            <div class="tech-layer">
                <div class="section-title">应用层</div>
                <div class="ai-framework">
                    <div class="ai-frameworks">
                        <h3 class="sub-title">智能城市</h3>
                        <div class="grid-container">
                            <div class="grid-item" v-for="(company, index) in companies[0].list[0].list" :key="index" >
                                <img :src="require(`@scrapy/company/应用层/智慧城市/${company.name}/${company.name}.png`)" alt="智能城市" class="tech-img" @click="showCompanyInfo(company, $event)"/>
                            </div>
                        </div>
                    </div>
                    <div class="ai-frameworks">
                        <h3 class="sub-title">智能交通</h3>
                        <div class="grid-container">
                            <div class="grid-item" v-for="(img, index) in 6" :key="index">
                                <img :src="`/static/icon/pytorch.png`" alt="智能交通" class="tech-img" />
                            </div>
                        </div>
                    </div>
                    <div class="ai-frameworks">
                        <h3 class="sub-title">智慧物流</h3>
                        <div class="grid-container">
                            <div class="grid-item" v-for="(img, index) in 6" :key="index">
                                <img :src="`/static/icon/pytorch.png`" alt="智慧物流" class="tech-img" />
                            </div>
                        </div>
                    </div>
                    <div class="ai-frameworks">
                        <h3 class="sub-title">智慧物流2</h3>
                        <div class="grid-container">
                            <div class="grid-item" v-for="(img, index) in 6" :key="index">
                                <img :src="`/static/icon/pytorch.png`" alt="智慧物流2" class="tech-img" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="tech-layer">
                <div class="section-title">服务层</div>
                <div class="ai-frameworks">
                    <h3 class="sub-title">AI框架、工具和库</h3>
                    <div class="grid-container">
                        <div class="grid-item" v-for="(img, index) in 6" :key="index">
                            <img :src="`/static/icon/pytorch.png`" alt="AI工具" class="tech-img" />
                        </div>
                    </div>
                </div>
            </div>
            <div class="tech-layer">
                <div class="section-title">技术层</div>
                <div class="ai-frameworks">
                    <h3 class="sub-title">AI框架、工具和库</h3>
                    <div class="grid-container">
                        <div class="grid-item" v-for="(img, index) in 6" :key="index">
                            <img :src="`/static/icon/pytorch.png`" alt="AI工具" class="tech-img" />
                        </div>
                    </div>
                </div>
            </div>
            <div class="tech-layer">
                <div class="section-title">基础设施</div>
                <div class="ai-frameworks">
                    <h3 class="sub-title">AI框架、工具和库</h3>
                    <div class="grid-container">
                        <div class="grid-item" v-for="(img, index) in 6" :key="index">
                            <img :src="`/static/icon/pytorch.png`" alt="AI工具" class="tech-img" />
                        </div>
                    </div>
                </div>
            </div>
        </a-layout-content>

        <div class="popup" v-if="showPopup" :style="{ left: popupPosition.x + 'px', top: popupPosition.y + 'px' }"  >
            <button class="close-btn" @click.stop="closePopup">×</button>
            <h3>{{ popupData.name }}</h3>
            <p>{{ popupData.describe }}</p>
            <p>成立时间：{{ popupData.time }}</p>
            <p>网站：<a :href="popupData.website" target="_blank">{{ popupData.website }}</a></p>
        </div>

    </div>
</template>
  
<script>
import { exportToPDF } from "@/utils/pdfExport";

export default {
    data() {
        return {
            companies:[
                {
                    name: '应用层',
                    list:[
                        {
                            name: '智慧城市',
                            list: []
                        },
                        {
                            name: '智慧家居',
                            list: []
                        }
                    ]
                },
                // {
                //     name: '服务层',
                //     list:[
                //         {
                //             name: '智慧城市',
                //             list: []
                //         },
                //         {
                //             name: '智慧家居',
                //             list: []
                //         }
                //     ]
                // }
            ],
            showPopup: false,
            popupData: {},
            popupPosition: { x: 0, y: 0 }
        };
    },

    beforeMount(){

    },
    async mounted(){
        this.getCompany();
    },

    methods: {
        // 控制信息弹窗
        showCompanyInfo(company, event) {
            this.popupData = company;
            this.popupPosition = {
                x: event.clientX + 10, // 偏移一点避免遮挡鼠标
                y: event.clientY + 10
            };
            this.showPopup = !this.showPopup
        },
        closePopup(){
            this.showPopup = false
        },
        // 导出pdf功能
        async handleExport(){
            // 输入div的class 和 导出的名称
            exportToPDF('app','landscape.pdf')
        },
        // 获取公司信息
        getCompany() {
            const context = require.context('@/../scrapy/company/', true, /\.md$/);
            
            this.companies.forEach(item => {
                item.list.forEach(service => {
                    service.list = context.keys()
                        .filter(filePath => {
                            const parts = filePath.split('/');
                            return parts[1] === item.name && parts[2] === service.name;
                        })
                        .map(filePath => {
                            const mdModule = context(filePath);
                            const content = mdModule.default || mdModule;
                            return parseMD(content);
                        });
                });
            });
            console.log("结果",this.companies);
            
        }
        
    }
};
// 处理md文件
function parseMD(content) {
    if (!content) {
        return {
            name: '',
            describe: '',
            time: '',
            website: ''
        };
    }
    const cleanContent = content
        .replace(/<\/?p>/g, '')
        .replace(/<br\s*\/?>/g, '\n')
        .replace(/<\/?a[^>]*>/g, '');
    const patterns = {
        name: /名称:\s*([^\n]+)/im,
        describe: /^描述[：:]\s*((?:.|\n)+?)(?=\n\S+[：:]|$)/im,
        time: /^成立时间[：:]\s*(\d{4}?)/im,
        website: /^网站[：:]\s*([^\n]+)/i
    };
    
    const result = {};
    for (const key in patterns) {
        const match = cleanContent.match(patterns[key]);
        if (key === 'tags') {
            result[key] = (match?.[1] || '').split(';').map(tag => tag.trim()).filter(Boolean);
        } else {
            result[key] = (match?.[1] || '').trim();
        }
    }

    return result;
}
</script>

<style scoped>
#app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background-color: #3e3e3f;
}

.title {
    background-color: #06072B;
    height: 6vh;
}

.logo {
    height: 60%;
    object-fit: contain;
    margin-left: 10%;
    margin-top: 0.7%;
}

.logo02 {
    width: 107px;
    object-fit: contain;
    margin-top: 2%;
    margin-left: 10%;
}

.cover-img {
    width: 100%;
}

.content-container {
    background-image: url('/public/static/photo/picture02.png');
    background-position: center; 
}

.tech-layer {
    display: flex;
    border: 2px solid #1890ff; /* Ant Design主题蓝色边框 */
    border-radius: 8px;
    margin-top: 1%;
    margin-bottom: 1%;
    margin-left: 10%;
    margin-right: 10%;
}

.section-title {
    color: #f5f7f9;
    margin-bottom: 16px;
    font-size: 20px;
    display: flex;
    flex-wrap: wrap;
    padding: 20px;
    writing-mode: vertical-rl;
    line-height: 1.5;
}

.ai-framework {
    display: flex;
    flex-wrap: wrap;
}

.ai-frameworks {
  border: 1px dashed #69c0ff; /* 虚线边框区分层级 */
  border-radius: 6px;
  width: 30%;
  padding: 0.5%;
  margin-top: 0.5%;
  margin-bottom: 0.5%;
  margin-left: 10px;
  background: white;
  display: flex;
  flex-wrap: wrap;
}

.sub-title {
  color: #595959;
  margin-bottom: 2%;
  margin-top: 0%;
  font-size: 7%;
}

.grid-item:hover {
  transform: translateY(-4px);
}

.grid-container {
  display: flex;
  flex-wrap: wrap; /* ✅ 允许换行 */
  gap: 16px; /* 可选：设置项目之间的间距 */
}

.grid-item {
  flex: 0 0 auto;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: transform 0.2s;
}

.tech-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain; /* 锁定纵横比，不拉伸 */
}
.popup {
    position: fixed;
    z-index: 9999;
    padding: 24px;
    background: rgba(24, 144, 255, 0.98); /* 更纯净的蓝色背景 */
    color: white;
    border-radius: 7px;
    box-shadow: 0 12px 32px rgba(24, 144, 255, 0.3);
    font-size: 15px;
    line-height: 1.5;
    max-width: 400px;
    word-break: break-word;
    animation: fadeIn 0.3s ease-in-out;
}

/* 弹窗标题样式 */
.popup h3 {
    margin-top: 0;
    margin-bottom: 12px;
    font-size: 20px;
    color: #fff;
    font-weight: bold;
}

/* 段落间距优化 */
.popup p {
    margin: 8px 0;
    color: #f9f9f9;
}

/* 链接样式 */
.popup a {
    color: #e6f7ff;
    text-decoration: underline;
    word-break: break-all;
}

/* 添加淡入动画 */
@keyframes fadeIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}

/* 关闭按钮样式 */
.popup .close-btn {
    position: absolute;
    top: 8px;
    right: 12px;
    background: transparent;
    border: none;
    color: white;
    font-size: 20px;
    cursor: pointer;
    font-weight: bold;
    outline: none;
    transition: transform 0.2s;
}

.popup .close-btn:hover {
    transform: rotate(90deg);
}

.export-btn {
    background-color: #262A36;
    height: 20vh;
}

</style>    