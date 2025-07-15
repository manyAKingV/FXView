### 1. Fork and Branch

Fork the repository 
```bash
git clone https://github.com/openfusionx/FXView.git
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

Once you are happy with your changes, commit them and open a pull request against the `main` branch of the main repository. Your changes will be reviewed by the community and then merged to the main branch upon approval.
