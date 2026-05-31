(function () {
  const root = window.SITE_ROOT || "";
  const body = document.body;
  const searchInput = document.getElementById("siteSearch");
  const searchResults = document.getElementById("searchResults");
  let searchIndex = null;

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
    if (!query) {
      searchResults.hidden = true;
      searchResults.innerHTML = "";
      return;
    }
    if (!items.length) {
      searchResults.hidden = false;
      searchResults.innerHTML = '<div class="search-result"><strong>没有匹配结果</strong><span>换一个关键词或题号试试。</span></div>';
      return;
    }
    searchResults.hidden = false;
    searchResults.innerHTML = items
      .slice(0, 12)
      .map((item) => {
        const url = root + item.url;
        return `<a class="search-result" href="${url}"><strong>${item.title}</strong><small>${item.group} · ${item.path}</small><span>${item.text || ""}</span></a>`;
      })
      .join("");
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
          const haystack = normalize([item.title, item.group, item.path, item.text, item.search].join(" "));
          const score = tokens.reduce((sum, token) => sum + (haystack.includes(token) ? 1 : 0), 0);
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
  }

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

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupMermaid);
  } else {
    setupMermaid();
  }
})();
