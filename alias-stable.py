import json, sys, urllib.request, urllib.error
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response
def call(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    add_surrogate_to_request(req, "custom.vercel", entry_name="access_token", allowed_hosts=("api.vercel.com",))
    with urllib.request.urlopen(req, timeout=60) as resp:
        return read_json_response(resp)
proj = "prj_mWff5SZDwtFbt5NJcWb8dUFdAY9s"
deps = call("GET", f"https://api.vercel.com/v6/deployments?projectId={proj}&limit=1&target=production")
dep_id = deps["deployments"][0]["uid"]
print("latest deployment:", dep_id)
try:
    r = call("POST", f"https://api.vercel.com/v2/deployments/{dep_id}/aliases", {"alias": "balap-kelereng-3d.vercel.app"})
    print("alias OK:", r.get("alias"))
except urllib.error.HTTPError as e:
    print("alias HTTP", e.code, e.read().decode()[:300])
