# main.py - NEXUS V4 API ONLY - Abhishek Pal
from fastapi import FastAPI
import numpy as np
import zlib
import base64

app = FastAPI(title="NEXUS V4 - Mesh Compressor API")

class NexusV4_Final:
    def __init__(self, chunk=65536):
        self.chunk = chunk
        
    def compress(self, vertices):
        vertices = vertices.astype(np.float32)
        packets = []
        total_orig = vertices.nbytes
        total_comp = 0
        
        for i in range(0, len(vertices), self.chunk):
            chunk_verts = vertices[i:i+self.chunk]
            vmin = chunk_verts.min(axis=0)
            vmax = chunk_verts.max(axis=0)
            scale = (vmax - vmin) / 65535.0
            scale[scale==0] = 1.0
            
            quantized = ((chunk_verts - vmin) / scale).astype(np.uint16)
            zipped = zlib.compress(quantized.tobytes(), 1)
            
            packets.append({
                "vmin": vmin.tolist(), 
                "scale": scale.tolist(), 
                "data": base64.b64encode(zipped).decode(),
                "len": len(chunk_verts)
            })
            total_comp += len(zipped) + 32
            
        ratio = total_orig / total_comp if total_comp else 0
        return {
            "chunks": len(packets),
            "ratio": round(ratio, 2),
            "orig_bytes": total_orig,
            "comp_bytes": total_comp,
            "message": f"20GB = {20/ratio:.2f}GB",
            "packets": packets
        }

    def decompress(self, packets):
        out = []
        for p in packets:
            zipped = base64.b64decode(p["data"])
            q = np.frombuffer(zlib.decompress(zipped), dtype=np.uint16).reshape(p["len"], 3)
            vmin = np.array(p["vmin"], dtype=np.float32)
            scale = np.array(p["scale"], dtype=np.float32)
            chunk = q.astype(np.float32) * scale + vmin
            out.append(chunk)
        return np.vstack(out)

v4 = NexusV4_Final()

@app.get("/")
def home():
    return {
        "engine": "NEXUS V4 FINAL",
        "author": "Abhishek Pal",
        "status": "Live ✅",
        "endpoints": ["/compress_demo", "/docs"]
    }

@app.get("/compress_demo")
def compress_demo():
    # 1 Lakh vertices ka demo + Tera Spike Test
    vertices = np.random.randn(100000, 3).astype(np.float32) * 0.01
    vertices[50000] += [1000, 1000, 1000]
    
    result = v4.compress(vertices)
    # Decompress check
    recovered = v4.decompress(result["packets"])
    error = float(np.mean(np.abs(vertices - recovered)))
    
    return {
        "demo": "1 Lakh Vertices + Spike at 50000",
        "chunks": result["chunks"],
        "ratio": result["ratio"],
        "20GB_to": f"{20/result['ratio']:.2f}GB",
        "error_mean": error,
        "status": "GAME READY ✅" if error < 0.01 else "FAIL ❌",
        "sample_packets": result["packets"][:1]  # Sirf 1 packet dikhayega
    }

@app.post("/compress")
def compress_api(data: dict):
    # data = {"vertices": [[x,y,z], [x,y,z], ...]}
    vertices = np.array(data["vertices"], dtype=np.float32)
    return v4.compress(vertices)
