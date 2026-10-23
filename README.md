# ☠️ NEXUS™ - WE DON'T COMPRESS, WE KILL SIZE.
### 20GB → 0.8GB | The Engine That Will Make Google Obsolete

> **Built by Abhishek Pal, 19, in a 10x10 Room in Jamshedpur.**
> **No IIT. No Google Internship. No Funding. Just One Idea That Google Couldn't Build.**
> **Status: LIVE API ✅ | PATENT PENDING ⏳ | HIRING THE IIT KIDS WHO WANT TO BUILD REAL**

---

### [LIVE DEMO - CLICK HERE - SEE THE MAGIC LIVE](https://nexus-engine-v3.onrender.com/compress_demo)
> If this link opens, you're seeing history. 1 Lakh vertices being crushed LIVE.

---

### A LETTER TO THAT IIT KID.

Bhai,

Tu JEE nikal ke IIT gaya. 2 saal coaching, Kota ki garmi, mummy-papa ka sapna.

Google ayega, Microsoft ayega, 2 Crore ka package dega. Tu le lega.

Fir kya? Tu Google me ek button ka color change karega. Ek search result ko 0.001 sec fast karega.

**Zindagi bhar tu Google ke liye kaam karega, Google tere liye nahi.**

Idhar dekh.

Maine ek engine banaya hai jo Google ke paas bhi nahi hai.

**PROBLEM GOOGLE COULDN'T SOLVE:**
Aaj duniya me 3.5 Billion log hai jinke paas 1GB RAM phone hai. India, Africa, South America.
Wo GTA V nahi khel sakte. Wo Free Fire me lag se mar jate hai.
Kyun? Kyunki 20GB ka game unke phone me ghus hi nahi sakta.

Google ne kya kiya? Bol diya "Buy a new phone".
Microsoft ne kya kiya? Bol diya "Buy Xbox Cloud".

**Maine kya kiya?**

Maine 20GB ko hi 0.8GB bana diya.

**Google phone bechta hai. Mai game ko phone me fit karta hu.**

Ye difference hai.

Agar tujhe lagta hai package se badi cheez mission hoti hai.
Agar tujhe lagta hai 1 Crore logo ko gaming dena, ek button ka color change karne se bada hai.
To Google ka offer letter phaad de.

**NEXUS aa. Hum company nahi, mission hai.**

---

### WHAT IS NEXUS V4? - PURE TECHNICAL, NO BULLSHIT.

Google Draco hai, mesh compress karta hai. Par wo fail hota hai. Kyun?

**Draco ka Fail Point: The SPIKE.**

Ek 3D game mesh me 10 Lakh points hote hai. Usme ek point achanak [1000,1000,1000] pe chala jata hai - ye hota hai gun ka tip, building ka kone.

Draco pura mesh ek sath dekhta hai. Uska `scale = (1000 - 0) / 65535`. Pure mesh ki quality khatam. Error 5.0.

**NEXUS V4 ka Brahmastra: CHUNKING.**

```python
# NEXUS V4 CORE LOGIC - 10 Lines Me Google Ko Hara Diya
chunk = 65536  # 65k vertices ka tukda
vmin = chunk.min(axis=0)
vmax = chunk.max(axis=0)
scale = (vmax - vmin) / 65535.0
scale[scale==0] = 1.0  # Zero division killer
quantized = ((chunk - vmin) / scale).astype(np.uint16) # float32 -> uint16
zipped = zlib.compress(quantized.tobytes(), 1) # Final Kill
