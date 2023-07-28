$(document).ready(function(){
    $('.payWithRazorpay').click(function(e){
        e.preventDefault();

        var address=$(".address:checked").val();
        var token=$('input[name=csrfmiddlewaretoken]').val();
        console.log(address)
        if (address == undefined){
            
            swal("Alert", "All Fields are required", "error");
            return false;
        }
        else
        {
            $.ajax({
                method: "GET",
                url: "/orders/proceed_to_pay",
                
                success: function (response) {
                    // console.log(response);
                    var options = {
                        "key": "rzp_test_Nq0pUqfDOMPhrY", // Enter the Key ID generated from the Dashboard
                        "amount": response.total_price*100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "EShopper",
                        "description": "Thank You For Your Purchase",
                    
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responseb){
                            // alert(responseb.razorpay_payment_id);
                            data={
                                'address':address,
                                "payment_mode":"Razorpay",
                                'payment_id': responseb.razorpay_payment_id,
                                csrfmiddlewaretoken:token
                            }
                            $.ajax({
                                method: "POST",
                                url: "/orders/place_order/",
                                data: data,
                                success: function (responsec) {
                                    swal("Congrats",responsec.status).then((value) => {
                                        window.location.href='/orders/order_summary/'
                                    });
                                    
                                    
                                }
                            });
                        },
                        "prefill": {
                            "name": "Gaurav Kumar",
                            "email": "gaurav.kumar@example.com",
                            "contact": "9999999999"
                        },
                        "notes": {
                            "address": "Razorpay Corporate Office"
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                    
                }
            });
      
        }

        
    });
});

