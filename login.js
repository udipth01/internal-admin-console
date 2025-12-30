async function login() {
  const username = document.querySelector('input[placeholder="Username"]').value;
  const password = document.querySelector('input[placeholder="Password"]').value;

  const res = await fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();

  if (!res.ok) {
    document.getElementById("error").innerText = data.error;
    return;
  }

  localStorage.setItem("admin_token", data.token);
  window.location.href = "/static/dashboard.html";
}
