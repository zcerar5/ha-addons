from importlib.util import find_spec
from pathlib import Path


TERMINAL_TEMPLATE = r"""{% extends "base.html" %}

{% block title %}Terminal - open3e{% endblock %}

{% block content %}
<div class="p-4">
    <div class="d-flex align-items-center justify-content-between mb-4">
        <div>
            <h4 class="mb-1"><i class="bi bi-terminal"></i> Open3e Terminal</h4>
            <div class="text-muted small">Run allowlisted Open3e CLI tools from the add-on container.</div>
        </div>
        <button class="btn btn-outline-secondary btn-sm" onclick="clearTerminal()">
            <i class="bi bi-x-lg"></i> Clear
        </button>
    </div>

    <div class="alert alert-warning py-2">
        <i class="bi bi-exclamation-triangle me-1"></i>
        This terminal is restricted to Open3e commands and runs without a shell. It does not support pipes, redirects, or general Linux commands.
    </div>

    <div class="card mb-3">
        <div class="card-header d-flex align-items-center justify-content-between">
            <span><i class="bi bi-keyboard"></i> Command</span>
            <span class="text-muted small">Working directory: <code>/data</code></span>
        </div>
        <div class="card-body">
            <textarea class="form-control font-monospace mb-3" id="terminal-command" rows="3"
                      spellcheck="false" placeholder="open3e --help"></textarea>
            <div class="d-flex flex-wrap gap-2">
                <button class="btn btn-primary" onclick="runTerminalCommand()">
                    <i class="bi bi-play-fill"></i> Run
                </button>
                <button class="btn btn-outline-secondary btn-sm" onclick="setTerminalCommand('open3e --help')">open3e help</button>
                <button class="btn btn-outline-secondary btn-sm" onclick="setTerminalCommand('open3e_depictSystem --help')">depict help</button>
                <button class="btn btn-outline-secondary btn-sm" onclick="setTerminalCommand('open3e_topology --help')">topology help</button>
                <button class="btn btn-outline-secondary btn-sm" onclick="setTerminalCommand('open3e_dids2json --help')">dids2json help</button>
            </div>
        </div>
    </div>

    <div class="card">
        <div class="card-header d-flex align-items-center justify-content-between">
            <span><i class="bi bi-file-text"></i> Output</span>
            <span class="text-muted small" id="terminal-status">idle</span>
        </div>
        <pre class="terminal-output mb-0 p-3" id="terminal-output"></pre>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
function setTerminalCommand(command) {
    document.getElementById('terminal-command').value = command;
    document.getElementById('terminal-command').focus();
}

function clearTerminal() {
    document.getElementById('terminal-output').textContent = '';
    document.getElementById('terminal-status').textContent = 'idle';
}

async function runTerminalCommand() {
    const commandInput = document.getElementById('terminal-command');
    const output = document.getElementById('terminal-output');
    const status = document.getElementById('terminal-status');
    const command = commandInput.value.trim();

    if (!command) {
        showToast('Enter an Open3e command first.', 'warning');
        return;
    }

    status.textContent = 'running...';
    output.textContent += '$ ' + command + '\n';

    try {
        const result = await apiCall('/api/terminal/run', 'POST', { command: command });
        output.textContent += (result.output || '') + '\n';
        output.textContent += '[exit ' + result.returncode + ']\n\n';
        status.textContent = result.ok ? 'completed' : 'failed';
        output.scrollTop = output.scrollHeight;
    } catch (err) {
        status.textContent = 'failed';
        output.textContent += '[error] ' + err.message + '\n\n';
        output.scrollTop = output.scrollHeight;
    }
}

document.getElementById('terminal-command').addEventListener('keydown', function(event) {
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        event.preventDefault();
        runTerminalCommand();
    }
});
</script>
{% endblock %}
"""


TERMINAL_ROUTES = r'''
    # -----------------------------------------------------------------------
    # API: restricted Open3e terminal
    # -----------------------------------------------------------------------

    @app.get("/terminal", response_class=HTMLResponse)
    async def terminal_page(request: Request):
        return templates.TemplateResponse(
            request,
            "terminal.html",
            {"active_page": "terminal"},
        )

    @app.post("/api/terminal/run")
    async def api_terminal_run(request: Request):
        import shlex

        body = await request.json()
        command = str(body.get("command", "")).strip()
        if not command:
            raise HTTPException(status_code=400, detail="Command is required")
        if len(command) > 2000:
            raise HTTPException(status_code=400, detail="Command is too long")

        try:
            args = shlex.split(command)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))

        allowed_commands = {
            "open3e",
            "open3e_depictSystem",
            "open3e_dids2json",
            "open3e_dids2md",
            "open3e_topology",
        }
        if not args or args[0] not in allowed_commands:
            raise HTTPException(
                status_code=400,
                detail="Only Open3e commands are allowed: " + ", ".join(sorted(allowed_commands)),
            )

        proc = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            cwd="/data",
        )
        try:
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=120)
        except asyncio.TimeoutError:
            proc.kill()
            await proc.communicate()
            return {
                "ok": False,
                "returncode": 124,
                "output": "Command timed out after 120 seconds.",
            }

        output = stdout.decode("utf-8", errors="replace") if stdout else ""
        if len(output) > 64000:
            output = output[-64000:]
            output = "[output truncated to last 64000 characters]\n" + output

        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "output": output,
        }

'''


CSS = r'''

.terminal-output {
    background: #05070a;
    color: #d1e7dd;
    min-height: 360px;
    max-height: 60vh;
    overflow: auto;
    white-space: pre-wrap;
    word-break: break-word;
}
'''


server_spec = find_spec("open3e.web.server")
if server_spec is None or server_spec.origin is None:
    raise RuntimeError("open3e.web.server was not found")

base_spec = find_spec("open3e.web")
if base_spec is None or base_spec.submodule_search_locations is None:
    raise RuntimeError("open3e.web package was not found")

web_dir = Path(next(iter(base_spec.submodule_search_locations)))
server_path = Path(server_spec.origin)
base_template_path = web_dir / "templates" / "base.html"
terminal_template_path = web_dir / "templates" / "terminal.html"
css_path = web_dir / "static" / "css" / "app.css"

server_source = server_path.read_text()
if '"/api/terminal/run"' not in server_source:
    anchor = "    # -----------------------------------------------------------------------\n    # API: settings\n    # -----------------------------------------------------------------------\n"
    if anchor not in server_source:
        raise RuntimeError("Could not find settings API anchor in server.py")
    server_source = server_source.replace(anchor, TERMINAL_ROUTES + anchor, 1)
    server_path.write_text(server_source)

base_source = base_template_path.read_text()
if "active_page == 'terminal'" not in base_source:
    nav_anchor = """                <li class="nav-item">
                    <a class="nav-link {% if active_page == 'settings' %}active{% endif %}" href="/settings">
                        <i class="bi bi-gear"></i> Settings
                    </a>
                </li>
"""
    nav_terminal = """                <li class="nav-item">
                    <a class="nav-link {% if active_page == 'terminal' %}active{% endif %}" href="/terminal">
                        <i class="bi bi-terminal"></i> Terminal
                    </a>
                </li>
""" + nav_anchor
    if nav_anchor not in base_source:
        raise RuntimeError("Could not find settings nav anchor in base.html")
    base_source = base_source.replace(nav_anchor, nav_terminal, 1)
    base_template_path.write_text(base_source)

terminal_template_path.write_text(TERMINAL_TEMPLATE)

css_source = css_path.read_text()
if ".terminal-output" not in css_source:
    css_path.write_text(css_source.rstrip() + CSS + "\n")
