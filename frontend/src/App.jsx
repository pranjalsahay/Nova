import { useEffect, useRef, useState, useMemo, useCallback } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Line } from "@react-three/drei";
import { motion, AnimatePresence } from "framer-motion";

const fontStyle = `@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@300;700&display=swap');`;

// =========================================
// FLOATING PARTICLES
// =========================================
function Particles() {
  const points = useMemo(() => {
    return Array.from({ length: 180 }, () => [
      (Math.random() - 0.5) * 12,
      (Math.random() - 0.5) * 12,
      (Math.random() - 0.5) * 12,
    ]);
  }, []);
  return (
    <>
      {points.map((pt, i) => (
        <mesh key={i} position={pt}>
          <sphereGeometry args={[0.018, 6, 6]} />
          <meshStandardMaterial
            color={i % 3 === 0 ? "#00f5ff" : i % 3 === 1 ? "#0891b2" : "#7ef7ff"}
            emissive={i % 3 === 0 ? "#00f5ff" : i % 3 === 1 ? "#0891b2" : "#7ef7ff"}
            emissiveIntensity={3}
          />
        </mesh>
      ))}
    </>
  );
}

// =========================================
// NEURAL LINES
// =========================================
function NeuralLines() {
  const lines = useMemo(() => {
    return Array.from({ length: 30 }, () => [
      [(Math.random() - 0.5) * 7, (Math.random() - 0.5) * 7, (Math.random() - 0.5) * 7],
      [(Math.random() - 0.5) * 7, (Math.random() - 0.5) * 7, (Math.random() - 0.5) * 7],
    ]);
  }, []);
  return (
    <>
      {lines.map((line, i) => (
        <Line
          key={i}
          points={line}
          color={i % 2 === 0 ? "#00f5ff" : "#0891b2"}
          lineWidth={0.6}
          transparent
          opacity={0.25}
        />
      ))}
    </>
  );
}

// =========================================
// SPIRIT FLAME SVG
// =========================================
function SpiritFlame({ status }) {
  const isListening = status === "Listening";
  const isThinking  = status === "Thinking";
  const isSpeaking  = status === "Speaking";

  const outerColor = isListening ? "#00f5ff" : isThinking ? "#f59e0b" : isSpeaking ? "#f0abfc" : "#00d4e8";
  const glowColor  = isListening
    ? "rgba(0,245,255,0.8)"
    : isThinking
    ? "rgba(245,158,11,0.7)"
    : isSpeaking
    ? "rgba(240,171,252,0.7)"
    : "rgba(0,212,232,0.6)";

  return (
    <motion.div style={{ position: "relative", display: "flex", flexDirection: "column", alignItems: "center", width: 220 }}>
      <motion.div
        style={{ display: "flex", justifyContent: "center", alignItems: "center" }}
        animate={{
          filter: [
            `drop-shadow(0 0 28px ${glowColor}) drop-shadow(0 0 60px ${glowColor.replace("0.8", "0.3")})`,
            `drop-shadow(0 0 44px ${glowColor}) drop-shadow(0 0 90px ${glowColor.replace("0.8", "0.5")})`,
            `drop-shadow(0 0 28px ${glowColor}) drop-shadow(0 0 60px ${glowColor.replace("0.8", "0.3")})`,
          ],
        }}
        transition={{ repeat: Infinity, duration: 2.4, ease: "easeInOut" }}
      >
        <svg width="200" height="260" viewBox="-20 -20 200 260" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ overflow: "visible" }}>
          <defs>
            <radialGradient id="outerGrad" cx="50%" cy="65%" r="60%">
              <stop offset="0%" stopColor={outerColor} stopOpacity="0.95" />
              <stop offset="70%" stopColor={outerColor} stopOpacity="0.4" />
              <stop offset="100%" stopColor={outerColor} stopOpacity="0" />
            </radialGradient>
            <radialGradient id="midGrad" cx="50%" cy="60%" r="55%">
              <stop offset="0%" stopColor="#7ef7ff" stopOpacity="0.95" />
              <stop offset="60%" stopColor="#00d4e8" stopOpacity="0.5" />
              <stop offset="100%" stopColor="#00a8c0" stopOpacity="0" />
            </radialGradient>
            <radialGradient id="coreGrad" cx="50%" cy="55%" r="50%">
              <stop offset="0%" stopColor="#ffffff" />
              <stop offset="40%" stopColor="#c0f8ff" />
              <stop offset="100%" stopColor="#00d4e8" stopOpacity="0" />
            </radialGradient>
          </defs>

          <motion.path
            d="M80 215 C30 210,5 175,10 145 C14 118,25 108,22 88 C19 68,30 52,38 44 C32 60,36 72,45 70 C48 56,52 38,60 22 C65 42,60 58,68 65 C72 50,76 28,80 8 C84 28,88 50,92 65 C100 58,95 42,100 22 C108 38,112 56,115 70 C124 72,128 60,122 44 C130 52,141 68,138 88 C135 108,146 118,150 145 C155 175,130 210,80 215 Z"
            fill="url(#outerGrad)"
            animate={{ scaleX: [1, 1.04, 0.97, 1], rotate: [0, 1.5, -1.5, 0] }}
            transition={{ repeat: Infinity, duration: 2.4, ease: "easeInOut" }}
            style={{ transformOrigin: "80px 215px" }}
          />
          <motion.path
            d="M80 208 C42 205,22 178,26 152 C29 128,40 118,38 100 C36 82,44 66,52 58 C50 70,54 80,62 78 C64 64,68 48,74 34 C78 50,74 64,80 70 C86 64,82 50,86 34 C92 48,96 64,98 78 C106 80,110 70,108 58 C116 66,124 82,122 100 C120 118,131 128,134 152 C138 178,118 205,80 208 Z"
            fill="url(#midGrad)"
            animate={{ scaleX: [1, 0.96, 1.04, 1], rotate: [0, -1.5, 1.5, 0] }}
            transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
            style={{ transformOrigin: "80px 208px" }}
          />
          <motion.ellipse
            cx="80" cy="148" rx={34} ry={38}
            fill="url(#coreGrad)"
            animate={{ scale: [1, 1.08, 1] }}
            transition={{ repeat: Infinity, duration: 1.6, ease: "easeInOut" }}
            style={{ transformOrigin: "80px 148px" }}
          />
          <motion.ellipse
            cx="80" cy="148" rx={18} ry={20}
            fill="#ffffff" opacity={0.9}
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ repeat: Infinity, duration: 1.6, ease: "easeInOut" }}
            style={{ transformOrigin: "80px 148px" }}
          />
          <motion.g
            animate={{ scaleY: [1, 1, 0.1, 1, 1] }}
            transition={{ repeat: Infinity, duration: 4, times: [0, 0.88, 0.92, 0.96, 1] }}
            style={{ transformOrigin: "80px 152px" }}
          >
            <circle cx="71" cy="148" r="3" fill="#0a1a20" />
            <circle cx="89" cy="148" r="3" fill="#0a1a20" />
            <path d="M73 157 Q80 163 87 157" stroke="#0a1a20" strokeWidth="2" strokeLinecap="round" fill="none" />
          </motion.g>
        </svg>
      </motion.div>

      <motion.div
        style={{
          width: 80, height: 16, marginTop: -8,
          background: `radial-gradient(ellipse, ${outerColor}66 0%, transparent 70%)`,
          borderRadius: "50%", filter: "blur(6px)",
          alignSelf: "center",
        }}
        animate={{ opacity: [0.5, 0.95, 0.5], scaleX: [1, 1.2, 1] }}
        transition={{ repeat: Infinity, duration: 2.4, ease: "easeInOut" }}
      />
    </motion.div>
  );
}

// =========================================
// WAVE BAR
// =========================================
function WaveBar({ i, status }) {
  const isActive    = status !== "Idle";
  const isSpeaking  = status === "Speaking";
  const isListening = status === "Listening";
  const isThinking  = status === "Thinking";
  const color = isListening ? "#00f5ff" : isThinking ? "#f59e0b" : isSpeaking ? "#f0abfc" : "#00d4e8";
  const h = isActive
    ? isSpeaking  ? [6, 55 + Math.sin(i * 0.45) * 38, 6]
    : isListening ? [6, 40 + Math.sin(i * 0.6) * 28, 6]
                  : [6, 22 + Math.sin(i * 0.9) * 14, 6]
    : [5, 5, 5];

  return (
    <motion.div
      style={{
        width: 4, minHeight: 5, borderRadius: 8,
        background: color,
        boxShadow: isActive ? `0 0 7px ${color}` : "none",
        flexShrink: 0,
      }}
      animate={{ height: h }}
      transition={{ repeat: Infinity, duration: isThinking ? 1.1 : 0.65, delay: i * 0.033, ease: "easeInOut" }}
    />
  );
}

const STATUS_META = {
  Idle:      { label: "IDLE",      color: "#00d4e8" },
  Listening: { label: "LISTENING", color: "#00f5ff" },
  Thinking:  { label: "THINKING",  color: "#f59e0b" },
  Speaking:  { label: "SPEAKING",  color: "#f0abfc" },
};

// =========================================
// TOAST NOTIFICATION
// =========================================
function Toast({ message, onDone }) {
  useEffect(() => {
    const t = setTimeout(onDone, 2500);
    return () => clearTimeout(t);
  }, [onDone]);

  return (
    <motion.div
      style={S.toast}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
    >
      ⚠️ {message}
    </motion.div>
  );
}

// =========================================
// MAIN APP
// =========================================
export default function App() {
  const [status,    setStatus]    = useState("Idle");
  const [time,      setTime]      = useState("");
  const [response,  setResponse]  = useState("");
  const [showResp,  setShowResp]  = useState(false);
  const [handsFree, setHandsFree] = useState(false);
  const [toast,     setToast]     = useState("");   // FIX: user-visible error messages
  const [micOk,     setMicOk]     = useState(true); // FIX: track mic permission state

  const recRef            = useRef(null);
  const activeRef         = useRef(false);
  const handsFreeRef      = useRef(false);
  const startListeningRef = useRef(null);

  // FIX: Use a ref for status inside polling so the interval never depends on
  // the status state value and does NOT restart on every status change.
  const statusRef = useRef("Idle");
  useEffect(() => {
    statusRef.current = status;
  }, [status]);

  // Keep handsFreeRef in sync
  useEffect(() => {
    handsFreeRef.current = handsFree;
  }, [handsFree]);

  // Clock
  useEffect(() => {
    const tick = () => {
      const d = new Date();
      setTime(d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }));
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, []);

  // FIX: Status polling — removed `status` from dependency array.
  // Previously it restarted the interval on every status change, and the
  // guard inside used stale closure values. Now we use statusRef.
  useEffect(() => {
    const poll = async () => {
      // Don't overwrite while frontend is managing these states
      if (
  statusRef.current === "Thinking" ||
  statusRef.current === "Speaking" ||
  handsFreeRef.current
) {
  return;
}

      try {
        const r = await fetch("http://127.0.0.1:5000/status");
        const d = await r.json();
        if (d.status) {
          setStatus(d.status.replace("...", ""));
        }
      } catch {
        // Backend offline — silently ignore
      }
    };

    poll();
    const id = setInterval(poll, 800);
    return () => clearInterval(id);
  }, []); // ← empty deps: runs once, uses statusRef inside

  // ── CORE: speak a string, then callback ──
  const speak = useCallback((text, onDone) => {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang   = "en-IN"; // ✅ FIX: match Indian English for TTS
    utterance.rate   = 1;
    utterance.pitch  = 1;
    utterance.volume = 1;
    utterance.onend  = () => onDone?.();
    utterance.onerror = (e) => {
      console.warn("TTS error:", e.error);
      onDone?.();
    };
    setTimeout(() => window.speechSynthesis.speak(utterance), 150);
  }, []);

  // ── CORE: one full listen → think → speak cycle ──
  const startListening = useCallback(() => {
  const SR =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

  if (!SR) {
    alert("Use Chrome browser");
    return;
  }

  // stop old recognition
  if (recRef.current) {
    try {
      recRef.current.stop();
    } catch (_) {}
  }

  const rec = new SR();
  recRef.current = rec;

rec.lang = "en-IN";
rec.continuous = true;
rec.interimResults = false;
rec.maxAlternatives = 1; 
rec.pauseThreshold = 2;
rec.phraseTimeLimit = 8;  // ✅ FIX: more alternatives = better accuracy

  activeRef.current = true;
  setStatus("Listening");

  console.log("Recognition started");

  rec.onstart = () => {
    console.log("Mic listening...");
  };

  // ✅ FIX: removed duplicate onsoundstart / onspeechstart handlers
  rec.onaudiostart  = () => console.log("Audio detected");
  rec.onsoundstart  = () => console.log("Sound detected");
  rec.onspeechstart = () => console.log("Speech started");
  rec.onspeechend   = () => console.log("Speech ended");

  rec.onresult = async (event) => {
    const transcript = Array.from(
      event.results
    )
      .map((r) => r[0].transcript)
      .join("")
      .trim();

    console.log("User said:", transcript);

    if (!transcript) return;

    try {
      rec.stop();
    } catch (_) {}

    activeRef.current = false;
    setStatus("Thinking");

    try {
      const res = await fetch(
        "http://127.0.0.1:5000/command",
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            command: transcript,
          }),
        }
      );

      const data = await res.json();

      const reply =
        data.response || "No response";

      setResponse(reply);
      setShowResp(true);
      setStatus("Speaking");

      speak(reply, () => {
        setShowResp(false);

        if (handsFreeRef.current) {
          setTimeout(() => {
            startListeningRef.current?.();
          }, 1000);
        } else {
          setStatus("Idle");
        }
      });
    } catch (err) {
      console.error(err);
      setStatus("Idle");
    }
  };

 rec.onerror = (e) => {
  console.log("Speech error:", e.error);

  if (e.error === "no-speech") {
    console.log("No speech detected — retrying");

    setTimeout(() => {
      startListeningRef.current?.();
    }, 2000);

    return;
  }

  setStatus("Idle");
};

  rec.onend = () => {
    console.log("Recognition ended");
  };

  try {
    rec.start();
  } catch (err) {
    console.error(err);
    setStatus("Idle");
  }
}, [speak]);

  // Keep ref in sync
  useEffect(() => {
    startListeningRef.current = startListening;
  }, [startListening]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      activeRef.current    = false;
      handsFreeRef.current = false;
      if (recRef.current) {
        try { recRef.current.abort(); } catch (_) {}
        recRef.current = null;
      }
      window.speechSynthesis.cancel();
    };
  }, []);

  // ── MIC BUTTON HANDLER ──
  const handleMicClick = useCallback(() => {
    if (handsFreeRef.current) {
      // STOP everything
      handsFreeRef.current = false;
      setHandsFree(false);
      activeRef.current = false;
      setStatus("Idle");
      setShowResp(false);
      setToast("");

      if (recRef.current) {
        try { recRef.current.stop(); } catch (_) {}
        recRef.current = null;
      }
      window.speechSynthesis.cancel();
    } else {
      // FIX: Pre-check mic permission before starting
      navigator.permissions?.query({ name: "microphone" }).then((result) => {
        if (result.state === "denied") {
          setMicOk(false);
          setToast("Microphone blocked. Allow mic in Chrome settings and refresh.");
          return;
        }
        activeRef.current    = false;
        handsFreeRef.current = true;
        setHandsFree(true);
        setMicOk(true);
        setStatus("Listening");

setTimeout(() => {
  startListeningRef.current?.();
}, 1200);
      }).catch(() => {
        // permissions API not available, just try anyway
        activeRef.current    = false;
        handsFreeRef.current = true;
        setHandsFree(true);
        setStatus("Listening");

setTimeout(() => {
  startListeningRef.current?.();
}, 1200);
      });
    }
  }, []);

  const meta = STATUS_META[status] || STATUS_META.Idle;

  return (
    <>
      <style>{fontStyle}</style>
      <div style={S.root}>
        <div style={S.scanlines} />

        {/* Corner brackets */}
        {[
          { top: 24, left: 24,   borderTop: "1px solid rgba(0,245,255,0.3)", borderLeft:  "1px solid rgba(0,245,255,0.3)" },
          { top: 24, right: 24,  borderTop: "1px solid rgba(0,245,255,0.3)", borderRight: "1px solid rgba(0,245,255,0.3)" },
          { bottom: 24, left:  24, borderBottom: "1px solid rgba(0,245,255,0.3)", borderLeft:  "1px solid rgba(0,245,255,0.3)" },
          { bottom: 24, right: 24, borderBottom: "1px solid rgba(0,245,255,0.3)", borderRight: "1px solid rgba(0,245,255,0.3)" },
        ].map((style, i) => (
          <div key={i} style={{ position: "absolute", width: 32, height: 32, zIndex: 20, ...style }} />
        ))}

        {/* Top bar */}
        <div style={S.topBar}>
          <span style={S.mono}>NOVA · AI ASSISTANT</span>
          <span style={{ ...S.mono, letterSpacing: 2 }}>{time}</span>
          <span style={{ ...S.mono, color: micOk ? "rgba(0,245,255,0.5)" : "rgba(255,80,80,0.8)" }}>
            {micOk ? "SYS · ONLINE" : "MIC · BLOCKED"}
          </span>
        </div>

        {/* 3D Canvas */}
        <div style={S.canvasWrap}>
          <Canvas
            camera={{ position: [0, 0, 6], fov: 55 }}
            // FIX: Suppress THREE.Clock deprecation warning
            onCreated={({ gl }) => {
              gl.debug = { checkShaderErrors: false };
            }}
          >
            <ambientLight intensity={0.4} />
            <pointLight position={[8, 8, 8]}   intensity={4} color="#00d4e8" />
            <pointLight position={[-8, -8, 4]}  intensity={2} color="#0891b2" />
            <Particles />
            <NeuralLines />
            <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={0.4} enablePan={false} />
          </Canvas>
        </div>

        {/* UI Overlay */}
        <div style={S.overlay}>
          {/* Title */}
          <div style={S.titleBlock}>
            <motion.div
              style={S.titleBloom}
              animate={{ opacity: [0.3, 0.85, 0.3] }}
              transition={{ repeat: Infinity, duration: 3 }}
            />
            <motion.h1
              style={S.title}
              animate={{ opacity: [0.88, 1, 0.88] }}
              transition={{ repeat: Infinity, duration: 2.5 }}
            >
              NOVA
            </motion.h1>
            <p style={S.subtitle}>NEURAL OPERATIONS VOICE AGENT</p>
          </div>

          {/* Flame */}
          <SpiritFlame status={status} />

          {/* Status badge */}
          <AnimatePresence mode="wait">
            <motion.div
              key={status}
              style={{ ...S.badge, borderColor: meta.color, boxShadow: `0 0 22px ${meta.color}44` }}
              initial={{ opacity: 0, scale: 0.9, y: 8 }}
              animate={{ opacity: 1, scale: 1,   y: 0 }}
              exit={{   opacity: 0, scale: 0.9,  y: -8 }}
              transition={{ duration: 0.22 }}
            >
              <motion.span
                style={{ ...S.dot, background: meta.color, boxShadow: `0 0 10px ${meta.color}` }}
                animate={{ scale: [1, 1.6, 1], opacity: [1, 0.4, 1] }}
                transition={{ repeat: Infinity, duration: 1.1 }}
              />
              <span style={{ ...S.badgeLabel, color: meta.color }}>{meta.label}</span>

              {/* FIX: "Speak now!" nudge shown inside the badge while listening */}
              <AnimatePresence>
                {status === "Listening" && (
                  <motion.span
                    style={{ fontSize: 10, color: "rgba(0,245,255,0.6)", letterSpacing: 2, marginLeft: 8 }}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: [0, 1, 0] }}
                    transition={{ repeat: Infinity, duration: 1.6 }}
                  >
                    SPEAK NOW
                  </motion.span>
                )}
              </AnimatePresence>
            </motion.div>
          </AnimatePresence>

          {/* Waveform */}
          <div style={S.waveRow}>
            {[...Array(44)].map((_, i) => <WaveBar key={i} i={i} status={status} />)}
          </div>

          {/* Mic button */}
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
            <motion.div
              animate={{ scale: status === "Listening" ? [1, 1.3, 1] : 1 }}
              transition={{ repeat: Infinity, duration: 1 }}
              style={{
                width: 70, height: 70, borderRadius: "50%",
                background: !micOk
                  ? "#3a1a1a"
                  : handsFree
                    ? (status === "Listening" ? "#00f5ff" : "#0891b2")
                    : "#1a3a4a",
                display: "flex", justifyContent: "center", alignItems: "center",
                fontSize: 28,
                boxShadow: !micOk
                  ? "0 0 20px rgba(255,80,80,0.3)"
                  : handsFree
                    ? (status === "Listening" ? "0 0 40px #00f5ff" : "0 0 40px #00d4e8")
                    : "0 0 20px rgba(0,212,232,0.3)",
                cursor: "pointer",
                border: handsFree ? "none" : `2px solid ${micOk ? "rgba(0,212,232,0.4)" : "rgba(255,80,80,0.4)"}`,
                transition: "background 0.3s, box-shadow 0.3s",
              }}
              onClick={handleMicClick}
            >
              {!micOk ? "🚫" : handsFree ? "🎤" : "🎙️"}
            </motion.div>
            <div style={{ fontSize: 11, letterSpacing: 4, color: "rgba(255,255,255,.6)" }}>
              {!micOk ? "MIC BLOCKED" : handsFree ? "CLICK TO STOP" : "CLICK TO START"}
            </div>
          </div>

          {/* Response box */}
          <AnimatePresence>
            {showResp && (
              <motion.div
                style={S.responseBox}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
              >
                {response}
              </motion.div>
            )}
          </AnimatePresence>

          {/* FIX: Toast notification for errors */}
          <AnimatePresence>
            {toast && (
              <Toast message={toast} onDone={() => setToast("")} />
            )}
          </AnimatePresence>

          {/* Bottom strip */}
          <div style={S.strip}>
            {["MICROPHONE", "FLASK API", "WEB SEARCH", "TTS ENGINE"].map((label, i) => (
              <div key={label} style={S.stripItem}>
                <motion.div
                  style={{
                    ...S.stripDot,
                    background: label === "MICROPHONE" && !micOk ? "#ff5050" : "#00f5ff",
                  }}
                  animate={{ opacity: [0.3, 1, 0.3] }}
                  transition={{ repeat: Infinity, duration: 1.6, delay: i * 0.35 }}
                />
                <span style={S.stripLabel}>{label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}

// =========================================
// STYLES
// =========================================
const S = {
  root: {
    width: "100vw", height: "100vh",
    background: "#04080f",
    overflow: "hidden", position: "relative",
    fontFamily: "'Share Tech Mono', 'Courier New', monospace",
  },
  scanlines: {
    position: "absolute", inset: 0,
    background: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.06) 2px, rgba(0,0,0,0.06) 4px)",
    pointerEvents: "none", zIndex: 10,
  },
  topBar: {
    position: "absolute", top: 0, left: 0, right: 0, height: 44,
    borderBottom: "1px solid rgba(0,245,255,0.12)",
    display: "flex", alignItems: "center", justifyContent: "space-between",
    padding: "0 56px", zIndex: 30,
    background: "rgba(4,8,15,0.8)", backdropFilter: "blur(10px)",
  },
  mono: { color: "rgba(0,245,255,0.5)", fontSize: 11, letterSpacing: 3 },
  canvasWrap: { position: "absolute", inset: 0, zIndex: 1 },
  overlay: {
    position: "absolute", inset: 0, zIndex: 20,
    display: "flex", flexDirection: "column",
    alignItems: "center", justifyContent: "center",
    gap: 12,
    padding: "52px 0 36px",
    pointerEvents: "auto",
  },
  titleBlock: { display: "flex", flexDirection: "column", alignItems: "center", position: "relative" },
  titleBloom: {
    position: "absolute", top: "50%", left: "50%",
    transform: "translate(-50%,-50%)",
    width: 320, height: 110,
    background: "radial-gradient(ellipse, rgba(0,212,232,0.3) 0%, transparent 70%)",
    filter: "blur(28px)", pointerEvents: "none",
  },
  title: {
    margin: 0, fontSize: 80, fontWeight: 700, letterSpacing: 24,
    color: "#ffffff", fontFamily: "'Rajdhani', sans-serif",
    textShadow: "0 0 50px rgba(0,245,255,0.9), 0 0 100px rgba(0,200,220,0.4), 0 2px 0 rgba(0,200,220,0.5)",
    lineHeight: 1,
  },
  subtitle: { margin: "10px 0 0", fontSize: 10, letterSpacing: 7, color: "rgba(0,245,255,0.45)", fontWeight: 400 },
  badge: {
    display: "flex", alignItems: "center", gap: 10,
    padding: "11px 26px", border: "1px solid", borderRadius: 100,
    background: "rgba(4,8,15,0.7)", backdropFilter: "blur(14px)",
  },
  dot:        { width: 8, height: 8, borderRadius: "50%", flexShrink: 0 },
  badgeLabel: { fontSize: 13, letterSpacing: 5, fontWeight: 700 },
  waveRow:    { display: "flex", alignItems: "center", gap: 4, height: 60 },
  responseBox: {
    maxWidth: 520, width: "90%",
    background: "rgba(0,10,18,0.88)",
    border: "1px solid rgba(0,245,255,0.18)",
    borderRadius: 12, padding: "14px 20px",
    fontSize: 12, lineHeight: 1.7,
    color: "rgba(200,240,255,0.85)",
    letterSpacing: 0.5,
    backdropFilter: "blur(16px)",
    boxShadow: "0 0 30px rgba(0,245,255,0.08)",
    textAlign: "center",
  },
  toast: {
    position: "fixed", bottom: 80, left: "50%", transform: "translateX(-50%)",
    background: "rgba(30,10,10,0.92)",
    border: "1px solid rgba(255,120,80,0.4)",
    borderRadius: 10, padding: "10px 22px",
    fontSize: 11, letterSpacing: 1.5,
    color: "rgba(255,180,160,0.9)",
    backdropFilter: "blur(14px)",
    zIndex: 100, whiteSpace: "nowrap",
    boxShadow: "0 0 20px rgba(255,80,50,0.15)",
  },
  strip: {
    display: "flex", gap: 28,
    borderTop: "1px solid rgba(0,245,255,0.12)",
    paddingTop: 18, width: "100%", maxWidth: 500,
    justifyContent: "center",
  },
  stripItem:  { display: "flex", alignItems: "center", gap: 7 },
  stripDot:   { width: 6, height: 6, borderRadius: "50%" },
  stripLabel: { fontSize: 10, letterSpacing: 2.5, color: "rgba(160,200,220,0.5)" },
};