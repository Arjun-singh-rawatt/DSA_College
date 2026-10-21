import base64
import json
import time
import urllib.request
from websockets.sync.client import connect

pages = json.loads(urllib.request.urlopen("http://127.0.0.1:9224/json").read())
page = next(item for item in pages if item["type"] == "page" and ":8503" in item["url"])
with connect(page["webSocketDebuggerUrl"], origin="http://127.0.0.1") as ws:
    def command(ident, method, params=None):
        ws.send(json.dumps({"id": ident, "method": method, "params": params or {}}))
        while True:
            response = json.loads(ws.recv())
            if response.get("id") == ident:
                return response

    command(1, "Page.enable")
    command(2, "Runtime.enable")
    command(5, "Emulation.setDeviceMetricsOverride", {"width": 1365, "height": 900, "deviceScaleFactor": 1, "mobile": False})
    command(6, "Page.reload", {"ignoreCache": True})
    time.sleep(8)
    expression = r"""(() => {
      const box = el => { if (!el) return null; const r=el.getBoundingClientRect(), s=getComputedStyle(el); return {tag:el.tagName,testid:el.dataset.testid||'',cls:String(el.className).slice(0,100),x:r.x,y:r.y,w:r.width,h:r.height,paddingTop:s.paddingTop,marginTop:s.marginTop,position:s.position,display:s.display}; };
      const main=document.querySelector('[data-testid="stMainBlockContainer"]');
      const title=[...document.querySelectorAll('h1')].find(e=>e.textContent.includes('Student Performance Dashboard'));
      const brand=document.querySelector('.sidebar-brand');
      const sidebar=document.querySelector('[data-testid="stSidebar"]');
      const ancestors=el=>{const a=[];while(el&&a.length<8){a.push(box(el));el=el.parentElement;}return a;};
      const titleStyle=title?getComputedStyle(title):null;
      return JSON.stringify({viewport:{w:innerWidth,h:innerHeight,scrollX,scrollY},title:box(title),titleText:title?.textContent,titleStyle:titleStyle?{color:titleStyle.color,opacity:titleStyle.opacity,visibility:titleStyle.visibility,fontSize:titleStyle.fontSize}:null,underTitle:document.elementsFromPoint(400,75).slice(0,4).map(e=>({tag:e.tagName,testid:e.dataset.testid||'',text:(e.textContent||'').slice(0,50)})),brand:box(brand),brandAncestors:ancestors(brand),main:ancestors(main).slice(0,3),sidebar:ancestors(brand).slice(0,5)});
    })()"""
    evaluated = command(3, "Runtime.evaluate", {"expression": expression, "returnByValue": True})
    value = evaluated["result"]["result"].get("value")
    print(json.dumps(json.loads(value), indent=2))
    shot = command(4, "Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True})
    with open("D:/ARJUN_code/01_prog_lan/COLLEGE/dsa/.tmp/dashboard-post-restart.png", "wb") as file:
        file.write(base64.b64decode(shot["result"]["data"]))
