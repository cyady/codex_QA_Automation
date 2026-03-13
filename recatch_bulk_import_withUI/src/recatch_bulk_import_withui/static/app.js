const bootstrap = JSON.parse(document.getElementById("bootstrap-data").textContent);
const state = {
  headers: [],
  preview: null,
};

function el(id) {
  return document.getElementById(id);
}

function showMessage(message, type = "info") {
  const box = el("form-message");
  box.className = `message-box ${type}`;
  box.textContent = message;
}

function currentFormPayload() {
  return {
    env_file: el("env-file").value.trim(),
    source_csv: el("source-csv").value.trim(),
    csv_dir: el("csv-dir").value.trim(),
    file_prefix: el("file-prefix").value.trim(),
    start: Number(el("start-part").value || 1),
    end: Number(el("end-part").value || 0),
    reset_state: el("reset-state").checked,
  };
}

function renderMappingRows(headers, defaultMappings) {
  state.headers = headers;
  const body = el("mapping-table-body");
  body.innerHTML = "";

  headers.forEach((header) => {
    const defaults = defaultMappings[header] || { query: "", option_text: "" };
    const row = document.createElement("tr");
    row.innerHTML = `
      <td><code>${header}</code></td>
      <td><input type="text" data-role="query" data-header="${header}" value="${defaults.query || ""}" placeholder="예: 이메일"></td>
      <td><input type="text" data-role="option" data-header="${header}" value="${defaults.option_text || ""}" placeholder="예: 이메일"></td>
      <td class="skip-cell"><input type="checkbox" data-role="skip" data-header="${header}"></td>
    `;
    body.appendChild(row);
  });
}

function renderPreview(preview) {
  state.preview = preview;
  renderMappingRows(preview.headers, preview.default_mappings || {});
  const metaLines = [];
  metaLines.push(`헤더 수: ${preview.headers.length}`);
  metaLines.push(`헤더 소스: ${preview.source}`);
  if (preview.mode === "split_files") {
    metaLines.push(`감지된 split 파일 수: ${preview.part_count}`);
    metaLines.push(`가능 범위: ${preview.first_part} ~ ${preview.last_part}`);
  }
  metaLines.push(`split 저장/조회 디렉터리: ${preview.split_output_dir}`);
  el("mapping-meta").textContent = metaLines.join(" | ");
}

function collectMappingRows() {
  return state.headers.map((header) => {
    const query = document.querySelector(`input[data-role="query"][data-header="${header}"]`);
    const option = document.querySelector(`input[data-role="option"][data-header="${header}"]`);
    const skip = document.querySelector(`input[data-role="skip"][data-header="${header}"]`);
    return {
      csv_header: header,
      query: query ? query.value.trim() : "",
      option_text: option ? option.value.trim() : "",
      skip: skip ? skip.checked : false,
    };
  });
}

async function loadHeaders() {
  showMessage("CSV 헤더를 확인하는 중입니다.", "info");
  const response = await fetch("/api/headers", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(currentFormPayload()),
  });
  const payload = await response.json();
  if (!response.ok || !payload.ok) {
    showMessage(payload.error || "헤더를 불러오지 못했습니다.", "error");
    return;
  }
  renderPreview(payload);
  showMessage("헤더를 불러왔습니다. 이제 필드 매핑을 확인한 뒤 임포트를 시작하세요.", "success");
}

async function startJob() {
  if (!state.headers.length) {
    showMessage("먼저 CSV 헤더를 불러오세요.", "error");
    return;
  }
  showMessage("작업을 시작하는 중입니다.", "info");
  const payload = {
    ...currentFormPayload(),
    mapping_rows: collectMappingRows(),
  };
  const response = await fetch("/api/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const body = await response.json();
  if (!response.ok || !body.ok) {
    showMessage(body.error || "작업 시작에 실패했습니다.", "error");
    return;
  }
  showMessage(body.message || "작업을 시작했습니다.", "success");
  renderStatus(body);
}

async function stopJob() {
  const response = await fetch("/api/stop", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  const payload = await response.json();
  if (!response.ok || !payload.ok) {
    showMessage(payload.error || "중지 요청에 실패했습니다.", "error");
    return;
  }
  showMessage(payload.message || "중지 요청을 보냈습니다.", "success");
}

function renderStatus(payload) {
  const progress = payload.progress || {};
  const percent = Number(progress.percent || 0);
  el("status-label").textContent = payload.status || "idle";
  el("phase-label").textContent = payload.phase || "idle";
  el("progress-label").textContent = `${percent.toFixed(2)}%`;
  el("progress-count").textContent = `${progress.completed_count || 0} / ${progress.total_parts || 0} parts`;
  el("progress-bar").style.width = `${Math.min(Math.max(percent, 0), 100)}%`;
  el("last-completed").textContent = progress.last_completed_part ?? "-";
  el("next-pending").textContent = progress.next_pending_part ?? "-";
  el("restart-label").textContent = progress.recommended_restart_start
    ? `${progress.recommended_restart_start} ~ ${payload.end || "?"}`
    : "-";
  el("log-file").textContent = payload.log_file || "-";
  el("state-file").textContent = payload.state_file || "-";
  el("log-tail").textContent = payload.log_tail || "로그가 아직 없습니다.";

  if (payload.status === "failed") {
    showMessage(`작업 실패: ${payload.last_error || "원인 미상"}`, "error");
  }
}

async function refreshStatus() {
  const response = await fetch("/api/status");
  const payload = await response.json();
  renderStatus(payload);
}

function bindEvents() {
  el("load-headers-btn").addEventListener("click", loadHeaders);
  el("start-btn").addEventListener("click", startJob);
  el("stop-btn").addEventListener("click", stopJob);
  window.addEventListener("agentation:session", (event) => {
    const detail = event.detail || {};
    el("agentation-session").textContent = detail.sessionId || "-";
    el("agentation-endpoint").textContent = detail.endpoint || "http://localhost:4747";
  });
  window.addEventListener("agentation:submit", (event) => {
    const detail = event.detail || {};
    const count = Array.isArray(detail.annotations) ? detail.annotations.length : 0;
    showMessage(`Agentation 피드백 수신: annotations ${count}개`, "success");
  });
}

function init() {
  bindEvents();
  renderStatus(bootstrap.status || {});
  setInterval(refreshStatus, 3000);
}

init();
