$(document).ready(function() {
       $("#add-to-cart-btn").click(function(e) {
        e.preventDefault();
        var is_Authenticated =$(this).data('is-authenticated')
        if (is_Authenticated === 'True') {
            console.log("User is authenticated");
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
                    } else if(res.response === 'success'){
                        Swal.fire({
                            icon: 'success',
                            title: 'Success',
                            text: 'Item Was Added to Your Cart!'
                        });
                    }
                },
            });
        } else {

            Swal.fire({
                icon: 'warning',
                title: 'Warning',
                text: 'You must be logged in to your account'
            }).then(function () {
                $(location).attr('href', '/accounts/login/');
            });
        }
    });
});



$(document).ready(function() {
    $("#remove-from-cart").click(function(e) {
        e.preventDefault();
        var is_Authenticated =$(this).data('is-authenticated')
        if (is_Authenticated === 'True') {
            var RemovefromCartUrl = $(this).data('url');
            var slug = $(this).data('slug');
            $.ajax({
                type: "GET",
                url: RemovefromCartUrl,
                data: {slug: slug},
                success: function (res) {
                    if (res.response === 'remove') {
                        Swal.fire({
                            icon: 'success',
                            title: 'Success',
                            text: 'Your Item Remove the Cart'
                        });
                    } else if (res.response === 'empty') {
                        Swal.fire({
                            icon: 'success',
                            title: 'Success',
                            text: 'You Dont have active Cart!'
                        });
                    }

                },
            });
        }
        else {
            Swal.fire({
                icon: 'warning',
                title: 'Warning',
                text: 'You must be logged in to your account'
            }).then(function () {
                $(location).attr('href', '/accounts/login/');
            });
        }
    });
});









