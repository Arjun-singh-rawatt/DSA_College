import base64
import json
import time
import urllib.request
from websockets.sync.client import connect

pages = json.loads(urllib.request.urlopen("http://127.0.0.1:9225/json").read())
page = next(item for item in pages if item["type"] == "page")
with connect(page["webSocketDebuggerUrl"], origin="http://127.0.0.1") as ws:
    def command(ident, method, params=None):
        ws.send(json.dumps({"id": ident, "method": method, "params": params or {}}))
        while True:
            response = json.loads(ws.recv())
            if response.get("id") == ident:
                return response

    command(1, "Page.enable")
    command(2, "Runtime.enable")
    command(3, "Emulation.setDeviceMetricsOverride", {"width": 1365, "height": 900, "deviceScaleFactor": 1, "mobile": False})
    command(4, "Page.navigate", {"url": "http://127.0.0.1:8501"})
    expression = r"""(() => {const h=document.querySelector('h1');const b=document.querySelector('.sidebar-brand');const rect=e=>{if(!e)return null;const r=e.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}};return JSON.stringify({ready:document.readyState,title:rect(h),titleText:h?.textContent,brand:rect(b),metrics:[...document.querySelectorAll('[data-testid="stMetricLabel"]')].map(x=>x.textContent),metricVals:[...document.querySelectorAll('[data-testid="stMetricValue"]')].map(x=>x.textContent),mainPadding:getComputedStyle(document.querySelector('[data-testid="stMainBlockContainer"]')).paddingTop})})()"""
    result = None
    for _ in range(40):
        time.sleep(.5)
        evaluated = command(5, "Runtime.evaluate", {"expression": expression, "returnByValue": True})
        value = evaluated.get("result", {}).get("result", {}).get("value")
        if value is None:
            continue
        result = json.loads(value)
        if result.get("title") and len(result.get("metrics", [])) == 3:
            break
    print(json.dumps(result, indent=2))
    shot = command(6, "Page.captureScreenshot", {"format": "png", "fromSurface": True})
    with open("D:/ARJUN_code/01_prog_lan/COLLEGE/dsa/.tmp/dashboard-existing-port.png", "wb") as file:
        file.write(base64.b64decode(shot["result"]["data"]))
