# Lesson 0: API Fundamentals - From Scratch

## 🤔 The Core Question

**"Why can't we just make an API server directly in Python?"**

**Answer: You CAN!** But frameworks make it 100x easier. Let's see why...

---

## 🔵 What is an API Server?

**Fundamentally: A program that listens for HTTP requests and sends responses.**

```
Client (browser) → HTTP Request → Server → HTTP Response → Client
```

That's it! Everything else is convenience.

---

## 🐍 Pure Python HTTP Server

**Yes, you CAN make a server without any framework:**

```python
from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"message": "Hello"}')

# Start server
server = HTTPServer(('localhost', 8000), MyHandler)
print("Server running on http://localhost:8000")
server.serve_forever()
```

**Problems with this approach:**

| Issue | Example |
|-------|---------|
| **No routing** | `self.path` is just a string like "/users/123" - you parse it manually |
| **No JSON handling** | You `json.loads()` raw body manually |
| **No validation** | Check every field yourself |
| **No docs** | Write Swagger manually |
| **No async** | Blocking requests only |
| **No type hints** | No autocomplete, no validation |

**This is like writing `const server = http.createServer()` in Node.js** - you get raw HTTP, but you want Express!

---

## 🎯 Enter: Frameworks

**What a framework does:**

```
Raw HTTP → Framework → Your Code (clean!)
            ↓
         Routing
         JSON parsing
         Validation
         Type safety
         Docs
```

**Same as:**
- Node.js: `http.createServer()` → Express
- Go: `net/http` → Gin/Echo/Fiber
- Python: `http.server` → FastAPI

---

## 🚀 What is FastAPI?

**FastAPI is a framework that sits on top of Python's HTTP capabilities.**

```
┌─────────────────────────────────────┐
│         Your Application            │
│  (routes, business logic, models)   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│           FastAPI Framework         │
│  • Routing (@app.get, @app.post)    │
│  • Validation (Pydantic)            │
│  • JSON parsing/auto                 │
│  • Type hints → validation           │
│  • Auto-generated docs              │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         ASGI Server (Uvicorn)        │
│  • Handles actual HTTP connections  │
│  • Manages connections, async IO     │
│  • Speaks ASGI protocol              │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         TCP Socket (OS level)        │
│  • Raw network communication        │
└─────────────────────────────────────┘
```

---

## 🔷 What is Uvicorn?

**Uvicorn = The actual HTTP server**

FastAPI doesn't handle raw HTTP. It speaks **ASGI** (Asynchronous Server Gateway Interface).

**Analogy:**
```
Express app  → Node.js runtime → OS sockets
FastAPI app  → ASGI server (Uvicorn) → OS sockets
```

**ASGI is the interface:**
```python
# What Uvicorn sees (ASGI protocol):
async def app(scope, receive, send):
    # scope = request details (path, method, headers)
    # receive = async function to get body
    # send = async function to send response
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [[b'content-type', b'application/json']],
    })
    await send({
        'type': 'http.response.body',
        'body': b'{"message": "hello"}',
    })
```

**FastAPI wraps this raw ASGI into something nice:**
```python
@app.get("/")
async def root():
    return {"message": "hello"}  # FastAPI converts to ASGI for you!
```

---

## 📊 Comparison: Node.js vs Python

| Layer | Node.js | Python |
|-------|---------|--------|
| **Your code** | Express routes | FastAPI routes |
| **Framework** | Express | FastAPI |
| **Runtime** | Node.js (V8) | CPython |
| **HTTP server** | Built-in (libuv) | Uvicorn (separate) |

**Why separate in Python?**
- **Choice:** Gunicorn, Uvicorn, Hypercorn, Daphne
- **Specialization:** Sync vs async, performance needs
- **History:** WSGI (Django/Flask) vs ASGI (FastAPI)

---

## 🎯 Why FastAPI Over Other Python Frameworks?

| Framework | Type | Async? | Auto Docs | Type Safety |
|-----------|------|--------|-----------|-------------|
| **http.server** | Built-in | ❌ | ❌ | ❌ |
| **Flask** | Framework | ⚠️ (via extensions) | ❌ | ⚠️ (via extensions) |
| **Django** | Full-stack | ⚠️ (partial) | ❌ | ⚠️ (via extensions) |
| **FastAPI** | Framework | ✅ Native | ✅ Auto | ✅ Native |

**For AI/LLM work:**
- FastAPI = Modern, async, typed, auto-docs
- Perfect for AI APIs (OpenAI, Anthropic integrations)

---

## 🤔 Why Not Just Use Express in Node.js?

**You COULD!** But for AI/LLM work:
- Python = First-class AI ecosystem (LangChain, LlamaIndex, etc.)
- FastAPI = Feels like Express, but with Python's AI libraries

---

## 📦 Summary: The Stack

```
Your Code
    ↓ (type hints, return dict)
FastAPI (Framework - routing, validation, docs)
    ↓ (ASGI protocol)
Uvicorn (ASGI Server - HTTP handling)
    ↓ (TCP)
Operating System
    ↓ (Network)
Client (Browser, API consumer)
```

**Without FastAPI:** You write ASGI by hand (painful!)
**Without Uvicorn:** You write TCP sockets by hand (more painful!)

---

## ✅ You Now Understand:

1. **API Server** = Program that speaks HTTP
2. **Pure Python** = Can do it, but painful (like `http.createServer`)
3. **FastAPI** = Framework that makes it nice (like Express)
4. **Uvicorn** = The actual HTTP server that speaks ASGI

**Next:** Let's build your first FastAPI API!
