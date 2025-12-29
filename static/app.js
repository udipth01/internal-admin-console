let currentPage = 1;
const pageSize = 25;

async function loadTables() {
  const res = await fetch("/tables", {
    headers: { Authorization: "Bearer " + localStorage.token }
  });
  const tables = await res.json();
  const sel = document.getElementById("tableSelect");
  sel.innerHTML = "";
  tables.forEach(t => sel.innerHTML += `<option>${t}</option>`);
}

async function loadTable() {
  const table = tableSelect.value;
  const q = searchBox.value || "";
  const res = await fetch(
    `/table/${table}?page=${currentPage}&page_size=${pageSize}&q=${q}`,
    { headers: { Authorization: "Bearer " + localStorage.token } }
  );
  const data = await res.json();
  output.textContent = JSON.stringify(data.data, null, 2);
  pageInfo.textContent =
    `Page ${data.page} of ${Math.ceil(data.total / pageSize)}`;
}

function nextPage() { currentPage++; loadTable(); }
function prevPage() { if (currentPage > 1) currentPage--; loadTable(); }

function downloadCSV() {
  const table = tableSelect.value;
  window.open(`/table/${table}/csv`, "_blank");
}

async function savePerm() {
  await fetch("/admin/permission", {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + localStorage.token,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      user_id: uid.value,
      table_name: ptable.value,
      can_read: read.checked,
      can_export: export.checked
    })
  });
  alert("Permission saved");
}

if (document.getElementById("tableSelect")) loadTables();
