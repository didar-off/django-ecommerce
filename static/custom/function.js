$(document).ready(function () {
    // SweetAlert2 Setting Toast
    const Toast = Swal.mixin({
        toast: true,
        position: "top-end", // position of toast
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer);
            toast.addEventListener('mouseleave', Swal.resumeTimer);
        }
    });

    // Generate or Get cart_id from localStorage
    function generateCardId() {
        let cartId = localStorage.getItem('cartId');
        if (!cartId) {
            cartId = '';
            for (let i = 0; i < 10; i++) {
                cartId += Math.floor(Math.random() * 10);
            }
            localStorage.setItem('cartId', cartId);
        }
        return cartId;
    }

    // Setup Add To Cart Button
    $(document).on("click", ".add_to_cart", function (e) {
        e.preventDefault();

        const button_el = $(this);
        const id = button_el.attr("data-id");
        const qty = $(".quantity").val();
        const weight = $("input[name='weight']:checked").val();
        const color = $("input[name='color']:checked").val();
        const cart_id = generateCardId();

        // Validate Data
        if (!color || !weight || !qty || qty <= 0) {
            Toast.fire({
                icon: "error",
                title: "Please select color, weight and set quantity."
            });
            return;
        }

        // Send AJAX-request to server
        $.ajax({
            url: "/add-to-cart/",
            method: "GET",
            data: {
                id: id,
                qty: qty,
                weight: weight,
                color: color,
                cart_id: cart_id,
            },
            beforeSend: function () {
                button_el.html("Adding To Cart <i class='fas fa-spinner fa-spin ms-2'></i>");
            },
            success: function (response) {
                console.log("Success:", response);
                Toast.fire({
                    icon: "success",
                    title: response?.message || "Product added to cart!"
                });
                button_el.html("Add To Cart <i class='fas fa-shopping-cart ms-2'></i>");
                $(".total_cart_items").text(response?.total_cart_items || 0);
            },
            error: function (xhr) {
                console.error("Error:", xhr.responseText);
                let errorResponse = JSON.parse(xhr.responseText);
                Toast.fire({
                    icon: "error",
                    title: errorResponse?.error || "Something went wrong."
                });
            }
        });
    });
});
