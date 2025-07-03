# ✨ FXView - AI Landscape

![image](https://img.shields.io/badge/license-MIT-green)  ![image](https://img.shields.io/badge/contributors-5-blue)  

FXView is an interactive landscape of the AI ecosystem, powered by the CNCF's [Landscape2](https://github.com/cncf/landscape2) tool. It provides a dynamic and filterable view of AI companies and projects.

This project is supported by [FusionX](https://www.fusionx.net/).

## 🚀 How it Works

The landscape is generated through a combination of data files and scripts:

1.  **Data Source**: Company information is stored in individual Markdown/txt files within the `/company` directory. Logos for these companies are stored in the `/logos` directory.
2.  **Data Processing**: A Python script, `generate_landscape.py`, reads the company Markdown/txt files, processes the data (e.g., generating pinyin prefixes for sorting, formatting URLs), and combines it into a single `landscape.yml` file.
3.  **Website Generation**: The `landscape2` command-line tool takes the `landscape.yml` file, along with `settings.yml` and the `logos/` directory, to build a static HTML, CSS, and JavaScript website.
4.  **Deployment**: The generated website is containerized using Docker and deployed to a cloud environment.

## 🙋‍ Getting Started (Viewing Locally)

To build and view the landscape on your local machine, follow these steps.

### Prerequisites

- **Python 3**: Make sure you have Python 3 installed.
- **Landscape2**: You need to install the `landscape2` CLI tool. You can find installation instructions [here](https://github.com/cncf/landscape2#installation). The easiest way for macOS users is with Homebrew:
  ```bash
  brew install cncf/landscape2/landscape2
  ```
  Ubuntu/CentOS: 
   ```bash
  curl --proto '=https' --tlsv1.2 -LsSf \
          https://github.com/cncf/landscape2/releases/download/v1.0.0/landscape2-installer.sh | sh
  ```
  

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/FXView-landscape.git
    cd FXView-landscape
    ```

2.  **Install Python dependencies:**
    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

3.  **Generate the `landscape.yml` file:**
    ```bash
    python convert_images_to_svg.py
    python generate_landscape.py
    ```
    This command reads from the `/company` and `/logos` directories and creates the `landscape.yml` file.

4.  **Build the static website:**
    ```bash
    landscape2 build \
            --data-file landscape.yml \
            --settings-file settings.yml \
            --logos-path ./logos/ \
            --output-dir build
    ```
    This will generate the static website in the `build/` directory.

5.  **Clean up auto-generated English abbreviations (Optional)**
    
    If your project contains Chinese descriptions or logos, run the `replace.py` script to remove auto-generated English text from the built website.
    ```bash
    python replace.py
    ```

6.  **Serve the website locally:**
    ```bash
    landscape2 serve --landscape-dir build
    ```
    The landscape will be available at `http://127.0.0.1:8000`.

## 🤝 How to Contribute

We welcome contributions! To add or update an entry in the landscape, please follow this process.

### 1. Fork and Branch

Fork the repository and checkout the `landprovide` branch:
```bash
git clone https://github.com/openfusionx/FXView.git
cd FXView
git checkout landprovide
```

### 2. Add or Update Company Information

- **To add a new company**: Create a new Markdown/txt file in the `/company` directory (e.g., `company_name.md`,`company_name.txt`).
- **To update a company**: Edit the existing Markdown/txt file in the `/company` directory.

The Markdown/txt file should contain key-value pairs separated by a colon. Here is an example:

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

**Field Descriptions:**

- `名称`: (Required) The name of the company or project.
- `描述`: A brief description.
- `成立时间`: The year the company was founded.
- `官网网站`: The official website URL.
- `一级分类`: The main category. Must be one of: `应用层`, `服务层`, `技术层`, `基础设施层`.
- `二级分类`: The subcategory.
- `展示大小`: Controls the display size on the landscape. Use `大` for a large logo or `小` for a small one.
- `展示优先级`: A number from 1 to 5 that determines the sorting order within a subcategory. `1` is the highest priority.

### 3. Add a Logo

- Add the company's logo to the `company/logos` directory.

- If you add a non-SVG logo (like `.png`, `.jpg`, or `.jpeg`), you must run the conversion script to automatically convert it to SVG. The original file will be removed after conversion.
    ```bash
    python convert_images_to_svg.py
    ```
- The logo filename should ideally match the company name for easy identification.

### 4. Test Your Changes Locally

1.  Run the generation script to update `landscape.yml`. If you added a non-SVG logo, remember to run the conversion script first.
    ```bash
    python generate_landscape.py
    ```
2.  Build and serve the landscape to preview your changes:
    ```bash
    landscape2 build \
            --data-file landscape.yml \
            --settings-file settings.yml \
            --logos-path ./logos/ \
            --output-dir build
    landscape2 serve --landscape-dir build
    ```
    Verify that your new entry appears correctly.

### 5. Submit a Pull Request

Once you are happy with your changes, commit them and open a pull request against the `landprovide` branch of the main repository. Your changes will be reviewed by the community and then merged to the main branch upon approval.

## 🔭 Deployment

Deployment is handled automatically by a GitHub Actions workflow defined in `.github/workflows/deploy.yml`. When changes are merged from the `landprovide` branch to the main branch, the workflow will:

1.  Run the Python scripts to prepare the data and generate `landscape.yml`.
2.  Build the static site using `landscape2`.
3.  Build a Docker image containing the site.
4.  Push the Docker image to our container registry.

---
*This AI Landscape is a community-driven project. Your contributions are highly valued.*
