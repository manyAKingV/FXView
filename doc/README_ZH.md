#  FXView - AI 生态图谱

![image](https://img.shields.io/badge/license-MIT-green)  ![image](https://img.shields.io/badge/contributors-5-blue)  

FXView 是一个基于 CNCF 的 [Landscape2](https://github.com/cncf/landscape2) 工具构建的 AI 生态系统交互式图谱。它提供了一个动态且可筛选的 AI 公司和项目视图。

本项目由 [FusionX](https://www.fusionx.net/) 支持。

## 🚀 工作原理

该图谱通过数据文件和脚本的组合生成：

1.  **数据源**：公司信息存储在 `/company` 目录下的单独 Markdown/txt 文件中。这些公司的标志存储在 `/logos` 目录中。
2.  **数据处理**：Python 脚本 `generate_landscape.py` 读取公司 Markdown/txt 文件，处理数据（例如，生成用于排序的拼音前缀、格式化 URL），并将其合并到单个 `landscape.yml` 文件中。
3.  **网站生成**：`landscape2` 命令行工具使用 `landscape.yml` 文件以及 `settings.yml` 和 `logos/` 目录来构建静态 HTML、CSS 和 JavaScript 网站。
4.  **部署**：生成的网站使用 Docker 容器化并部署到云环境。

## 🙋‍ 开始使用（本地查看）

要在本地机器上构建和查看图谱，请按照以下步骤操作。

### 前置条件

- **Python 3**：确保已安装 Python 3。
- **Landscape2**：需要安装 `landscape2` CLI 工具。您可以在[这里](https://github.com/cncf/landscape2#installation)找到安装说明。对于 macOS 用户，最简单的方法是使用 Homebrew：
  ```bash
  brew install cncf/landscape2/landscape2
  ```
  Ubuntu/CentOS：
   ```bash
  curl --proto '=https' --tlsv1.2 -LsSf \
          https://github.com/cncf/landscape2/releases/download/v1.0.0/landscape2-installer.sh | sh
  ```

### 步骤

1.  **克隆仓库：**
    ```bash
    git clone https://github.com/your-username/FXView-landscape.git
    cd FXView-landscape
    ```

2.  **安装 Python 依赖：**
    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

3.  **生成 `landscape.yml` 文件：**
    ```bash
    python convert_images_to_svg.py
    python generate_landscape.py
    ```
    此命令从 `/company` 和 `/logos` 目录读取并创建 `landscape.yml` 文件。

4.  **构建静态网站：**
    ```bash
    landscape2 build \
            --data-file landscape.yml \
            --settings-file settings.yml \
            --logos-path ./logos/ \
            --output-dir build
    ```
    这将在 `build/` 目录中生成静态网站。

5.  **清理自动生成的英文缩写（可选）**
    
    如果您的项目包含中文描述或标志，请运行 `replace.py` 脚本以从构建的网站中删除自动生成的英文文本。
    ```bash
    python replace.py
    ```

6.  **本地提供网站服务：**
    ```bash
    landscape2 serve --landscape-dir build
    ```
    图谱将在 `http://127.0.0.1:8000` 上可用。

## 🤝 如何贡献

我们欢迎贡献！要在图谱中添加或更新条目，请遵循此流程。

### 1. Fork 和分支

Fork 仓库并切换到 `landprovide` 分支：
```bash
git clone https://github.com/openfusionx/FXView.git
cd FXView
git checkout landprovide
```

### 2. 添加或更新公司信息

- **添加新公司**：在 `/company` 目录中创建新的 Markdown/txt 文件（例如，`company_name.md`、`company_name.txt`）。
- **更新公司**：编辑 `/company` 目录中现有的 Markdown/txt 文件。

Markdown/txt 文件应包含用冒号分隔的键值对。以下是一个示例：

```markdown
名称: FusionX
描述: FusionX is a company focused on AI...
成立时间: 2023
官网网站: https://www.fusionxu.com/
一级分类: 应用层
二级分类: AI平台
展示大小: 大
展示优先级: 1
```

**字段描述：**

- `名称`：（必填）公司或项目的名称。
- `描述`：简要描述。
- `成立时间`：公司成立的年份。
- `官网网站`：官方网站 URL。
- `一级分类`：主要类别。必须是以下之一：`应用层`、`服务层`、`技术层`、`基础设施层`。
- `二级分类`：子类别。
- `展示大小`：控制图谱上的显示大小。使用 `大` 表示大标志，`小` 表示小标志。
- `展示优先级`：1 到 5 的数字，决定子类别内的排序顺序。`1` 是最高优先级。

### 3. 添加标志

- 将公司标志添加到 `company/logos` 目录。

- 如果您添加非 SVG 标志（如 `.png`、`.jpg` 或 `.jpeg`），必须运行转换脚本以自动将其转换为 SVG。转换后将删除原始文件。
    ```bash
    python convert_images_to_svg.py
    ```
- 标志文件名最好与公司名称匹配，以便于识别。

### 4. 本地测试您的更改

1.  运行生成脚本以更新 `landscape.yml`。如果您添加了非 SVG 标志，请记住先运行转换脚本。
    ```bash
    python generate_landscape.py
    ```
2.  构建并提供图谱服务以预览您的更改：
    ```bash
    landscape2 build \
            --data-file landscape.yml \
            --settings-file settings.yml \
            --logos-path ./logos/ \
            --output-dir build
    landscape2 serve --landscape-dir build
    ```
    验证您的新条目是否正确显示。

### 5. 提交拉取请求

当您完成完成验证后，提交它们并针对主仓库的 `landprovide` 分支打开拉取请求。您的更改将由社区审查，然后在批准后合并到主分支。

## 👨🏽‍💻 部署

部署由 `.github/workflows/deploy.yml` 中定义的 GitHub Actions 工作流自动处理。当更改从 `landprovide` 分支合并到主分支时，工作流将：

1.  运行 Python 脚本以准备数据并生成 `landscape.yml`。
2.  使用 `landscape2` 构建静态站点。
3.  构建包含站点的 Docker 镜像。
4.  将 Docker 镜像推送到我们的容器注册表。

---
* ✨ FXView是一个社区驱动的项目，期待大家积极参与贡献！。*
