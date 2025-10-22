function getCSRFToken() {
    const csrfInput = document.querySelector("[name=csrfmiddlewaretoken]");
    if (!csrfInput) {
        console.error("CSRF token not found in DOM!");
        return "";
    }
    return csrfInput.value;
}

function addToCart(event, formElement, productSlug) {
    event.preventDefault();

    const quantityInput = formElement.querySelector('input[name="quantity"]');
    const quantity = quantityInput ? quantityInput.value : 1;

    const button = formElement.querySelector('button[type="submit"]');
    const spinner = button.querySelector(".spinner-border");
    const buttonText = button.querySelector(".btn-text");

    // Show spinner
    spinner.classList.remove("d-none");
    buttonText.classList.add("d-none");
    button.disabled = true;

    const myUrl = window.CART_ADD_AJAX_URL;

    fetch(myUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken(),
        },
        body: new URLSearchParams({
            slug: productSlug,
            quantity: quantity,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                document.getElementById("cart-count").innerText = data.cartCount;
                showCartToast(data.message);
            } else {
                showCartToast("Error: " + data.error);
            }
        })
        .catch((err) => {
            showCartToast("Something went wrong.");
            console.error(err);
        })
        .finally(() => {
            // Hide spinner, restore button
            spinner.classList.add("d-none");
            buttonText.classList.remove("d-none");
            button.disabled = false;
        });
}

function showCartToast(message) {
    const toastBody = document.getElementById("cart-toast-body");
    const toastEl = document.getElementById("cart-toast");

    toastBody.innerText = message;

    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}

// update and remove item from cart
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".update-btn").forEach((button) => {
        button.addEventListener("click", () => {
            const row = button.closest(".cart-item"); // ✅ changed
            const slug = row.dataset.slug;
            const quantity = row.querySelector(".qty-input").value; // ✅ matches your class name

            fetch(window.CART_UPDATE_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: new URLSearchParams({ slug, quantity }),
            })
                .then((res) => res.json())
                .then((data) => {
                    if (data.success) {
                        row.querySelector(".item-total").innerText = `₦${data.itemTotal}`;
                        document.getElementById("cart-subtotal").innerText = "₦" + data.cartTotal;
                        document.getElementById("cart-final-total").innerText = "₦" + data.finalTotal;
                        document.getElementById("cart-count").innerText = data.cartCount;
                        showCartToast("Quantity updated!");
                    } else {
                        showCartToast("Error updating item.");
                    }
                });
        });
    });

    document.querySelectorAll(".remove-btn").forEach((button) => {
        button.addEventListener("click", () => {
            const row = button.closest(".cart-item"); // ✅ changed
            const slug = row.dataset.slug;

            fetch(window.CART_REMOVE_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: new URLSearchParams({ slug }),
            })
                .then((res) => res.json())
                .then((data) => {
                    if (data.success) {
                        row.remove();
                        document.getElementById("cart-count").innerText = data.cartCount;
                        document.getElementById("cart-subtotal").innerText = "₦" + data.cartTotal;
                        document.getElementById("cart-final-total").innerText = "₦" + data.finalTotal;
                        showCartToast("Item removed.");
                    } else {
                        showCartToast("Error removing item.");
                    }
                });
        });
    });
});
