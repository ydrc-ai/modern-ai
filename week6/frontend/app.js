const notesState = { page: 1, pageSize: 5, q: "", sort: "created_desc", total: 0 };
const actionsState = { page: 1, pageSize: 5, filter: "all", total: 0, selected: new Set() };

async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  if (res.status === 204) return null;
  return res.json();
}

function notesQuery() {
  const params = new URLSearchParams({
    page: String(notesState.page),
    page_size: String(notesState.pageSize),
    sort: notesState.sort,
  });
  if (notesState.q.trim()) params.set("q", notesState.q.trim());
  const path = notesState.q.trim() ? "/notes/search/" : "/notes/";
  return `${path}?${params.toString()}`;
}

function actionsQuery() {
  const params = new URLSearchParams({
    page: String(actionsState.page),
    page_size: String(actionsState.pageSize),
  });
  if (actionsState.filter === "open") params.set("completed", "false");
  if (actionsState.filter === "done") params.set("completed", "true");
  return `/action-items/?${params.toString()}`;
}

async function loadNotes() {
  const list = document.getElementById("notes");
  const count = document.getElementById("note-count");
  const pageLabel = document.getElementById("notes-page-label");
  list.innerHTML = "";
  const body = await fetchJSON(notesQuery());
  notesState.total = body.total;
  count.textContent = `${body.total} result${body.total === 1 ? "" : "s"}`;
  pageLabel.textContent = `Page ${body.page}`;
  document.getElementById("notes-prev").disabled = body.page <= 1;
  document.getElementById("notes-next").disabled =
    body.page * body.page_size >= body.total;

  for (const n of body.items) {
    list.appendChild(renderNote(n));
  }
}

function renderNote(n) {
  const li = document.createElement("li");
  li.dataset.id = String(n.id);

  const body = document.createElement("div");
  body.className = "body";

  const titleInput = document.createElement("input");
  titleInput.value = n.title;
  titleInput.setAttribute("aria-label", "Note title");

  const contentInput = document.createElement("input");
  contentInput.value = n.content;
  contentInput.setAttribute("aria-label", "Note content");

  const err = document.createElement("div");
  err.className = "error";

  body.append(titleInput, contentInput, err);

  const actions = document.createElement("div");
  actions.className = "row-actions";

  const saveBtn = document.createElement("button");
  saveBtn.type = "button";
  saveBtn.textContent = "Save";
  saveBtn.onclick = async () => {
    const previous = { title: n.title, content: n.content };
    const next = { title: titleInput.value, content: contentInput.value };
    // Optimistic update
    n.title = next.title;
    n.content = next.content;
    err.textContent = "";
    try {
      const updated = await fetchJSON(`/notes/${n.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(next),
      });
      n.title = updated.title;
      n.content = updated.content;
      titleInput.value = updated.title;
      contentInput.value = updated.content;
    } catch (e) {
      n.title = previous.title;
      n.content = previous.content;
      titleInput.value = previous.title;
      contentInput.value = previous.content;
      err.textContent = "Save failed — rolled back.";
    }
  };

  const extractBtn = document.createElement("button");
  extractBtn.type = "button";
  extractBtn.textContent = "Extract";
  extractBtn.onclick = async () => {
    err.textContent = "";
    try {
      const result = await fetchJSON(`/notes/${n.id}/extract?apply=true`, {
        method: "POST",
      });
      err.textContent = `Extracted ${result.action_items.length} action(s), tags: ${
        result.hashtags.join(", ") || "none"
      }`;
      await loadActions();
    } catch (e) {
      err.textContent = "Extract failed.";
    }
  };

  const delBtn = document.createElement("button");
  delBtn.type = "button";
  delBtn.textContent = "Delete";
  delBtn.onclick = async () => {
    const snapshot = li.cloneNode(true);
    li.remove();
    notesState.total = Math.max(0, notesState.total - 1);
    document.getElementById("note-count").textContent =
      `${notesState.total} result${notesState.total === 1 ? "" : "s"}`;
    try {
      await fetchJSON(`/notes/${n.id}`, { method: "DELETE" });
      await loadNotes();
    } catch (e) {
      list.prepend(snapshot);
      err.textContent = "Delete failed — restored.";
      await loadNotes();
    }
  };

  actions.append(saveBtn, extractBtn, delBtn);
  li.append(body, actions);
  return li;
}

async function loadActions() {
  const list = document.getElementById("actions");
  const count = document.getElementById("action-count");
  const pageLabel = document.getElementById("actions-page-label");
  list.innerHTML = "";
  actionsState.selected.clear();
  const body = await fetchJSON(actionsQuery());
  actionsState.total = body.total;
  count.textContent = `${body.total} item${body.total === 1 ? "" : "s"}`;
  pageLabel.textContent = `Page ${body.page}`;
  document.getElementById("actions-prev").disabled = body.page <= 1;
  document.getElementById("actions-next").disabled =
    body.page * body.page_size >= body.total;

  for (const a of body.items) {
    list.appendChild(renderAction(a));
  }
}

function renderAction(a) {
  const li = document.createElement("li");
  const check = document.createElement("input");
  check.type = "checkbox";
  check.disabled = a.completed;
  check.onchange = () => {
    if (check.checked) actionsState.selected.add(a.id);
    else actionsState.selected.delete(a.id);
  };

  const body = document.createElement("div");
  body.className = "body";
  body.textContent = `${a.description} [${a.completed ? "done" : "open"}]`;

  const actions = document.createElement("div");
  actions.className = "row-actions";
  if (!a.completed) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = "Complete";
    btn.onclick = async () => {
      await fetchJSON(`/action-items/${a.id}/complete`, { method: "PUT" });
      await loadActions();
    };
    actions.appendChild(btn);
  }

  li.append(check, body, actions);
  return li;
}

window.addEventListener("DOMContentLoaded", () => {
  document.getElementById("note-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = document.getElementById("note-title").value;
    const content = document.getElementById("note-content").value;
    await fetchJSON("/notes/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, content }),
    });
    e.target.reset();
    notesState.page = 1;
    await loadNotes();
  });

  document.getElementById("action-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const description = document.getElementById("action-desc").value;
    await fetchJSON("/action-items/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description }),
    });
    e.target.reset();
    actionsState.page = 1;
    await loadActions();
  });

  let searchTimer;
  document.getElementById("note-search").addEventListener("input", (e) => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      notesState.q = e.target.value;
      notesState.page = 1;
      loadNotes();
    }, 200);
  });

  document.getElementById("note-sort").addEventListener("change", (e) => {
    notesState.sort = e.target.value;
    notesState.page = 1;
    loadNotes();
  });

  document.getElementById("notes-prev").onclick = () => {
    notesState.page = Math.max(1, notesState.page - 1);
    loadNotes();
  };
  document.getElementById("notes-next").onclick = () => {
    notesState.page += 1;
    loadNotes();
  };

  document.querySelectorAll('input[name="action-filter"]').forEach((el) => {
    el.addEventListener("change", (e) => {
      if (!e.target.checked) return;
      actionsState.filter = e.target.value;
      actionsState.page = 1;
      loadActions();
    });
  });

  document.getElementById("actions-prev").onclick = () => {
    actionsState.page = Math.max(1, actionsState.page - 1);
    loadActions();
  };
  document.getElementById("actions-next").onclick = () => {
    actionsState.page += 1;
    loadActions();
  };

  document.getElementById("bulk-complete").onclick = async () => {
    const ids = [...actionsState.selected];
    if (!ids.length) return;
    await fetchJSON("/action-items/bulk-complete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ids }),
    });
    await loadActions();
  };

  loadNotes();
  loadActions();
});
