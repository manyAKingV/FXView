#  FXView - AI 生态图谱

![image](https://img.shields.io/badge/license-MIT-green)  ![image](https://img.shields.io/badge/contributors-5-blue)  

FXView 是一个基于 CNCF开源 的 [Landscape2](https://github.com/cncf/landscape2) 工具构建的 AI 生态系统交互式图谱。它提供了一个动态且可筛选的 AI行业公司和项目视图。

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

[开发人员](https://github.com/Ada-pro/FXView/blob/main/doc/Contribution_development.md)

[非开发人员](https://github.com/Ada-pro/FXView/blob/main/doc/%E5%A6%82%E4%BD%95%E5%8F%82%E4%B8%8E%E8%B4%A1%E7%8C%AE_%E9%9D%9E%E6%8A%80%E6%9C%AF.md)

## 👨🏽‍💻 部署

部署由 `.github/workflows/deploy.yml` 中定义的 GitHub Actions 工作流自动处理。当更改从 `landprovide` 分支合并到主分支时，工作流将：

1.  运行 Python 脚本以准备数据并生成 `landscape.yml`。
2.  使用 `landscape2` 构建静态站点。
3.  构建包含站点的 Docker 镜像。
4.  将 Docker 镜像推送到我们的容器注册表。

---
* ✨ FXView是一个社区驱动的项目，期待大家积极参与贡献！*
