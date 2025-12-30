const token = localStorage.getItem("token");

let page = 1;
const limit = 20;

if (!token) {
  alert("Not logged in");
  window.location.href = "/static/login.html";
}

// 🔹 Load table list on startup
window.onload = async () => {
  const res = await fetch("/api/tables", {
    headers: { Authorization: "Bearer " + token }
  });

  if (!res.ok) {
    alert("Failed to load tables");
    return;
  }

  const tables = await res.json();
  const select = document.getElementById("tableSelect");

  tables.forEach(t => {
    const opt = document.createElement("option");
    opt.value = t;
    opt.textContent = t;
    select.appendChild(opt);
  });
};

async function loadTable() {
  const table = document.getElementById("tableSelect").value;
  const search = document.getElementById("searchBox").value;

  const res = await fetch(
    `/api/tables/${table}?page=${page}&limit=${limit}&search=${encodeURIComponent(search)}`,
    { headers: { Authorization: "Bearer " + token } }
  );

  const rows = await res.json();
  renderTable(rows);
  document.getElementById("pageInfo").innerText = `Page ${page}`;
}

function renderTable(rows) {
  const tableEl = document.getElementById("dataTable");
  tableEl.innerHTML = "";

  if (!rows || rows.length === 0) {
    tableEl.innerHTML = "<tr><td>No data</td></tr>";
    return;
  }

  const header = document.createElement("tr");
  Object.keys(rows[0]).forEach(col => {
    const th = document.createElement("th");
    th.textContent = col;
    header.appendChild(th);
  });
  tableEl.appendChild(header);

  rows.forEach(row => {
    const tr = document.createElement("tr");
    Object.values(row).forEach(val => {
      const td = document.createElement("td");
      td.textContent = val;
      tr.appendChild(td);
    });
    tableEl.appendChild(tr);
  });
}

function nextPage() {
  page++;
  loadTable();
}

function prevPage() {
  if (page > 1) page--;
  loadTable();
}

async function downloadCSV() {
  const table = document.getElementById("tableSelect").value;

  const res = await fetch(`/api/tables/${table}/csv`, {
    headers: { Authorization: "Bearer " + token }
  });

  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${table}.csv`;
  a.click();
}

async function savePerm() {
  const payload = {
    user_id: document.getElementById("uid").value,
    table: document.getElementById("ptable").value,
    can_read: document.getElementById("read").checked,
    can_export: document.getElementById("export").checked
  };

  const res = await fetch("/api/permissions", {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + token,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (res.ok) alert("Permission saved");
  else alert("Failed to save permission");
}
