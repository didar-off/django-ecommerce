$(document).ready(function () {
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


    // Add to cart
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


    // Update cart quantity
    $(document).on("click", ".update_cart_qty", function () {
        const button_el = $(this);
        const update_type = button_el.attr("data-update_type");
        const item_id = button_el.attr("data-item_id");
        const product_id = button_el.attr("data-product_id");
        var qty = $(".item-qty-" + item_id).val();
        const cart_id = generateCardId();

        if (update_type === "increase") {
            $(".item-qty-" + item_id).val(parseInt(qty) + 1);
            qty++;
        } else {
            if (parseInt(qty) <= 1) {
                $(".item-qty-" + item_id).val(1);
                qty = 1;
            } else {
                $(".item-qty-" + item_id).val(parseInt(qty) - 1);
                qty--;
            }
        }

        // Send AJAX-request to server
        $.ajax({
            url: "/add-to-cart/",
            data: {
                id: product_id,
                qty: qty,
                cart_id: cart_id,
            },
            beforeSend: function () {
                button_el.html("<i class='fas fa-spinner fa-spin ms-2'></i>");
            },
            success: function (response) {
                console.log("Success:", response);
                Toast.fire({
                    icon: "success",
                    title: response?.message || "Product added to cart!"
                });

                if (update_type === "increase") {
                    button_el.html("+");
                } else {
                    button_el.html("-");
                }

                $(".item_sub_total_" + item_id).text(response.item_sub_total);
                $(".cart_sub_total").text(response.cart_sub_total);
            },
            error: function (xhr) {
                console.error("Error:", xhr.responseText);
                let errorResponse = JSON.parse(xhr.responseText);
                Toast.fire({
                    icon: "error",
                    title: errorResponse?.error || "Something went wrong."
                });

                if (update_type == "increase") {
                    button_el.html("+");
                } else {
                    button_el.html("-");
                }
            }
        });
    });


    $(document).on("click", ".delete_cart_item", function(){
        const button_el = $(this);
        const item_id = button_el.attr("data-item_id");
        const product_id = button_el.attr("data-product_id");
        const cart_id = generateCardId();

        $.ajax({
            url: "/delete-cart-item/",
            method: "GET",
            data: {
                id: product_id,
                item_id: item_id,
                cart_id: cart_id,
            },
            beforeSend: function () {
                button_el.html("<i class='fas fa-spinner fa-spin ms-2'></i>");
            },
            success: function (response) {
                console.log("Success:", response);
                Toast.fire({
                    icon: "success",
                    title: response?.message || "Product added to cart!"
                });
                $(".total_cart_items").text(response?.total_cart_items || 0);
                $(".cart_sub_total").text(response?.cart_sub_total || 0);
                $(".item_div_" + item_id).fadeOut(300, function () {
                    $(this).remove();
                });
            },
        });
    });
});
