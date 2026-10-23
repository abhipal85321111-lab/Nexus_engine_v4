import numpy as np
import time
import zlib

class NexusV4_Final:
    def __init__(self, chunk=65536):
        self.chunk = chunk

    def compress(self, vertices):
        vertices = vertices.astype(np.float32)
        packets = []
        total_orig = vertices.nbytes
        total_comp = 0

        for i in range(0, len(vertices), self.chunk):
            chunk_verts = vertices[i:i + self.chunk]
            vmin = chunk_verts.min(axis=0)
            vmax = chunk_verts.max(axis=0)
            scale = (vmax - vmin) / 65535.0
            scale[scale == 0] = 1.0

            quantized = ((chunk_verts - vmin) / scale).astype(np.uint16)
            zipped = zlib.compress(quantized.tobytes(), 1)

            packets.append({
                "vmin": vmin,
                "scale": scale,
                "data": zipped,
                "len": len(chunk_verts),
                "shape": quantized.shape
            })
            total_comp += len(zipped) + 32

        ratio = total_orig / total_comp
        print(f"[V4 FINAL] Chunks: {len(packets)} | Ratio: {ratio:.1f}x -> 20GB = {20 / ratio:.2f}GB")
        return packets

    def decompress(self, packets):
        out = []
        for p in packets:
            q = np.frombuffer(zlib.decompress(p["data"]), dtype=np.uint16).reshape(p["shape"])
            chunk = q.astype(np.float32) * p["scale"] + p["vmin"]
            out.append(chunk)
        return np.vstack(out)

# TERA SPIKE TEST
print("--- Testing V4 FINAL Direct ---")
spike = np.random.randn(1_000_000, 3).astype(np.float32) * 0.01
spike[500_000] += [1000, 1000, 1000]

v4 = NexusV4_Final()

s = time.time()
pk = v4.compress(spike)
print(f"Compress: {time.time() - s:.2f}s")

s = time.time()
r = v4.decompress(pk)
print(f"Decompress: {time.time() - s:.2f}s")

print(f"Error: {np.mean(np.abs(spike - r)):.6f} | Max: {np.max(np.abs(spike - r)):.6f}")
print(f"Status: {'✅ GAME READY' if np.mean(np.abs(spike - r)) < 0.01 else '❌'}")
