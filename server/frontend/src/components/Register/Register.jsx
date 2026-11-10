import React, { useState } from "react";
import Header from "../Header/Header";
import "./Register.css";

export default function Register() {
  const [form, setForm] = useState({
    userName: "", firstName: "", lastName: "", email: "", password: "",
  });
  const [error, setError] = useState("");

  const update = (event) => setForm({ ...form, [event.target.name]: event.target.value });
  const submit = async (event) => {
    event.preventDefault();
    setError("");
    const response = await fetch("/djangoapp/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    const result = await response.json();
    if (!response.ok) {
      setError(result.error || "Registration failed.");
      return;
    }
    sessionStorage.setItem("username", result.userName);
    window.location.href = "/dealers";
  };

  return <div><Header /><main className="register_container">
    <h1 className="header">Sign-up</h1>
    <form className="inputs" onSubmit={submit}>
      <label>Username <input className="input_field" name="userName" required value={form.userName} onChange={update} /></label>
      <label>First Name <input className="input_field" name="firstName" required value={form.firstName} onChange={update} /></label>
      <label>Last Name <input className="input_field" name="lastName" required value={form.lastName} onChange={update} /></label>
      <label>Email <input className="input_field" type="email" name="email" required value={form.email} onChange={update} /></label>
      <label>Password <input className="input_field" type="password" name="password" required minLength="8" value={form.password} onChange={update} /></label>
      {error && <p role="alert">{error}</p>}
      <button className="submit" type="submit">Register</button>
    </form>
  </main></div>;
}
