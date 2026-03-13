const choiceMessages = {
  tracking: "실시간 트래킹 여정: 클릭, 스크롤, CTA 진입 시점을 빠르게 모니터링하는 시나리오입니다.",
  automation: "자동화 연결 여정: 상담 요청 후 후속 액션으로 어떻게 이어지는지 테스트하는 시나리오입니다.",
  reporting: "리포트 분석 여정: 중간 탐색 행동이 어떤 전환 흐름으로 이어지는지 점검하는 시나리오입니다.",
};

const choiceButtons = Array.from(document.querySelectorAll("[data-choice]"));
const choiceCopy = document.querySelector("#choice-copy");
const planCards = Array.from(document.querySelectorAll("[data-plan-card]"));
const selectedPlan = document.querySelector("#selected-plan");
const embedModal = document.querySelector("#embed-modal");
const embedTriggers = Array.from(document.querySelectorAll("[data-open-embed]"));
const embedClosers = Array.from(document.querySelectorAll("[data-close-embed]"));

for (const button of choiceButtons) {
  button.addEventListener("click", () => {
    for (const candidate of choiceButtons) {
      candidate.classList.toggle("is-active", candidate === button);
    }
    if (choiceCopy) {
      choiceCopy.textContent = choiceMessages[button.dataset.choice] || "";
    }
  });
}

for (const card of planCards) {
  const action = card.querySelector(".select-plan");
  if (!action) {
    continue;
  }
  action.addEventListener("click", () => {
    for (const candidate of planCards) {
      candidate.classList.toggle("is-selected", candidate === card);
    }
    const title = card.querySelector("h3");
    if (selectedPlan && title) {
      selectedPlan.textContent = `현재 선택: ${title.textContent}`;
    }
  });
}

for (const trigger of document.querySelectorAll("[data-scroll-target]")) {
  trigger.addEventListener("click", () => {
    const target = document.querySelector(trigger.getAttribute("data-scroll-target") || "");
    target?.scrollIntoView({ behavior: "smooth", block: "start" });
  });
}

function setEmbedModalOpen(isOpen) {
  if (!embedModal) {
    return;
  }
  embedModal.hidden = !isOpen;
  document.body.classList.toggle("modal-open", isOpen);
}

for (const trigger of embedTriggers) {
  trigger.addEventListener("click", () => {
    setEmbedModalOpen(true);
  });
}

for (const trigger of embedClosers) {
  trigger.addEventListener("click", () => {
    setEmbedModalOpen(false);
  });
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    setEmbedModalOpen(false);
  }
});

if (embedModal) {
  embedModal.addEventListener("click", (event) => {
    if (event.target === embedModal) {
      setEmbedModalOpen(false);
    }
  });
}
