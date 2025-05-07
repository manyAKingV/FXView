<template>
    <div id="app">
        <!-- 导航栏 -->
        <a-layout-header>
            <div class="logo">
                <img src="@/assets/logo.png" alt="Company Logo">
            </div>
        </a-layout-header>
        <!-- 内容区域 -->
        <a-layout-content class="content-container">
            <div class="tech-layer">
                <div class="section-title">应用层</div>
                <div class="ai-framework">
                    <div class="ai-frameworks">
                    <h3 class="sub-title">智能城市</h3>
                    <div class="grid-container">
                        <div class="grid-item" v-for="(conpany, index) in companies" :key="index">
                            <img :src="`/static/icon/${conpany.name}.png`" alt="智能城市" class="tech-img" />
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
    </div>
</template>
  
<script>
import { exportToPDF } from "@/utils/pdfExport";
// import marked from 'marked';
// import matter from 'gray-matter';

export default {
    name: 'App',
    data() {
        return {
            companies:[],
        };
    },

    beforeMount(){

    },
    async mounted(){
        this.getCompany();
    },

    methods: {
        // 导出pdf功能
        async handleExport(){
            // 输入div的class 和 导出的名称
            exportToPDF('app','landscape.pdf')
        },
        // 获取公司信息
        getCompany() {
            // 使用 require.context 扫描 public/company 目录下的所有.md 文件
            const mdContext = require.context('@/../public/company', false, /\.md$/);
            const allMDFiles = mdContext.keys().reduce((acc, filePath) => {
                // 优化路径处理（兼容Windows/Linux）
                const fileName = filePath
                .replace(/^\.\//, '')
                .replace(/\.md$/, '')
                .split('/')
                .pop();
                // 移除.default获取方式
                const content = mdContext(filePath); 
                acc[fileName] = content;
                return acc;
            }, {});
            
            const result = Object.values(allMDFiles).map(content => {
                const parseMD = (content) => {
                    if (!content) {
                        return {
                            name: '',
                            describe: '',
                            time: '',
                            website: null,
                            tags: []
                        };
                    }

                    const cleanContent = content
                        .replace(/<\/?p>/g, '')
                        .replace(/<br\s*\/?>/g, '\n')
                        .replace(/<\/?a[^>]*>/g, '');

                    // TODO 处理描述、名称、网站、标签为空导致的问题
                    const patterns = {
                        name: /名称:\s*([^\n]+)/im,
                        describe: /^描述[：:]\s*((?:.|\n)+?)(?=\n\S+[：:]|$)/im,
                        time: /^成立时间[：:]\s*(\d{4}?)/im,
                        website: /网站:\s*([^\n]+)/i,
                        tags: /标签分类:\s*([^\n]+)/i
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
                };
                const x = parseMD(content)
                return x
            });
            // todo 将读取的内容正常的展示到第一栏中
            
            this.companies = result;
            console.log("result",this.companies);
        },
        
    }
};
</script>

<style scoped>
#app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background-color: #3e3e3f;
}

.logo {
    font-size: 24px;
    font-weight: bold;
}

.content-container {
    padding: 50px;
    background-color: #f5f5f5;
}

.tech-layer {
    display: flex;
    border: 2px solid #1890ff; /* Ant Design主题蓝色边框 */
    border-radius: 8px;
    background: #f0f9ff; /* 浅蓝色背景 */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 阴影增强层次感 */
    margin: 1%;
}

.section-title {
  color: #1890ff;
  margin-bottom: 16px;
  font-size: 20px;
  display: flex;
  flex-wrap: wrap;
  padding: 20px;
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

</style>    