import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Agentation } from 'agentation';

const STORAGE_KEY = 'recatch-bulk-import-agentation-session-id';
const ENDPOINT = 'http://localhost:4747';

function emit(name, detail) {
  window.dispatchEvent(new CustomEvent(name, { detail }));
}

async function postJson(url, payload) {
  try {
    await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
  } catch (error) {
    console.warn('Agentation callback failed', error);
  }
}

function AgentationBridge() {
  const initialSessionId = useMemo(() => window.localStorage.getItem(STORAGE_KEY) || '', []);
  const [sessionId, setSessionId] = useState(initialSessionId);

  useEffect(() => {
    emit('agentation:session', {
      sessionId: sessionId || null,
      endpoint: ENDPOINT,
    });
  }, [sessionId]);

  return (
    <Agentation
      endpoint={ENDPOINT}
      sessionId={sessionId || undefined}
      onSessionCreated={(nextSessionId) => {
        window.localStorage.setItem(STORAGE_KEY, nextSessionId);
        setSessionId(nextSessionId);
        emit('agentation:session', {
          sessionId: nextSessionId,
          endpoint: ENDPOINT,
        });
        postJson('/api/agentation/session', {
          session_id: nextSessionId,
          endpoint: ENDPOINT,
          created_at: new Date().toISOString(),
        });
      }}
      onSubmit={(output, annotations) => {
        const payload = {
          session_id: window.localStorage.getItem(STORAGE_KEY) || sessionId || '',
          endpoint: ENDPOINT,
          output,
          annotations,
          created_at: new Date().toISOString(),
          url: window.location.href,
        };
        emit('agentation:submit', payload);
        postJson('/api/agentation/submit', payload);
      }}
    />
  );
}

function mount() {
  let container = document.getElementById('agentation-root');
  if (!container) {
    container = document.createElement('div');
    container.id = 'agentation-root';
    document.body.appendChild(container);
  }
  createRoot(container).render(<AgentationBridge />);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', mount, { once: true });
} else {
  mount();
}
