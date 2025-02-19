$(document).ready(function (){
    $(".filter-checkbox, #price-filter").on("click", function(){

        let fillter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        fillter_object.min_price = min_price;
        fillter_object.max_price = max_price;

        $(".filter-checkbox").each(function (){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

            fillter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
                return element.value
            })
        })
        $.ajax({
            url: '/filter-products',
            data: fillter_object,
            dataType: 'json',
            success: function(response){
                console.log(response);
                $("#div-filter-product").html(response.data)
            }
        })
    })

    $("#max_price").on("blur", function(){
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){

            min_price = Math.round(min_price * 100) / 100
            max_price = Math.round(max_price * 100) / 100

            alert("Price must be between $" + min_price + " and $" + max_price)
            $(this).val(min_price)
            $("#range").val(min)

            $(this).focus()

            return false
        }
        
    })
})