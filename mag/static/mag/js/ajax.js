$(document).ready(function () {
        $.ajax({
            type: 'GET',
            url: '/product/',
            dataType: 'json',
            success: function (data) {
                $.each(data, function (i, val) {
                    var html = "<div class='col-lg-4 col-md-6 mb-r'>" +
                        "                <div class='card card-cascade narrower'>" +
                        "                    <div class='view gradient-card-header blue-gradient'>" +
                        "                        <h2 class='h2-responsive'>"+val.name+"</h2>" +
                        "                        <p>£"+val.price+"</p>"+
                        "                        <div class='text-center'>" +
                        "                           <a type='button' class='btn-floating btn-lg waves-effect waves-light'>Edit</a>" +
                        "                           <a type='button' class='btn-floating btn-lg waves-effect waves-light'>Delete</a>" +
                        "                       </div>"+
                        "                    </div>" +
                        "                   <div class='card-body text-center'><p class='card-text'>"+val.description+"</p></div>"+
                        "                </div>" +
                        "            </div>";
                    $('#in').append(html)
                })
            }
        });
});
