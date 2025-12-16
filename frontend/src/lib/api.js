// lib/api.js
const API_ROOT = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function postDetect(blob, conf = 0.45) {
  const form = new FormData();
  form.append("file", blob, "frame.png");
  // add conf if you want as query param
  const res = await fetch(`${API_ROOT}/detect?conf=${conf}`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Detect failed: ${res.status} ${text}`);
  }
  return res.json();
}

export async function postScanFace(session_id, face, colors) {
  const res = await fetch(`${API_ROOT}/scan_face`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id, face, colors }),
  });
  return res.json();
}

export async function getState(session_id) {
  const res = await fetch(`${API_ROOT}/session/${session_id}/state`);
  return res.json();
}

export async function getKociemba(session_id) {
  const res = await fetch(`${API_ROOT}/session/${session_id}/kociemba`);
  return res.json();
}

export async function getSolve(session_id) {
  const res = await fetch(`${API_ROOT}/session/${session_id}/solve`);
  return res.json();
}