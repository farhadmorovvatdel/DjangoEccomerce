$(document).ready(function() {
    $("#add-to-cart-btn").click(function(e) {
        e.preventDefault();
        var addToCartUrl = $(this).data('url');
        var slug = $(this).data('slug');
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



$(document).ready(function() {
    $("#remove-from-cart").click(function(e) {
        e.preventDefault();
        var RemovefromCartUrl = $(this).data('url');
        var slug = $(this).data('slug');
        $.ajax({
            type: "GET",
            url: RemovefromCartUrl,
            data: { slug: slug },
            success: function(res) {
               if (res.response === 'remove') {
                   Swal.fire({
                   icon: 'success',
                   title: 'Success',
                   text: 'Your Item Remove the Cart'
                });
               }
               // else if(res.response ==='success'){
               //     Swal.fire({
               //     icon: 'success',
               //     title: 'Success',
               //     text: 'Item Was Add to Your Cart!'
               //  });
               // }
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


