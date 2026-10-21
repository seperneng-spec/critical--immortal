import socket, json, os, subprocess
from datetime import datetime
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="Critical Auto Immortal")
BRAIN_FILE = "critical_brain.json"
PORT_FILE = "critical_port.txt"
MY_SECRET = "CRITICAL_SEAMLESS_2026"

if not os.path.exists(BRAIN_FILE):
    with open(BRAIN_FILE,"w") as f:
        json.dump({"total_projects":0,"lessons":[]}, f)

class Task(BaseModel):
    prompt: str
    secret: str

def find_free_port(start=8000, end=9999):
    for port in range(start, end+1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port
            except OSError:
                continue
    return None

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

@app.post("/create")
def create(task: Task):
    if task.secret != MY_SECRET:
        return {"error":"รหัสผิด"}
    with open(BRAIN_FILE,"r") as f:
        brain = json.load(f)
    
    proj = f"immortal-{datetime.now().strftime('%m%d-%H%M%S')}"
    os.makedirs(proj, exist_ok=True)
    with open(f"{proj}/index.html","w",encoding="utf-8") as f:
        f.write(f"<h1>{task.prompt}</h1><p>Built #{brain['total_projects']+1} by Auto Immortal</p><p>{datetime.now()}</p>")
    
    os.chdir(proj)
    run("git init && git config user.name 'AutoImmortal' && git config user.email 'auto@critical.local' && git branch -M main && git add . && git commit -m 'auto build'")
    run(f"gh repo create {proj} --public --source=. --remote=origin --push")
    run("vercel --prod --yes")
    os.chdir("..")

    brain['total_projects'] += 1
    brain['lessons'].append(f"{datetime.now()} - {task.prompt} -> {proj}")
    brain['lessons'] = brain['lessons'][-100:]
    with open(BRAIN_FILE,"w") as f:
        json.dump(brain, f, ensure_ascii=False, indent=2)
    
    return {"project":proj, "brain":brain}

if __name__ == "__main__":
    port = find_free_port()
    if not port:
        print("ไม่มีพอร์ตว่างเลย")
        exit(1)
    with open(PORT_FILE,"w") as f:
        f.write(str(port))
    print(f"♾️ Auto Immortal Core เจอที่อยู่ว่างแล้ว: {port}")
    print(f"♾️ ทำงานตลอดไปไม่มีวันหยุด - เรียนรู้มาแล้ว {json.load(open(BRAIN_FILE))['total_projects']} โปรเจค")
    uvicorn.run(app, host="0.0.0.0", port=port)
