#  FXView - AI Landscape

![image](https://img.shields.io/badge/license-MIT-green)  ![image](https://img.shields.io/badge/contributors-5-blue)  

English | [中文](doc/README_ZH.md)

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

[Development](https://github.com/Ada-pro/FXView/blob/main/doc/Contribution_development.md)

[非开发人员](https://github.com/Ada-pro/FXView/blob/main/doc/%E5%A6%82%E4%BD%95%E5%8F%82%E4%B8%8E%E8%B4%A1%E7%8C%AE_%E9%9D%9E%E6%8A%80%E6%9C%AF.md)


## 👨🏽‍💻 Deployment

Deployment is handled automatically by a GitHub Actions workflow defined in `.github/workflows/deploy.yml`. When changes are merged from the `landprovide` branch to the main branch, the workflow will:

1.  Run the Python scripts to prepare the data and generate `landscape.yml`.
2.  Build the static site using `landscape2`.
3.  Build a Docker image containing the site.
4.  Push the Docker image to our container registry.

---
* ✨ This AI Landscape is a community-driven project. Your contributions are highly valued.*
