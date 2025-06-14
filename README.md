**🚀 My Static Site Generator**
===============================

This project is a custom-built static site generator, created as part of the [Boot.dev](https://www.boot.dev) course. It takes Markdown content files and a HTML template, then processes them to produce a fully functional static website, ready for deployment!

**✨ Features**
--------------

*   **Markdown to HTML Conversion**: Automatically converts Markdown files (.md) into clean, semantic HTML.
    
*   **Template-Based Generation**: Uses a single HTML template to ensure consistent site structure and styling.
    
*   **Asset Management**: Copies static assets like CSS and images to the output directory.
    
*   **Relative Path Handling**: Correctly resolves href and src attributes for seamless navigation and asset loading, both locally and on GitHub Pages.
    
*   **Configurable Base Path**: Supports deploying the site to a subdirectory on web hosts like GitHub Pages.
    

**🛠️ Setup**
-------------

To get this project up and running locally, follow these simple steps:

1.  **Clone the repository:**git clone https://github.com/your-username/static-site-generator.gitcd static-site-generator_(Remember to replace your-username/static-site-generator.git with your actual repository URL)_
    
2.  Ensure Python is installed:This project requires Python 3.x. You can download it from python.org.
    
3.  **Make scripts executable:**chmod +x build.shchmod +x main.shchmod +x test.sh
    

**🏃 Usage**
------------

### **Local Development**

For local testing and development, run the following command. This will build the site into the docs/ directory and serve it using a simple Python HTTP server.

./main.sh

Open your browser and navigate to http://localhost:8888/ to see your site live.

### **Building for Production (GitHub Pages)**

To build the site for deployment on GitHub Pages (or any web server where your site is hosted in a subdirectory), use the build.sh script. Remember to replace REPO\_NAME with your actual GitHub repository name.

./build.sh # Make sure REPO\_NAME in build.sh is your actual repo name

_(Example: If your repo is static-site-generator, build.sh should contain python3 src/main.py "/static-site-generator/")_

This command generates the static site in the docs/ directory with paths correctly configured for your GitHub Pages URL (e.g., https://USERNAME.github.io/REPO\_NAME/).


**🙏 Credits**
--------------

This static site generator was built as part of the [Build a Static Site Generator with Python](https://www.boot.dev/courses/build-static-site-generator-python) course on [Boot.dev](https://www.boot.dev).
