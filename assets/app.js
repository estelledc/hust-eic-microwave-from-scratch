(function () {
  const root = window.SITE_ROOT || "";
  const body = document.body;
  const searchInput = document.getElementById("siteSearch");
  const searchResults = document.getElementById("searchResults");
  const progressBar = document.querySelector(".reading-progress span");
  let searchIndex = null;
  let activeSearchIndex = -1;

  function applyTheme(theme) {
    if (theme === "dark") {
      document.documentElement.setAttribute("data-theme", "dark");
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
  }

  const savedTheme = localStorage.getItem("mw-theme");
  if (savedTheme) {
    applyTheme(savedTheme);
  }

  document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      localStorage.setItem("mw-theme", next);
      applyTheme(next);
    });
  });

  document.querySelectorAll("[data-sidebar-toggle]").forEach((button) => {
    button.addEventListener("click", () => body.classList.add("sidebar-open"));
  });

  document.querySelectorAll("[data-sidebar-close]").forEach((button) => {
    button.addEventListener("click", () => body.classList.remove("sidebar-open"));
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "/" && searchInput && document.activeElement !== searchInput) {
      const tag = document.activeElement && document.activeElement.tagName;
      if (!["INPUT", "TEXTAREA"].includes(tag)) {
        event.preventDefault();
        searchInput.focus();
      }
    }
    if (event.key === "Escape") {
      body.classList.remove("sidebar-open");
      if (searchResults) {
        searchResults.hidden = true;
      }
    }
  });

  function normalize(value) {
    return value.toLowerCase().replace(/\s+/g, " ").trim();
  }

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function updateReadingProgress() {
    if (!progressBar) {
      return;
    }
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const percent = scrollable > 0 ? Math.min(1, Math.max(0, window.scrollY / scrollable)) : 0;
    progressBar.style.transform = `scaleX(${percent})`;
  }

  updateReadingProgress();
  window.addEventListener("scroll", updateReadingProgress, { passive: true });
  window.addEventListener("resize", updateReadingProgress);

  async function ensureSearchIndex() {
    if (searchIndex) {
      return searchIndex;
    }
    const response = await fetch(root + "search-index.json");
    searchIndex = await response.json();
    return searchIndex;
  }

  function renderSearchResults(items, query) {
    if (!searchResults) {
      return;
    }
    activeSearchIndex = -1;
    if (!query) {
      searchResults.hidden = true;
      searchResults.innerHTML = "";
      return;
    }
    if (!items.length) {
      searchResults.hidden = false;
      searchResults.innerHTML = '<div class="search-status">没有匹配结果，换一个关键词或题号试试。</div>';
      return;
    }
    const visibleItems = items.slice(0, 12);
    searchResults.hidden = false;
    searchResults.innerHTML =
      `<div class="search-status">找到 ${items.length} 个结果，显示前 ${visibleItems.length} 个。按 ↑/↓ 选择，Enter 打开。</div>` +
      visibleItems
      .map((item, index) => {
        const url = root + item.url;
        return `<a class="search-result" href="${url}" data-search-index="${index}"><strong>${escapeHtml(item.title)}</strong><small><b>${escapeHtml(item.group)}</b>${escapeHtml(item.path)}</small><span>${escapeHtml(item.text)}</span></a>`;
      })
      .join("");
  }

  function moveSearchSelection(delta) {
    if (!searchResults || searchResults.hidden) {
      return;
    }
    const results = Array.from(searchResults.querySelectorAll(".search-result[href]"));
    if (!results.length) {
      return;
    }
    activeSearchIndex = (activeSearchIndex + delta + results.length) % results.length;
    results.forEach((result, index) => {
      result.classList.toggle("active", index === activeSearchIndex);
      if (index === activeSearchIndex) {
        result.scrollIntoView({ block: "nearest" });
      }
    });
  }

  if (searchInput && searchResults) {
    searchInput.addEventListener("input", async () => {
      const query = normalize(searchInput.value);
      if (query.length < 2) {
        renderSearchResults([], "");
        return;
      }
      const index = await ensureSearchIndex();
      const tokens = query.split(" ");
      const matches = index
        .map((item) => {
          const title = normalize(item.title);
          const group = normalize(item.group);
          const path = normalize(item.path);
          const text = normalize(item.text);
          const search = normalize(item.search);
          const score = tokens.reduce((sum, token) => {
            return sum
              + (title.includes(token) ? 6 : 0)
              + (path.includes(token) ? 4 : 0)
              + (group.includes(token) ? 3 : 0)
              + (text.includes(token) ? 2 : 0)
              + (search.includes(token) ? 1 : 0);
          }, 0);
          return { item, score };
        })
        .filter((entry) => entry.score > 0)
        .sort((a, b) => b.score - a.score || a.item.path.localeCompare(b.item.path, "zh-CN"))
        .map((entry) => entry.item);
      renderSearchResults(matches, query);
    });

    document.addEventListener("click", (event) => {
      if (!searchResults.contains(event.target) && event.target !== searchInput) {
        searchResults.hidden = true;
      }
    });

    searchInput.addEventListener("keydown", (event) => {
      if (event.key === "ArrowDown") {
        event.preventDefault();
        moveSearchSelection(1);
      } else if (event.key === "ArrowUp") {
        event.preventDefault();
        moveSearchSelection(-1);
      } else if (event.key === "Enter" && activeSearchIndex >= 0) {
        const active = searchResults.querySelector(".search-result.active");
        if (active) {
          event.preventDefault();
          active.click();
        }
      }
    });
  }

  document.querySelectorAll(".sidebar a").forEach((link) => {
    link.addEventListener("click", () => body.classList.remove("sidebar-open"));
  });

  function setupMermaid() {
    document.querySelectorAll("pre > code.language-mermaid").forEach((code) => {
      const block = document.createElement("div");
      block.className = "mermaid";
      block.textContent = code.textContent;
      code.parentElement.replaceWith(block);
    });
    if (window.mermaid) {
      const explicitTheme = document.documentElement.getAttribute("data-theme");
      const isDark = explicitTheme === "dark"
        || (!explicitTheme && window.matchMedia("(prefers-color-scheme: dark)").matches);
      window.mermaid.initialize({
        startOnLoad: true,
        securityLevel: "loose",
        theme: isDark ? "dark" : "base",
      });
    }
  }

  function setupFormulaQuickView() {
    const toggle = document.querySelector("[data-formula-quick-toggle]");
    const grid = document.getElementById("formula-quick-grid");
    if (!toggle || !grid) {
      return;
    }

    async function typesetGridIfNeeded() {
      if (!grid.hasAttribute("data-math-pending")) {
        return;
      }
      const deadline = Date.now() + 10000;
      while (!(window.MathJax && typeof window.MathJax.typesetPromise === "function")) {
        if (Date.now() >= deadline) {
          return;
        }
        await new Promise((resolve) => window.setTimeout(resolve, 50));
      }
      await window.MathJax.typesetPromise([grid]);
      grid.removeAttribute("data-math-pending");
    }

    function setQuickView(active) {
      body.classList.toggle("formula-quick-active", active);
      toggle.setAttribute("aria-pressed", active ? "true" : "false");
      toggle.textContent = active ? "返回全文" : "公式速查";
      grid.hidden = !active;
      grid.setAttribute("aria-hidden", active ? "false" : "true");
      if (active) {
        typesetGridIfNeeded();
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
    }

    toggle.addEventListener("click", () => {
      setQuickView(!body.classList.contains("formula-quick-active"));
    });
  }

  function setupPageEnhancements() {
    setupMermaid();
    setupFormulaQuickView();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupPageEnhancements);
  } else {
    setupPageEnhancements();
  }
})();
