async function login() {
    const res = await fetch("/login", {
        method: "POST"
    });

    const data = await res.json();

    localStorage.setItem("token", data.access_token);

    alert("Login successful");
}

async function fetchData(type) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "Loading...";

    try {
        const token = localStorage.getItem("token");

        const res = await fetch(`/api/v1/${type}`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (res.status === 401) {
            resultDiv.innerHTML = "<p>Unauthorized. Please login again.</p>";
            return;
        }

        const data = await res.json();

        if (!Array.isArray(data) || data.length === 0) {
            resultDiv.innerHTML = `<p class="empty">No ${type} found.</p>`;
            return;
        }

        let table = "<table><tr>";

        Object.keys(data[0]).forEach(key => {
            table += `<th>${key}</th>`;
        });

        table += "</tr>";

        data.forEach(item => {
            table += "<tr>";
            Object.values(item).forEach(val => {
                table += `<td>${val ?? ""}</td>`;
            });
            table += "</tr>";
        });

        table += "</table>";

        resultDiv.innerHTML = table;

    } catch (err) {
        console.error(err);
        resultDiv.innerHTML = "Error loading data";
    }
}

window.createCustomer = async function () {
    const input = prompt("Enter details:\nName\nEmail\nPhone");

    if (!input) return;

    const [name, email, phone] = input.split(",");

    const token = localStorage.getItem("token");

    const res = await fetch("/api/v1/customers", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            name: name?.trim(),
            email: email?.trim(),
            phone: phone?.trim()
        })
    });

    alert("Customer created");
};

async function updateCustomer() {
    const id = prompt("Enter customer ID");
    const phone = prompt("Enter new phone");

    const token = localStorage.getItem("token");

    const res = await fetch(`/api/v1/customers/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ phone })
    });

    alert(await res.text());
}

async function deleteCustomer() {
    const id = prompt("Enter customer ID");

    const token = localStorage.getItem("token");

    const res = await fetch(`/api/v1/customers/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    alert(await res.text());
}

window.createProduct = async function () {
    const input = prompt("Enter Name, Price");

    const [name, price] = input.split(",");

    const token = localStorage.getItem("token");

    await fetch("/api/v1/products", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            name: name?.trim(),
            price: Number(price)
        })
    });

    alert("Product created");
};

window.updateProduct = async function () {
    const input = prompt("Enter ID, New Name, New Price");

    const [id, name, price] = input.split(",");

    const token = localStorage.getItem("token");

    await fetch(`/api/v1/products/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            name: name?.trim(),
            price: Number(price)
        })
    });

    alert("Product updated");
};

window.deleteProduct = async function () {
    const id = prompt("Enter Product ID");

    const token = localStorage.getItem("token");

    await fetch(`/api/v1/products/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    alert("Product deleted");
};

window.createOrder = async function () {
    const input = prompt("Enter Customer ID");

    const token = localStorage.getItem("token");

    await fetch("/api/v1/orders", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            partner_id: Number(input)
        })
    });

    alert("Order created");
};

window.updateOrder = async function () {
    const input = prompt("Enter Order ID, New Customer ID, State");

    const [id, partner_id, state] = input.split(",");

    const token = localStorage.getItem("token");

    await fetch(`/api/v1/orders/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            partner_id: partner_id ? Number(partner_id) : null,
            state: state?.trim()
        })
    });

    alert("Order updated");
};

window.deleteOrder = async function () {
    const id = prompt("Enter Order ID");

    const token = localStorage.getItem("token");

    await fetch(`/api/v1/orders/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    alert("Order deleted");
};