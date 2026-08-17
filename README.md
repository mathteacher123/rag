# Local Execution & Testing

This section guides you through running the web server locally and testing its endpoints.

## 1. Start Web Server

Run the following command from the root directory to spin up the FastAPI application with auto-reload enabled:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 2. GitHub Codespaces Port Visibility Configuration

By default, forwarded ports in GitHub Codespaces are set to **Private**. To allow external tools or APIs to access your local chunking endpoint, you must change the visibility of port `8000` to **Public**. 

Choose **one** of the methods below:

### Method A: Via Terminal (Fastest)
Execute this command directly in your Codespace terminal pane to flip the port visibility instantly:

```bash
gh codespace ports visibility 8000:public -c $CODESPACE_NAME
```

### Method B: Via VS Code User Interface
1. Navigate to the bottom panel section and click on the **Ports** tab.
2. Find port `8000` in the forwarded ports list.
3. Right-click on the port line item and hover over **Port Visibility**.
4. Select **Public** from the dropdown options list.

---

## 3. Test HTML Chunking POST Endpoint

Open a separate terminal window to test your target endpoint using the full hosted environment proxy URL:

```bash
curl -X POST "https://vigilant-capybara-45479rjr959h964-8000.app.github.dev/test/chunking" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com"}'
```

---

## 4. Local Development Environment Shortcuts

If you prefer using fast terminal shortcuts instead of typing the raw execution strings above every time, you can utilize the workspace configuration script.

### Activate Shortcuts
Run the following line in your active terminal session to register the custom workspace shorthand utilities (`devserver` and `chunkurl`) and automatically flip your Codespace port visibility to public:

```bash
source ./dev_env.sh
```

### Persistent Configuration
*Tip: If you want these shortcuts automatically active every time you launch this specific workspace terminal, append the initialization hook directly into your local profile file (replace `/path/to/your/project/` with your actual repository folder path):*

```bash
echo "source /path/to/your/project/dev_env.sh" >> ~/.bashrc
```
