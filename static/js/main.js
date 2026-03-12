$(document).ready(function () {
    // Hide sections initially
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Preview uploaded image
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('.image-section').fadeIn(500);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#imageUpload").change(function () {
        $('#result').hide();
        readURL(this);
    });

    // Handle Predict button
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        $(this).hide();
        $('.loader').show();

        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result span').text('Result: ' + data);
                $('#btn-predict').show();
            },
            error: function () {
                $('.loader').hide();
                $('#btn-predict').show();
                alert("Upload failed.");
            }
        });
    });
});