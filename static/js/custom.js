
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
                    updateCartItemCount()
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

    updateCartItemCount();
    function updateCartItemCount() {
        $.ajax({
            url: '/cart-item-count/',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                $('#badge-item').text(data.item_count);
            },
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
                        updateCartItemCount()
                    } else if (res.response === 'empty') {
                        Swal.fire({
                            icon: 'success',
                            title: 'success',
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
     updateCartItemCount();
    function updateCartItemCount() {
        $.ajax({
            url: '/cart-item-count/',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                $('#badge-item').text(data.item_count);
               // we can the icon for sales bring the body and the show with badg.text in here
               //  sales icon at header

            },

        });
    }
    });
});

// $(document).ready(function() {
//     $('.faviorate-btn').click(function() {
//         var itemid = $(this).data('item-id');
//         $.ajax({
//             type: 'GET',
//             url: '/faviorate-item/' + itemid  ,
//             success: function(res) {
//                 if (res.faviorate === true) {
//
//                     // $('.faviorate-btn').css('background-color','red')
//                     console.log('faviorate')
//                 } else {
//                 //    $('.faviorate-btn').css('background-color','blue')
//                     console.log('not faviorate')
//                 }
//             }
//         });
//     });
// });


$(document).ready(function() {
    $('#faviorate-btn').click(function() {
        var itemid = $(this).data('item-id');
        $.get('/faviorate-item/' + itemid).then(function (res){
            if (res.faviorate === true) {
                $('#faviorate-btn').css('background-color','brown')
                $('#faviorate-btn').text('Unfavorite');
                console.log('favored');

            } else {
                $('#faviorate-btn').css('background-color','black')
                $('#faviorate-btn').text('favorite');
            }
        });
    });
});

$(document).ready(function(){
    $('#cart-plus').on('click',function (event){
        event.preventDefault();
        var slug=$(this).data('slug');
        $.get('/add-single-item-to-cart/' + slug ).then(function (res){
            if(res.response === 'success'){
                var plus= parseInt($('#input-id').val())
                var newplus=plus +1
                $('#input-id').val(newplus)
                $(location).attr('href', '/order-summary/');

            }
        })
    })
})



$(document).ready(function(){
    $('#cart-mines').on('click',function (event){
        event.preventDefault();
        var slug=$(this).data('slug');
        $.get('/remove-single-item-from-cart/' + slug ).then(function (res){
            if(res.response === 'remove'){
                 var mines=$('#input-id').val()
                 var newmines=mines -1
                 $('#input-id').val(newmines)
                 $(location).attr('href', '/order-summary/');
            }
        })

        })
})

$(document).ready(function (){
    $('#remove-cart-summary').click(function (event){
        event.preventDefault();
        var slug= $(this).data('slug')
        $.get('/remove-from-cart/' + slug).then(function (res){
            if(res.response ==='remove'){
                $(location).attr('href', '/order-summary/');
            }
        })
    })
})