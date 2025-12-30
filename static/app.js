document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault(); // 🔴 VERY IMPORTANT

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();

  if (!res.ok) {
    document.getElementById("error").innerText =
      data.detail || "Login failed";
    return;
  }

  // ✅ store JWT
  localStorage.setItem("token", data.token);

  // ✅ redirect after login
  window.location.href = "/static/index.html";
});
