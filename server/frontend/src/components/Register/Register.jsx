import { useState } from "react";

function getCookie(name) {
    const cookies = document.cookie.split("; ");
    const cookie = cookies.find((item) => item.startsWith(`${name}=`));
    return cookie ? decodeURIComponent(cookie.split("=")[1]) : "";
}

export default function Register() {
    const [form, setForm] = useState({
        username: "",
        firstName: "",
        lastName: "",
        email: "",
        password: "",
    });
    const [error, setError] = useState("");
    const [success, setSuccess] = useState(false);

    function updateField(event) {
        setForm({ ...form, [event.target.name]: event.target.value });
    }

    async function handleSubmit(event) {
        event.preventDefault();
        setError("");
        setSuccess(false);

        try {
            const response = await fetch("/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({
                    username: form.username,
                    first_name: form.firstName,
                    last_name: form.lastName,
                    email: form.email,
                    password: form.password,
                }),
            });
            const data = await response.json();
            if (!response.ok) {
                setError(data.error || "Unable to create your account.");
                return;
            }
            setSuccess(true);
        } catch {
            setError("The server is unavailable. Please try again.");
        }
    }

    return (
        <section className="register-page" aria-labelledby="register-heading">
            <div className="register-panel">
                <p className="eyebrow">Join Best Cars</p>
                <h1 id="register-heading">Sign-up</h1>
                <p className="register-intro">Create your account to save cars and connect with trusted dealers.</p>
                <form className="register-form" onSubmit={handleSubmit}>
                    <label htmlFor="username">Username</label>
                    <input id="username" name="username" type="text" value={form.username} onChange={updateField} autoComplete="username" required />

                    <label htmlFor="firstName">First Name</label>
                    <input id="firstName" name="firstName" type="text" value={form.firstName} onChange={updateField} autoComplete="given-name" required />

                    <label htmlFor="lastName">Last Name</label>
                    <input id="lastName" name="lastName" type="text" value={form.lastName} onChange={updateField} autoComplete="family-name" required />

                    <label htmlFor="email">Email</label>
                    <input id="email" name="email" type="email" value={form.email} onChange={updateField} autoComplete="email" required />

                    <label htmlFor="password">Password</label>
                    <input id="password" name="password" type="password" value={form.password} onChange={updateField} minLength={8} autoComplete="new-password" required />

                    {error && <p className="form-error" role="alert">{error}</p>}
                    {success && <p className="form-success" role="status">Your account has been created.</p>}
                    <button className="btn btn-accent" type="submit">Register</button>
                </form>
            </div>
        </section>
    );
}
