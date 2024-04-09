$(document).ready(function() {
    $("#add-to-cart-btn").click(function(e) {
        e.preventDefault(); // Prevent default anchor behavior
        var addToCartUrl = $(this).data('url'); // Get the URL from data-url attribute
        var slug = $(this).data('slug'); // Get the slug from data-slug attribute
        $.ajax({
            type: "GET",
            url: addToCartUrl,
            data: { slug: slug },
            success: function(res) {
               if (res.response === 'updated') {
                   Swal.fire({
                   icon: 'success',
                   title: 'Success',
                   text: 'Your Cart was Updated!'
                });
               }
               else if(res.response ==='success'){
                   Swal.fire({
                   icon: 'success',
                   title: 'Success',
                   text: 'Item Was Add to Your Cart!'
                });
               }
            },
        });
    });
});

// $(document).ready(function(){
//     $("#add-to-cart-btn").click(function(e){
//         alert($("#add-to-cart").val())
//         e.preventDefault();
//         var url = $(this).data('url');
//         $.ajax({
//             type: "GET",
//             url: url,
//             success: function(data){
//                 if(data === 'success'){
//                     Swal.fire({
//                         icon: 'success',
//                         title: 'Success',
//                         text: 'Item added to cart successfully!'
//                     });
//                 }
//             },
//
//         });
//     });
// });


